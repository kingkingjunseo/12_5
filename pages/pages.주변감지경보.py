
import streamlit as st
import requests
import folium
import streamlit.components.v1 as components

from streamlit_geolocation import streamlit_geolocation
from streamlit_folium import st_folium

# ------------------------------
# 기본 설정
# ------------------------------
st.set_page_config(
    page_title="안전 동행",
    page_icon="🌼",
    layout="wide",
)

# ------------------------------
# 따뜻하고 둥근 디자인
# ------------------------------
st.markdown("""
<style>
.stApp {
    background: #FFF9F0;
    color: #3F3932;
}
.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #594638;
}
div.stButton > button {
    border-radius: 18px;
    min-height: 54px;
    font-size: 18px;
    font-weight: 700;
    border: 1px solid #E8D5BE;
    background: #F5E5D0;
    color: #49382B;
}
div.stButton > button:hover {
    background: #EBD2B3;
    border-color: #D9B894;
}
div[data-testid="stAlert"] {
    border-radius: 16px;
}
.welcome-card {
    background: #F5E8D8;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
}
.small-note {
    color: #786B5E;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌼 안전 동행")
st.markdown("""
<div class="welcome-card">
    <h3>오늘도 안전하게 걸어요!</h3>
    현재 위치를 확인하고 주변의 보행 주의 정보를 찾아보세요.
</div>
""", unsafe_allow_html=True)

# ------------------------------
# 세션 상태 초기화
# ------------------------------
if "hazards" not in st.session_state:
    st.session_state.hazards = []
if "searched_location" not in st.session_state:
    st.session_state.searched_location = None
if "search_error" not in st.session_state:
    st.session_state.search_error = None

# ------------------------------
# 현재 위치
# ------------------------------
st.subheader("📍 내 현재 위치")

location = streamlit_geolocation()

if not isinstance(location, dict):
    st.info("위치 확인 버튼을 누르고 브라우저의 위치 권한을 허용해 주세요.")
    st.stop()

latitude = location.get("latitude")
longitude = location.get("longitude")
accuracy = location.get("accuracy")

if latitude is None or longitude is None:
    st.warning(
        "아직 위치 정보가 없습니다. 위치 확인 버튼을 다시 눌러 주세요."
    )
    st.stop()

try:
    latitude = float(latitude)
    longitude = float(longitude)
    accuracy = float(accuracy) if accuracy is not None else None
except (ValueError, TypeError):
    st.error("위치 좌표를 읽을 수 없습니다. 다시 위치를 확인해 주세요.")
    st.stop()

if not (
    -90 <= latitude <= 90
    and -180 <= longitude <= 180
):
    st.error("올바르지 않은 위치 좌표입니다.")
    st.stop()

st.write(f"**위도:** {latitude:.6f}")
st.write(f"**경도:** {longitude:.6f}")

if accuracy is None:
    st.warning("위치 정확도를 확인할 수 없습니다.")
elif accuracy > 200:
    st.warning(
        f"위치 오차가 약 ±{accuracy:.0f}m입니다. "
        "주변 위험 정보가 부정확할 수 있습니다. "
        "기기의 위치 권한을 확인하고 다시 시도해 주세요."
    )
else:
    st.success(f"위치 확인 완료 · 표시된 정확도 약 ±{accuracy:.0f}m")

current_location = (
    round(latitude, 5),
    round(longitude, 5),
)

# 위치가 바뀌면 예전 위치의 위험 정보는 표시하지 않음
if st.session_state.searched_location != current_location:
    st.session_state.hazards = []
    st.session_state.search_error = None

# ------------------------------
# 주변 지도 데이터 검색
# ------------------------------
@st.cache_data(ttl=180)
def search_nearby(lat, lon):
    query = f"""
    [out:json][timeout:20];
    (
      nwr(around:500,{lat},{lon})["construction"];
      nwr(around:500,{lat},{lon})["highway"="steps"];
      nwr(around:500,{lat},{lon})["barrier"="construction"];
      nwr(around:500,{lat},{lon})
        ["highway"="footway"]["surface"~"gravel|unpaved"];
    );
    out center tags;
    """

    servers = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
    ]

    errors = []

    for server in servers:
        try:
            response = requests.post(
                server,
                data={"data": query},
                timeout=(10, 30),
                headers={"User-Agent": "SafetyDonghaeng/1.0"},
            )
            response.raise_for_status()
            data = response.json()

            results = []
            seen = set()

            for element in data.get("elements", []):
                tags = element.get("tags", {})

                if "lat" in element and "lon" in element:
                    h_lat = element["lat"]
                    h_lon = element["lon"]
                else:
                    center = element.get("center", {})
                    h_lat = center.get("lat")
                    h_lon = center.get("lon")

                if h_lat is None or h_lon is None:
                    continue

                unique_id = (element.get("type"), element.get("id"))
                if unique_id in seen:
                    continue
                seen.add(unique_id)

                if (
                    "construction" in tags
                    or tags.get("barrier") == "construction"
                ):
                    kind = "공사 관련 정보"
                elif tags.get("highway") == "steps":
                    kind = "계단"
                elif tags.get("surface") in ("gravel", "unpaved"):
                    kind = "자갈·비포장 보행로"
                else:
                    continue

                results.append({
                    "lat": float(h_lat),
                    "lon": float(h_lon),
                    "kind": kind,
                    "name": tags.get("name", "이름 미등록"),
                })

            return results, None

        except (requests.RequestException, ValueError) as error:
            errors.append(f"{server}: {error}")

    return [], "주변 정보 서버 연결 실패: " + " / ".join(errors)


st.subheader("🚧 주변 보행 주의 정보")

if accuracy is not None and accuracy > 200:
    st.button(
        "🔎 주변 주의 정보 검색",
        disabled=True,
        use_container_width=True,
    )
    st.caption("위치 정확도가 낮아 검색을 잠시 중단했습니다.")
else:
    if st.button(
        "🔎 주변 500m 위험 정보 검색",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("주변 지도 정보를 확인하고 있어요..."):
            hazards, error = search_nearby(
                round(latitude, 5),
                round(longitude, 5),
            )

        st.session_state.hazards = hazards
        st.session_state.search_error = error
        st.session_state.searched_location = current_location

# ------------------------------
# 지도 표시
# ------------------------------
st.subheader("🗺️ 내 주변 지도")

hazards = st.session_state.hazards
search_error = st.session_state.search_error

map_view = folium.Map(
    location=[latitude, longitude],
    zoom_start=17,
    control_scale=True,
)

folium.Marker(
    [latitude, longitude],
    tooltip="내 현재 위치",
    popup="현재 기기에서 받은 위치",
    icon=folium.Icon(color="blue", icon="user", prefix="fa"),
).add_to(map_view)

folium.Circle(
    [latitude, longitude],
    radius=500,
    color="#E5A35C",
    fill=True,
    fill_opacity=0.08,
    tooltip="주변 검색 범위 500m",
).add_to(map_view)

for item in hazards:
    folium.Marker(
        [item["lat"], item["lon"]],
        tooltip=item["kind"],
        popup=(
            f'{item["kind"]}<br>'
            f'이름: {item["name"]}'
        ),
        icon=folium.Icon(
            color="red",
            icon="exclamation-triangle",
            prefix="fa",
        ),
    ).add_to(map_view)

st_folium(
    map_view,
    height=480,
    use_container_width=True,
    key=f"map_{latitude:.5f}_{longitude:.5f}",
)

st.caption("🔵 파란색은 현재 위치 · 🔴 빨간색은 검색된 보행 주의 정보")

# ------------------------------
# 경보 표시 및 경보음
# ------------------------------
if search_error:
    st.error(
        "주변 정보 서버에 연결하지 못했습니다. "
        "위험 정보가 없다는 뜻은 아닙니다."
    )
    st.caption(search_error)

elif st.session_state.searched_location == current_location:
    if hazards:
        st.error(
            f"🚨 주의! 주변에서 보행 주의 정보 {len(hazards)}개를 찾았습니다."
        )

        for item in hazards:
            st.warning(f"⚠️ {item['kind']} — {item['name']}")

        st.markdown("### 🔊 경보음")

        # 브라우저의 자동 재생 제한을 피할 수 있도록
        # 사용자가 버튼을 직접 누르면 경보음을 재생함
        components.html("""
        <div style="
            background:#FCE7E2;
            border-radius:18px;
            padding:16px;
            font-family:sans-serif;
            text-align:center;
        ">
          <button id="alarm" style="
            background:#B83227;
            color:white;
            border:0;
            border-radius:14px;
            padding:14px 22px;
            font-size:18px;
            font-weight:bold;
            cursor:pointer;
          ">🔔 경보음 재생</button>
          <p id="message" style="color:#7A2E27;">
            위험 정보가 표시되었습니다. 주변을 살피고 안전한 길을 선택하세요.
          </p>
        </div>
        <script>
        const button = document.getElementById("alarm");
        const message = document.getElementById("message");

        button.addEventListener("click", async () => {
          try {
            const AudioContext =
              window.AudioContext || window.webkitAudioContext;
            const audio = new AudioContext();
            await audio.resume();

            for (let i = 0; i < 3; i++) {
              const oscillator = audio.createOscillator();
              const gain = audio.createGain();

              oscillator.type = "sine";
              oscillator.frequency.value = 880;
              gain.gain.value = 0.18;

              oscillator.connect(gain);
              gain.connect(audio.destination);

              const start = audio.currentTime + i * 0.45;
              oscillator.start(start);
              oscillator.stop(start + 0.25);
            }

            message.textContent = "경보음을 재생했습니다.";
          } catch (e) {
            message.textContent =
              "소리를 재생하지 못했습니다. 기기의 음량을 확인해 주세요.";
          }
        });
        </script>
        """, height=150)

    else:
        st.success("검색 조건에 맞는 주의 정보를 찾지 못했습니다.")
        st.caption(
            "지도에 등록되지 않은 위험이 있을 수 있으니 "
            "주변을 계속 살펴보세요."
        )

st.divider()
st.markdown("""
<div class="small-note">
🌷 안전 동행은 보행을 돕는 시제품입니다. 지도 데이터는 실시간 정보가 아닐 수 있으며,
실제 장애물이나 다가오는 차량을 자동으로 감지하지 않습니다.
</div>
""", unsafe_allow_html=True)
