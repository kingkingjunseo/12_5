
import streamlit as st
import requests
import folium

from streamlit_geolocation import streamlit_geolocation
from streamlit_folium import st_folium


# ---------------------------
# 1. 기본 설정
# ---------------------------
st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="wide",
)

st.title("🚶 안전 동행")
st.header("어르신 보행 안전 도우미")

st.markdown("""
<style>
.stApp {
    font-size: 19px;
}
.stButton button {
    min-height: 55px;
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.info(
    "현재 위치를 지도에 표시하고, 주변 지도 데이터에 등록된 "
    "공사 구역과 계단 등의 보행 주의 요소를 찾아 표시합니다."
)


# ---------------------------
# 2. GPS 위치 가져오기
# ---------------------------
st.subheader("📍 현재 위치")

location = streamlit_geolocation()

if not isinstance(location, dict):
    st.warning(
        "현재 위치를 가져오려면 위의 위치 확인 버튼을 누르고 "
        "브라우저의 위치 권한을 허용해 주세요."
    )
    st.stop()

latitude = location.get("latitude")
longitude = location.get("longitude")

if latitude is None or longitude is None:
    st.info("위치 정보가 아직 없습니다. 위치 확인 버튼을 다시 눌러 주세요.")
    st.stop()

try:
    latitude = float(latitude)
    longitude = float(longitude)
except (ValueError, TypeError):
    st.error("GPS 좌표를 읽을 수 없습니다.")
    st.stop()

if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
    st.error("올바르지 않은 GPS 좌표입니다.")
    st.stop()

st.success("현재 위치를 확인했습니다.")

accuracy = location.get("accuracy")
if isinstance(accuracy, (int, float)):
    st.caption(f"위치 정확도 약 ±{accuracy:.0f}m")


# ---------------------------
# 3. 주변 위험 지도 데이터 검색
# ---------------------------
@st.cache_data(ttl=300)
def search_nearby(latitude, longitude):
    query = f"""
    [out:json][timeout:25];
    (
      nwr(around:500,{latitude},{longitude})["construction"];
      nwr(around:500,{latitude},{longitude})["highway"="steps"];
      nwr(around:500,{latitude},{longitude})["barrier"="construction"];
      nwr(around:500,{latitude},{longitude})
        ["highway"="footway"]["surface"~"gravel|unpaved"];
    );
    out center tags;
    """

    servers = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.private.coffee/api/interpreter",
    ]

    errors = []

    for server in servers:
        try:
            response = requests.post(
                server,
                data={"data": query},
                headers={
                    "User-Agent": "SafetyCompanion/1.0"
                },
                timeout=(10, 35),
            )

            response.raise_for_status()
            data = response.json()

            hazards = []
            seen = set()

            for element in data.get("elements", []):
                tags = element.get("tags", {})

                if "lat" in element and "lon" in element:
                    lat = element["lat"]
                    lon = element["lon"]
                else:
                    center = element.get("center", {})
                    lat = center.get("lat")
                    lon = center.get("lon")

                if lat is None or lon is None:
                    continue

                key = (element.get("type"), element.get("id"))
                if key in seen:
                    continue
                seen.add(key)

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
                    kind = "보행 주의 정보"

                hazards.append({
                    "lat": float(lat),
                    "lon": float(lon),
                    "kind": kind,
                    "name": tags.get("name", "이름 미등록"),
                })

            return hazards, None

        except (
            requests.RequestException,
            ValueError,
        ) as error:
            errors.append(f"{server}: {error}")

    return [], "\n".join(errors)


# ---------------------------
# 4. 검색 버튼
# ---------------------------
st.subheader("🚧 주변 500m 주의 요소")

if st.button(
    "🔎 주변 위험 정보 검색",
    type="primary",
    use_container_width=True,
):
    with st.spinner("주변 지도 데이터를 검색하고 있습니다..."):
        hazards, error = search_nearby(
            round(latitude, 5),
            round(longitude, 5),
        )

    if error:
        st.session_state["hazard_error"] = error
        st.session_state["hazards"] = []
        st.session_state["hazard_location"] = (
            round(latitude, 5),
            round(longitude, 5),
        )
    else:
        st.session_state["hazard_error"] = None
        st.session_state["hazards"] = hazards
        st.session_state["hazard_location"] = (
            round(latitude, 5),
            round(longitude, 5),
        )


# ---------------------------
# 5. 지도에 위치와 주의 요소 표시
# ---------------------------
st.subheader("🗺️ 내 주변 지도")

current_key = (round(latitude, 5), round(longitude, 5))

if st.session_state.get("hazard_location") != current_key:
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

# 현재 위치: 파란색 표식
folium.Marker(
    location=[latitude, longitude],
    tooltip="현재 위치",
    popup="내 현재 위치",
    icon=folium.Icon(
        color="blue",
        icon="user",
        prefix="fa",
    ),
).add_to(map_view)

# 현재 위치 기준 500m 범위
folium.Circle(
    location=[latitude, longitude],
    radius=500,
    color="blue",
    fill=True,
    fill_opacity=0.06,
    tooltip="검색 범위 약 500m",
).add_to(map_view)

# 주의 요소: 빨간색 표식
for hazard in hazards:
    folium.Marker(
        location=[hazard["lat"], hazard["lon"]],
        tooltip=hazard["kind"],
        popup=(
            f"{hazard['kind']}<br>"
            f"이름: {hazard['name']}"
        ),
        icon=folium.Icon(
            color="red",
            icon="exclamation-triangle",
            prefix="fa",
        ),
    ).add_to(map_view)

st_folium(
    map_view,
    height=520,
    use_container_width=True,
)

st.markdown("""
🔵 파란색: 현재 위치

🔴 빨간색: 지도 데이터에서 찾은 보행 주의 요소
""")

if search_error:
    st.error(
        "지도 위험 정보 서버에 연결하지 못했습니다. "
        "지도는 표시되지만 주의 요소는 불러오지 못했습니다."
    )
    st.caption("오류 정보")
    st.code(search_error)

elif hazards:
    st.warning(
        f"지도 데이터에서 주의 요소 {len(hazards)}개를 찾았습니다."
    )

    for item in hazards:
        st.markdown(
            f"- ⚠️ **{item['kind']}** — {item['name']}"
        )

elif st.session_state.get("hazard_location") == current_key:
    st.success("검색 조건에 맞는 지도 정보가 없습니다.")

st.divider()

st.caption(
    "안전 동행은 보행 보조용 시제품입니다. "
    "지도에 없는 위험이나 실시간 장애물을 감지하지 못하며, "
    "검색 결과가 없다고 안전한 것은 아닙니다."
)
