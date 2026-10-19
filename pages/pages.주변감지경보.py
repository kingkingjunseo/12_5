
import streamlit as st
import requests
import folium

from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

# =========================
# 1. 페이지 설정
# =========================
st.set_page_config(
    page_title="안전 동행",
    page_icon="🌼",
    layout="wide",
)

# =========================
# 2. 디자인
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #FFF9F0;
    color: #493D32;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #654B3B;
}
div.stButton > button {
    border-radius: 18px;
    min-height: 54px;
    font-size: 18px;
    font-weight: bold;
    background-color: #F3DFC7;
    color: #493D32;
    border: 1px solid #E3C7A8;
}
div.stButton > button:hover {
    background-color: #EBD0B0;
    border-color: #D9B58E;
}
div[data-testid="stAlert"] {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌼 안전 동행")
st.markdown("""
안녕하세요! 오늘도 안전하게 걸어요.  
현재 위치를 확인하고 주변의 보행 주의 정보를 찾아볼게요.
""")

# =========================
# 3. 현재 위치 가져오기
# =========================
st.subheader("📍 내 현재 위치")

location = streamlit_geolocation()

if not isinstance(location, dict):
    st.info("위치 확인 버튼을 누르고 위치 권한을 허용해 주세요.")
    st.stop()

latitude = location.get("latitude")
longitude = location.get("longitude")
accuracy = location.get("accuracy")

if latitude is None or longitude is None:
    st.warning("위치 정보가 없습니다. 위치 확인 버튼을 다시 눌러 주세요.")
    st.stop()

try:
    latitude = float(latitude)
    longitude = float(longitude)
    accuracy = float(accuracy) if accuracy is not None else None
except (ValueError, TypeError):
    st.error("위치 좌표를 읽을 수 없습니다. 다시 시도해 주세요.")
    st.stop()

if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
    st.error("잘못된 위치 좌표가 전달되었습니다.")
    st.stop()

st.write(f"**위도:** {latitude:.6f}")
st.write(f"**경도:** {longitude:.6f}")

if accuracy is None:
    st.warning("위치 정확도를 확인할 수 없습니다.")
elif accuracy > 200:
    st.warning(
        f"위치 오차가 약 ±{accuracy:.0f}m입니다. "
        "주변 정보가 부정확할 수 있으니 위치 권한과 기기 설정을 확인해 주세요."
    )
else:
    st.success(f"위치를 받았습니다. 표시된 정확도는 약 ±{accuracy:.0f}m입니다.")

# =========================
# 4. 주변 보행 주의 정보 검색
# =========================
@st.cache_data(ttl=180)
def search_hazards(lat, lon):
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

            hazards = []
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

                element_id = (element.get("type"), element.get("id"))
                if element_id in seen:
                    continue
                seen.add(element_id)

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

                hazards.append({
                    "lat": float(h_lat),
                    "lon": float(h_lon),
                    "kind": kind,
                    "name": tags.get("name", "이름 미등록"),
                })

            return hazards, None

        except (requests.RequestException, ValueError) as error:
            errors.append(str(error))

    return [], "주변 정보 서버에 연결하지 못했습니다: " + " / ".join(errors)


st.subheader("🚧 주변 500m 보행 주의 정보")

if st.button("🔎 주변 주의 정보 검색", use_container_width=True):
    if accuracy is not None and accuracy > 200:
        st.session_state["hazards"] = []
        st.session_state["hazard_error"] = "위치 정확도가 낮습니다."
        st.session_state["searched_coords"] = (
            round(latitude, 5), round(longitude, 5)
        )
    else:
        with st.spinner("주변 정보를 검색하고 있어요..."):
            hazards, error = search_hazards(
                round(latitude, 5),
                round(longitude, 5),
            )

        st.session_state["hazards"] = hazards
        st.session_state["hazard_error"] = error
        st.session_state["searched_coords"] = (
            round(latitude, 5), round(longitude, 5)
        )

# =========================
# 5. 지도 표시
# =========================
st.subheader("🗺️ 내 주변 지도")

current_coords = (round(latitude, 5), round(longitude, 5))

if st.session_state.get("searched_coords") != current_coords:
    hazards = []
    search_error = None
else:
    hazards = st.session_state.get("hazards", [])
    search_error = st.session_state.get("hazard_error")

map_view = folium.Map(
    location=[latitude, longitude],
    zoom_start=17,
    control_scale=True,
)

folium.Marker(
    [latitude, longitude],
    tooltip="내 현재 위치",
    popup=f"위도: {latitude:.6f}, 경도: {longitude:.6f}",
    icon=folium.Icon(color="blue", icon="user", prefix="fa"),
).add_to(map_view)

folium.Circle(
    [latitude, longitude],
    radius=500,
    color="#DCA36C",
    fill=True,
    fill_opacity=0.08,
    tooltip="검색 범위 약 500m",
).add_to(map_view)

for hazard in hazards:
    folium.Marker(
        [hazard["lat"], hazard["lon"]],
        tooltip=hazard["kind"],
        popup=f'{hazard["kind"]}<br>이름: {hazard["name"]}',
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

st.caption("🔵 파란색: 현재 위치 · 🔴 빨간색: 검색된 주의 정보")

# =========================
# 6. 경보
# =========================
if search_error:
    st.error(search_error)

elif st.session_state.get("searched_coords") == current_coords:
    if hazards:
        st.error(f"🚨 주변 보행 주의 정보 {len(hazards)}개를 찾았습니다.")

        for hazard in hazards:
            st.warning(f"⚠️ {hazard['kind']} — {hazard['name']}")

        st.markdown("### 🔔 경보음")

        if st.button("🔊 경보음 재생", use_container_width=True):
            components_code = """
            <script>
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            ctx.resume().then(() => {
              for (let i = 0; i < 3; i++) {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.frequency.value = 880;
                gain.gain.value = 0.2;
                osc.connect(gain);
                gain.connect(ctx.destination);
                const start = ctx.currentTime + i * 0.45;
                osc.start(start);
                osc.stop(start + 0.25);
              }
            });
            </script>
            """
            st.components.v1.html(components_code, height=0)

    else:
        st.success("검색 조건에 맞는 주의 정보를 찾지 못했습니다.")
        st.caption("주의 정보가 없더라도 주변을 계속 살펴보세요.")

st.divider()
st.caption(
    "🌷 안전 동행은 보행 보조용 시제품입니다. "
    "지도 데이터에 등록되지 않은 위험이나 실시간 장애물을 감지하지 못합니다."
)
