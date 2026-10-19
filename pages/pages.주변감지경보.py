
import streamlit as st
import requests
import folium
import streamlit.components.v1 as components
from streamlit_folium import st_folium

st.set_page_config(
    page_title="안전 동행",
    page_icon="🌼",
    layout="wide",
)

# 기존 학교 위치 유지
SCHOOL_LAT = 36.84152810
SCHOOL_LON = 127.14213325
SEARCH_RADIUS = 500

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


@st.cache_data(ttl=180)
def search_hazards(lat, lon):
    # 다양한 보행 위험 태그를 검색
    query = f"""
    [out:json][timeout:35];
    (
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["construction"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["highway"="construction"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["barrier"="construction"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["hazard"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["highway"="steps"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["natural"="cliff"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["man_made"="embankment"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["incline"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["surface"~"gravel|unpaved|ground|dirt|mud"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["smoothness"~"bad|very_bad|horrible|very_horrible|impassable"];
      nwr(around:{SEARCH_RADIUS},{lat},{lon})["tracktype"~"grade3|grade4|grade5"];
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
                timeout=(10, 45),
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

                key = (element.get("type"), element.get("id"))
                if key in seen:
                    continue
                seen.add(key)

                construction = (
                    "construction" in tags
                    or tags.get("highway") == "construction"
                    or tags.get("barrier") == "construction"
                )

                incline = str(tags.get("incline", "")).lower()
                steep = (
                    tags.get("natural") == "cliff"
                    or tags.get("man_made") == "embankment"
                    or incline in ("steep", "very_steep")
                )

                # 경사도 숫자가 등록된 경우 8% 초과를 주의 대상으로 분류
                try:
                    incline_number = float(
                        incline.replace("%", "").replace("+", "")
                    )
                    if abs(incline_number) > 8:
                        steep = True
                except ValueError:
                    pass

                steps = tags.get("highway") == "steps"

                rough_surface = (
                    tags.get("surface") in (
                        "gravel", "unpaved", "ground", "dirt", "mud"
                    )
                    or tags.get("smoothness") in (
                        "bad", "very_bad", "horrible",
                        "very_horrible", "impassable"
                    )
                    or tags.get("tracktype") in (
                        "grade3", "grade4", "grade5"
                    )
                )

                if construction:
                    kind = "🚧 공사 관련 정보"
                    severity = "공사"
                elif steep:
                    kind = "⛰️ 급경사·절벽 관련 정보"
                    severity = "경사"
                elif steps:
                    kind = "🪜 계단"
                    severity = "계단"
                elif rough_surface:
                    kind = "⚠️ 거친·비포장 보행로"
                    severity = "노면"
                elif tags.get("hazard"):
                    kind = "🚨 등록된 위험 정보"
                    severity = "위험"
                else:
                    continue

                hazards.append({
                    "lat": float(h_lat),
                    "lon": float(h_lon),
                    "kind": kind,
                    "severity": severity,
                    "name": tags.get("name", "이름 미등록"),
                    "details": (
                        f"표면: {tags.get('surface', '정보 없음')}, "
                        f"경사: {tags.get('incline', '정보 없음')}"
                    ),
                })

            return hazards, None

        except (requests.RequestException, ValueError) as error:
            errors.append(str(error))

    return [], "주변 위험 정보 서버에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요."


# 위치 찾기 버튼
if st.button("📍 현재 위치 찾기", use_container_width=True):
    st.session_state["show_map"] = True
    search_hazards.clear()

    with st.spinner("주변 보행 주의 정보를 검색하고 있어요..."):
        hazards, error = search_hazards(SCHOOL_LAT, SCHOOL_LON)

    st.session_state["hazards"] = hazards
    st.session_state["hazard_error"] = error
    st.session_state["alarm_pending"] = bool(hazards) and not error

# 다시 검색
if st.session_state.get("show_map", False):
    if st.button("🔎 주변 위험 정보 다시 검색", use_container_width=True):
        search_hazards.clear()

        with st.spinner("주변 정보를 다시 검색하고 있어요..."):
            hazards, error = search_hazards(SCHOOL_LAT, SCHOOL_LON)

        st.session_state["hazards"] = hazards
        st.session_state["hazard_error"] = error
        st.session_state["alarm_pending"] = bool(hazards) and not error

if st.session_state.get("show_map", False):
    hazards = st.session_state.get("hazards", [])
    error = st.session_state.get("hazard_error")

    st.subheader("🗺️ 내 주변 지도")

    m = folium.Map(
        location=[SCHOOL_LAT, SCHOOL_LON],
        zoom_start=17,
        control_scale=True,
    )

    # 검색 반경
    folium.Circle(
        [SCHOOL_LAT, SCHOOL_LON],
        radius=SEARCH_RADIUS,
        color="#DCA36C",
        fill=True,
        fill_opacity=0.07,
        tooltip="검색 범위 500m",
    ).add_to(m)

    # 현재 위치 표시
    folium.Marker(
        [SCHOOL_LAT, SCHOOL_LON],
        tooltip="현재 위치로 지정된 학교",
        popup="천안오성고등학교",
        icon=folium.Icon(
            color="blue",
            icon="user",
            prefix="fa",
        ),
    ).add_to(m)

    # 위험 정보는 큰 빨간 원 + 빨간 경고 아이콘으로 표시
    for hazard in hazards:
        popup_text = (
            f"{hazard['kind']}<br>"
            f"이름: {hazard['name']}<br>"
            f"{hazard['details']}"
        )

        folium.CircleMarker(
            location=[hazard["lat"], hazard["lon"]],
            radius=15,
            color="#8B0000",
            weight=3,
            fill=True,
            fill_color="#FF0000",
            fill_opacity=0.85,
            tooltip=hazard["kind"],
            popup=popup_text,
        ).add_to(m)

        folium.Marker(
            [hazard["lat"], hazard["lon"]],
            tooltip=f"⚠️ {hazard['kind']}",
            popup=popup_text,
            icon=folium.Icon(
                color="red",
                icon="exclamation-triangle",
                prefix="fa",
            ),
        ).add_to(m)

    st_folium(
        m,
        height=500,
        use_container_width=True,
        key="safety_donghaeng_map",
    )

    st.caption("🔵 파란색: 지정된 현재 위치 · 🔴 빨간색: 검색된 주의 정보")

    if error:
        st.error(error)

    elif hazards:
        st.error(f"🚨 주변 보행 주의 정보 {len(hazards)}개를 찾았습니다.")

        for hazard in hazards:
            st.warning(
                f"{hazard['kind']} — {hazard['name']} "
                f"({hazard['details']})"
            )

        # 브라우저가 자동 재생을 허용하면 경보음 재생을 시도
        if st.session_state.get("alarm_pending", False):
            components.html("""
            <script>
            (async () => {
              try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                await ctx.resume();
                for (let i = 0; i < 4; i++) {
                  const osc = ctx.createOscillator();
                  const gain = ctx.createGain();
                  osc.type = "sine";
                  osc.frequency.value = 880;
                  gain.gain.value = 0.22;
                  osc.connect(gain);
                  gain.connect(ctx.destination);
                  const start = ctx.currentTime + i * 0.5;
                  osc.start(start);
                  osc.stop(start + 0.3);
                }
              } catch (e) {}
            })();
            </script>
            """, height=0)
            st.session_state["alarm_pending"] = False

        # 자동 재생이 차단된 경우 사용자가 눌러 재생
        if st.button("🔔 경보음 재생", use_container_width=True):
            components.html("""
            <script>
            (async () => {
              const ctx = new (window.AudioContext || window.webkitAudioContext)();
              await ctx.resume();
              for (let i = 0; i < 4; i++) {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.frequency.value = 880;
                gain.gain.value = 0.22;
                osc.connect(gain);
                gain.connect(ctx.destination);
                const start = ctx.currentTime + i * 0.5;
                osc.start(start);
                osc.stop(start + 0.3);
              }
            })();
            </script>
            """, height=0)

    elif not error:
        st.success("검색 조건에 맞는 위험 정보를 찾지 못했습니다.")
        st.caption(
            "등록된 위험 정보가 없다는 뜻이며, "
            "실제로 위험이 없다는 보장은 없습니다."
        )

st.divider()
st.caption(
    "🌷 안전 동행은 보행 보조용 시제품입니다. "
    "지도에 등록되지 않은 공사장·급경사·장애물은 표시되지 않을 수 있습니다."
)
