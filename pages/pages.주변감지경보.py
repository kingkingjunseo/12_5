
import streamlit as st
import requests
import folium
import streamlit.components.v1 as components
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="안전 동행",
    page_icon="🌼",
    layout="wide",
)

# 천안오성고등학교 좌표
SCHOOL_LAT = 36.84152810
SCHOOL_LON = 127.14213325

# 따뜻하고 둥근 디자인 유지
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
}
div[data-testid="stAlert"] {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌼 안전 동행")
st.markdown("오늘도 안전하게 걸어요! 주변의 보행 주의 정보를 확인해 보세요.")

st.subheader("📍 현재 위치 확인")

# 학교를 테스트용 현재 위치로 지정
@st.cache_data(ttl=180)
def search_hazards(lat, lon):
    query = f"""
    [out:json][timeout:25];
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

    return [], "주변 정보 서버에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요."


# 현재 위치 찾기 버튼
if st.button("📍 현재 위치 찾기", use_container_width=True):
    st.session_state["show_map"] = True

    with st.spinner("주변 보행 주의 정보를 검색하고 있어요..."):
        hazards, error = search_hazards(SCHOOL_LAT, SCHOOL_LON)

    st.session_state["hazards"] = hazards
    st.session_state["hazard_error"] = error

# 주변 정보 다시 검색
if st.session_state.get("show_map", False):
    if st.button("🔎 주변 주의 정보 다시 검색", use_container_width=True):
        search_hazards.clear()

        with st.spinner("주변 정보를 다시 검색하고 있어요..."):
            hazards, error = search_hazards(SCHOOL_LAT, SCHOOL_LON)

        st.session_state["hazards"] = hazards
        st.session_state["hazard_error"] = error

# 지도와 위험 정보
if st.session_state.get("show_map", False):
    hazards = st.session_state.get("hazards", [])
    search_error = st.session_state.get("hazard_error")

    st.subheader("🗺️ 내 주변 지도")

    m = folium.Map(
        location=[SCHOOL_LAT, SCHOOL_LON],
        zoom_start=17,
        control_scale=True,
    )

    # 파란색 현재 위치 표시
    folium.Marker(
        [SCHOOL_LAT, SCHOOL_LON],
        tooltip="천안오성고등학교",
        popup="천안오성고등학교",
        icon=folium.Icon(color="blue", icon="user", prefix="fa"),
    ).add_to(m)

    # 주변 500m 범위
    folium.Circle(
        [SCHOOL_LAT, SCHOOL_LON],
        radius=500,
        color="#DCA36C",
        fill=True,
        fill_opacity=0.08,
        tooltip="검색 범위 약 500m",
    ).add_to(m)

    # 위험 위치를 빨간색으로 표시
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
        ).add_to(m)

    st_folium(
        m,
        height=480,
        use_container_width=True,
        key="safety_donghaeng_map",
    )

    st.caption("🔵 파란색: 현재 위치로 지정된 학교 · 🔴 빨간색: 검색된 주의 정보")

    if search_error:
        st.error(search_error)

    elif hazards:
        st.error(f"🚨 주변 보행 주의 정보 {len(hazards)}개를 찾았습니다.")

        for hazard in hazards:
            st.warning(f"⚠️ {hazard['kind']} — {hazard['name']}")

        if st.button("🔔 경보음 재생", use_container_width=True):
            components.html("""
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
            """, height=0)

    else:
        st.success("검색 조건에 맞는 보행 주의 정보를 찾지 못했습니다.")
        st.caption("주의 정보가 없더라도 주변을 계속 살펴보세요.")

st.divider()
st.caption(
    "🌷 안전 동행은 보행 보조용 시제품입니다. "
    "등록되지 않은 위험이나 실시간 장애물을 모두 감지하지는 못합니다."
)
