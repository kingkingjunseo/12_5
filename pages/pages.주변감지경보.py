
import io
import math
import struct
import wave

import requests
import streamlit as st
import folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="wide",
)

# 공개 Overpass API 서버를 순서대로 시도
SERVERS = [
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

DEFAULT_LAT = 37.5665
DEFAULT_LON = 126.9780


def search_hazards(lat, lon, radius):
    query = f"""
    [out:json][timeout:20];
    (
      nwr(around:{radius},{lat},{lon})["highway"="construction"];
      nwr(around:{radius},{lat},{lon})["construction"];
      nwr(around:{radius},{lat},{lon})["barrier"="construction"];
      nwr(around:{radius},{lat},{lon})["highway"="steps"];
      nwr(around:{radius},{lat},{lon})["natural"="cliff"];
      nwr(around:{radius},{lat},{lon})["hazard"];
      way(around:{radius},{lat},{lon})["incline"];
      way(around:{radius},{lat},{lon})
        ["highway"~"path|track"]
        ["smoothness"~"bad|very_bad|horrible|impassable"];
    );
    out center tags;
    """

    errors = []

    for server in SERVERS:
        try:
            response = requests.post(
                server,
                data={"data": query},
                headers={
                    "User-Agent": "SafeCompanion/1.0"
                },
                timeout=(8, 30),
            )

            if response.status_code != 200:
                errors.append(
                    f"{server}: HTTP {response.status_code}"
                )
                continue

            try:
                data = response.json()
            except ValueError:
                errors.append(f"{server}: JSON 응답 오류")
                continue

            if not isinstance(data.get("elements"), list):
                errors.append(f"{server}: 예상하지 못한 응답")
                continue

            return data["elements"], errors

        except requests.Timeout:
            errors.append(f"{server}: 시간 초과")
        except requests.RequestException as exc:
            errors.append(
                f"{server}: {type(exc).__name__}: {exc}"
            )

    raise RuntimeError("\n".join(errors))


def coordinates(item):
    if "lat" in item and "lon" in item:
        return item["lat"], item["lon"]

    center = item.get("center", {})
    if "lat" in center and "lon" in center:
        return center["lat"], center["lon"]

    return None


def hazard_type(tags):
    if (
        tags.get("highway") == "construction"
        or "construction" in tags
        or tags.get("barrier") == "construction"
    ):
        return "공사 구간"

    if tags.get("highway") == "steps":
        return "계단"

    if tags.get("natural") == "cliff":
        return "절벽"

    if tags.get("hazard"):
        return "위험 표시"

    if tags.get("incline"):
        return "경사 정보"

    if tags.get("smoothness"):
        return "노면 상태 주의"

    return "주의 구간"


def beep_audio():
    rate = 22050
    output = io.BytesIO()

    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)

        frames = bytearray()
        for i in range(int(rate * 0.4)):
            value = int(
                9000 * math.sin(2 * math.pi * 880 * i / rate)
            )
            frames.extend(struct.pack("<h", value))

        wav.writeframes(frames)

    return output.getvalue()


st.title("🚶 안전 동행")
st.subheader("어르신을 위한 주변 보행 안전 지도")
st.write(
    "주변의 공사 구간, 계단, 절벽, 경사 및 노면 상태 관련 "
    "지도 정보를 검색합니다."
)

with st.sidebar:
    st.header("📍 위치 설정")

    lat = st.number_input(
        "위도", min_value=-90.0, max_value=90.0,
        value=DEFAULT_LAT, format="%.6f",
    )
    lon = st.number_input(
        "경도", min_value=-180.0, max_value=180.0,
        value=DEFAULT_LON, format="%.6f",
    )
    radius = st.slider(
        "탐색 반경 (m)", 100, 2000, 500, 100
    )

    search_button = st.button(
        "주변 위험 요소 찾기",
        type="primary",
        use_container_width=True,
    )

    st.caption(
        "초기 위치는 서울의 예시 좌표입니다. "
        "GPS 자동 추적이 아니므로 실제 위치에 맞게 수정하세요."
    )

if "results" not in st.session_state:
    st.session_state.results = None
if "error" not in st.session_state:
    st.session_state.error = None
if "search_params" not in st.session_state:
    st.session_state.search_params = None

params = (lat, lon, radius)

if (
    search_button
    or st.session_state.search_params != params
):
    st.session_state.results = None
    st.session_state.error = None

    with st.spinner("주변 지도 데이터를 검색하고 있습니다..."):
        try:
            results, server_errors = search_hazards(
                float(lat), float(lon), int(radius)
            )
            st.session_state.results = results
            st.session_state.search_params = params

            if server_errors:
                st.info(
                    "일부 서버에는 연결할 수 없었지만 "
                    "다른 서버에서 응답을 받았습니다."
                )

        except RuntimeError as exc:
            st.session_state.error = str(exc)
            st.session_state.search_params = params

# 위험 데이터 조회가 실패해도 지도는 표시
map_obj = folium.Map(
    location=[lat, lon],
    zoom_start=16,
    tiles="OpenStreetMap",
)

folium.Marker(
    [lat, lon],
    tooltip="설정한 기준 위치",
    popup="입력한 기준 위치 (실제 GPS 위치와 다를 수 있음)",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(map_obj)

folium.Circle(
    [lat, lon],
    radius=radius,
    color="blue",
    fill=True,
    fill_opacity=0.05,
).add_to(map_obj)

hazards = []

if st.session_state.results is not None:
    for item in st.session_state.results:
        point = coordinates(item)
        if point is None:
            continue

        tags = item.get("tags", {})
        hazards.append({
            "lat": point[0],
            "lon": point[1],
            "type": hazard_type(tags),
            "name": tags.get("name", "이름 없는 지점"),
            "tags": tags,
        })

for item in hazards:
    folium.Marker(
        [item["lat"], item["lon"]],
        tooltip=f"⚠️ {item['type']}",
        popup=(
            f"위험 종류: {item['type']}<br>"
            f"이름: {item['name']}"
        ),
        icon=folium.Icon(color="red", icon="warning-sign"),
    ).add_to(map_obj)

left, right = st.columns([2, 1])

with left:
    st.subheader("🗺️ 주변 위험 지도")
    st_folium(
        map_obj,
        use_container_width=True,
        height=520,
        key="safety_map",
    )

with right:
    st.subheader("🚨 검색 결과")

    if st.session_state.error:
        st.error("위험 데이터를 불러오지 못했습니다.")
        st.code(st.session_state.error)
        st.info(
            "위 오류는 연결할 수 없었던 서버와 응답 상태를 보여줍니다. "
            "잠시 후 다시 시도해 주세요."
        )

    elif st.session_state.results is None:
        st.info("위치를 설정하고 검색 버튼을 눌러 주세요.")

    elif hazards:
        st.metric("발견한 지도 객체", len(hazards))
        st.warning(
            "위험 관련 지도 정보가 발견되었습니다. "
            "실제 현장 상황도 반드시 확인하세요."
        )

        if st.button("🔊 경고음 재생", use_container_width=True):
            st.audio(beep_audio(), format="audio/wav")

        for i, item in enumerate(hazards, 1):
            with st.expander(f"🔴 {i}. {item['type']}"):
                st.write(item["name"])
                st.caption(
                    f"{item['lat']:.5f}, {item['lon']:.5f}"
                )
                st.json(item["tags"])

    else:
        st.success("검색된 위험 관련 지도 정보가 없습니다.")
        st.caption(
            "이것은 주변에 위험이 없다는 의미가 아닙니다. "
            "지도에 등록되지 않은 위험 요소가 있을 수 있습니다."
        )

st.divider()
st.caption(
    "지도: OpenStreetMap | 위험 정보: 공개 Overpass API "
    "| 정보 누락이나 지연이 있을 수 있으며 안전을 보장하지 않습니다."
)
