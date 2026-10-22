
import io
import math
import wave
import struct

import requests
import streamlit as st
import folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="wide",
)

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

# 천안 오성고등학교 인근을 시작 위치로 사용하는 예시 좌표.
# 실제 위치와 다를 수 있으므로 앱에서 직접 수정할 수 있다.
DEFAULT_LAT = 36.82
DEFAULT_LON = 127.14


@st.cache_data(ttl=300, show_spinner=False)
def get_hazards(lat, lon, radius):
    """OpenStreetMap에서 주변 위험 관련 지도 데이터를 조회한다."""
    query = f"""
    [out:json][timeout:20];
    (
      way(around:{radius},{lat},{lon})["highway"="construction"];
      way(around:{radius},{lat},{lon})["construction"];
      way(around:{radius},{lat},{lon})["barrier"="construction"];
      way(around:{radius},{lat},{lon})["highway"="steps"];
      node(around:{radius},{lat},{lon})["highway"="steps"];
      way(around:{radius},{lat},{lon})["natural"="cliff"];
      way(around:{radius},{lat},{lon})["barrier"="cliff"];
      way(around:{radius},{lat},{lon})["highway"="path"]["smoothness"~"bad|very_bad|horrible|impassable"];
      way(around:{radius},{lat},{lon})["highway"="track"]["smoothness"~"bad|very_bad|horrible|impassable"];
      way(around:{radius},{lat},{lon})["incline"];
      node(around:{radius},{lat},{lon})["hazard"];
    );
    out center tags;
    """

    errors = []

    for endpoint in OVERPASS_URLS:
        try:
            response = requests.post(
                endpoint,
                data={"data": query},
                timeout=30,
                headers={"User-Agent": "SafeCompanionStreamlit/1.0"},
            )
            response.raise_for_status()
            payload = response.json()
            return payload.get("elements", [])
        except (requests.RequestException, ValueError) as exc:
            errors.append(str(exc))

    raise RuntimeError(
        "지도 데이터를 가져오지 못했습니다. 잠시 후 다시 시도해 주세요."
    )


def get_coordinates(element):
    """노드 또는 도로 중심점의 좌표를 반환한다."""
    if "lat" in element and "lon" in element:
        return element["lat"], element["lon"]

    center = element.get("center", {})
    if "lat" in center and "lon" in center:
        return center["lat"], center["lon"]

    return None


def classify_hazard(tags):
    """지도 태그를 사용자에게 이해하기 쉬운 위험 종류로 변환한다."""
    if (
        tags.get("highway") == "construction"
        or "construction" in tags
        or tags.get("barrier") == "construction"
    ):
        return "공사 구간"

    if tags.get("highway") == "steps":
        return "계단"

    if tags.get("natural") == "cliff" or tags.get("barrier") == "cliff":
        return "절벽"

    if tags.get("hazard"):
        return "위험 표시"

    if tags.get("incline"):
        return "경사 정보"

    if tags.get("smoothness"):
        return "노면 상태 주의"

    return "주의 구간"


def make_beep():
    """외부 음원 파일 없이 짧은 경고음을 WAV로 생성한다."""
    sample_rate = 22050
    duration = 0.45
    frequency = 880
    frames = bytearray()

    for i in range(int(sample_rate * duration)):
        sample = int(
            10000 * math.sin(2 * math.pi * frequency * i / sample_rate)
        )
        frames.extend(struct.pack("<h", sample))

    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(frames)

    return output.getvalue()


st.title("🚶 안전 동행")
st.subheader("어르신을 위한 주변 보행 안전 지도")
st.write(
    "주변의 공사 구간, 계단, 절벽, 경사 및 노면 상태 관련 "
    "지도 정보를 확인할 수 있습니다."
)

with st.sidebar:
    st.header("📍 탐색 설정")

    lat = st.number_input(
        "위도",
        min_value=-90.0,
        max_value=90.0,
        value=DEFAULT_LAT,
        format="%.6f",
    )
    lon = st.number_input(
        "경도",
        min_value=-180.0,
        max_value=180.0,
        value=DEFAULT_LON,
        format="%.6f",
    )
    radius = st.slider(
        "주변 탐색 거리 (m)",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
    )

    search_clicked = st.button(
        "주변 위험 요소 찾기",
        type="primary",
        use_container_width=True,
    )

    st.caption(
        "현재 좌표는 초기 예시값입니다. 실제 위치의 위도와 경도를 "
        "입력해 주세요. 자동 GPS 위치 추적 기능은 포함되어 있지 않습니다."
    )

if "hazards" not in st.session_state:
    st.session_state.hazards = None
if "search_error" not in st.session_state:
    st.session_state.search_error = None
if "last_search" not in st.session_state:
    st.session_state.last_search = None

if search_clicked or st.session_state.last_search is None:
    with st.spinner("주변 지도 데이터를 검색하고 있습니다..."):
        try:
            results = get_hazards(float(lat), float(lon), int(radius))
            st.session_state.hazards = results
            st.session_state.search_error = None
            st.session_state.last_search = (lat, lon, radius)
        except Exception as exc:
            st.session_state.search_error = str(exc)
            st.session_state.hazards = None
            st.session_state.last_search = (lat, lon, radius)

if st.session_state.search_error:
    st.error(st.session_state.search_error)
    st.info("인터넷 연결을 확인하거나 잠시 후 다시 검색해 주세요.")

hazards = st.session_state.hazards

if hazards is not None:
    valid_hazards = []

    for item in hazards:
        coords = get_coordinates(item)
        if coords is None:
            continue

        item_lat, item_lon = coords
        tags = item.get("tags", {})
        valid_hazards.append(
            {
                "lat": item_lat,
                "lon": item_lon,
                "type": classify_hazard(tags),
                "name": tags.get("name", "이름 없는 위험 지점"),
                "details": tags,
                "id": item.get("id"),
            }
        )

    left, right = st.columns([2, 1])

    with left:
        st.markdown("### 🗺️ 주변 위험 지도")

        map_view = folium.Map(
            location=[lat, lon],
            zoom_start=16,
            tiles="OpenStreetMap",
        )

        folium.Marker(
            [lat, lon],
            tooltip="설정한 기준 위치",
            popup="현재 탐색 기준 위치 (GPS로 확인된 위치가 아닐 수 있음)",
            icon=folium.Icon(color="blue", icon="user"),
        ).add_to(map_view)

        # 탐색 반경 표시
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            color="blue",
            fill=True,
            fill_opacity=0.06,
            tooltip=f"탐색 반경 {radius}m",
        ).add_to(map_view)

        for hazard in valid_hazards:
            folium.Marker(
                [hazard["lat"], hazard["lon"]],
                tooltip=f"⚠️ {hazard['type']}",
                popup=(
                    f"위험 종류: {hazard['type']}<br>"
                    f"이름: {hazard['name']}<br>"
                    f"지도 객체 ID: {hazard['id']}"
                ),
                icon=folium.Icon(color="red", icon="warning-sign"),
            ).add_to(map_view)

        st_folium(
            map_view,
            use_container_width=True,
            height=520,
            key="safety_map",
        )

    with right:
        st.markdown("### 🚨 탐색 결과")

        st.metric("발견한 위험 관련 지도 객체", len(valid_hazards))

        if valid_hazards:
            st.warning(
                "주변에서 위험 관련 지도 정보를 발견했습니다. "
                "실제 현장을 확인하고 안전하게 이동하세요."
            )

            if st.button("🔊 경고음 재생", use_container_width=True):
                st.audio(make_beep(), format="audio/wav")

            for index, hazard in enumerate(valid_hazards, start=1):
                with st.container(border=True):
                    st.markdown(f"**🔴 {index}. {hazard['type']}**")
                    st.write(hazard["name"])
                    st.caption(
                        f"위도 {hazard['lat']:.5f}, "
                        f"경도 {hazard['lon']:.5f}"
                    )

                    if hazard["details"]:
                        with st.expander("지도 세부 정보"):
                            st.json(hazard["details"])
        else:
            st.success(
                "검색된 위험 관련 지도 정보가 없습니다. "
                "위험이 없다는 뜻은 아니므로 주변을 계속 살펴보세요."
            )

    st.caption(
        "데이터 출처: OpenStreetMap 및 Overpass API. "
        "정보 누락, 오래된 데이터, 위치 오차가 있을 수 있습니다. "
        "이 앱은 실시간 현장 감지나 안전을 보장하지 않습니다."
    )
