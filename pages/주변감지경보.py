
import io
import math
import struct
import wave

import requests
import streamlit as st
import folium
from streamlit_folium import st_folium


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="wide",
)

SCHOOL_NAME = "천안오성고등학교"
SCHOOL_ADDRESS = "충남 천안시 서북구 과수원길 27"

# 천안오성고등학교 고정 좌표
SCHOOL_LAT = 36.84152810
SCHOOL_LON = 127.14213325

OVERPASS_SERVERS = [
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]


# -----------------------------
# 주변 위험 데이터 조회
# -----------------------------
@st.cache_data(ttl=180, show_spinner=False)
def fetch_hazards(lat, lon, radius):
    query = f"""
    [out:json][timeout:25];
    (
      nwr(around:{radius},{lat},{lon})["highway"="construction"];
      nwr(around:{radius},{lat},{lon})["construction"];
      nwr(around:{radius},{lat},{lon})["barrier"="construction"];
      nwr(around:{radius},{lat},{lon})["highway"="steps"];
      nwr(around:{radius},{lat},{lon})["natural"="cliff"];
      nwr(around:{radius},{lat},{lon})["barrier"="cliff"];
      nwr(around:{radius},{lat},{lon})["hazard"];
      way(around:{radius},{lat},{lon})["incline"];
      way(around:{radius},{lat},{lon})
        ["highway"~"path|track"]
        ["smoothness"~"bad|very_bad|horrible|impassable"];
    );
    out center tags;
    """

    errors = []

    for server in OVERPASS_SERVERS:
        try:
            response = requests.post(
                server,
                data={"data": query},
                timeout=(8, 35),
                headers={
                    "User-Agent": "SafetyCompanion/1.0"
                },
            )

            if response.status_code != 200:
                errors.append(
                    f"{server} → HTTP {response.status_code}"
                )
                continue

            try:
                payload = response.json()
            except ValueError:
                errors.append(f"{server} → JSON 응답 오류")
                continue

            if not isinstance(payload.get("elements"), list):
                errors.append(f"{server} → 응답 데이터 형식 오류")
                continue

            return payload["elements"]

        except requests.Timeout:
            errors.append(f"{server} → 연결 시간 초과")
        except requests.RequestException as exc:
            errors.append(
                f"{server} → {type(exc).__name__}: {exc}"
            )

    raise RuntimeError(
        "모든 지도 데이터 서버에 연결하지 못했습니다.\n\n"
        + "\n".join(errors)
    )


# -----------------------------
# 위험 종류 분류
# -----------------------------
def classify_hazard(tags):
    if (
        tags.get("highway") == "construction"
        or "construction" in tags
        or tags.get("barrier") == "construction"
    ):
        return "공사 구간"

    if tags.get("highway") == "steps":
        return "계단"

    if (
        tags.get("natural") == "cliff"
        or tags.get("barrier") == "cliff"
    ):
        return "절벽"

    if tags.get("hazard"):
        return "위험 표시"

    if tags.get("incline"):
        return "경사 정보"

    if tags.get("smoothness"):
        return "노면 상태 주의"

    return "주의 구간"


def get_coordinates(item):
    if "lat" in item and "lon" in item:
        return item["lat"], item["lon"]

    center = item.get("center", {})
    if "lat" in center and "lon" in center:
        return center["lat"], center["lon"]

    return None


# -----------------------------
# 경고음 생성
# -----------------------------
def create_warning_sound():
    sample_rate = 22050
    output = io.BytesIO()
    frames = bytearray()

    # 두 번의 짧은 경고음
    for frequency, duration in [(880, 0.25), (660, 0.25)]:
        count = int(sample_rate * duration)

        for i in range(count):
            value = int(
                10000
                * math.sin(2 * math.pi * frequency * i / sample_rate)
            )
            frames.extend(struct.pack("<h", value))

    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(frames)

    return output.getvalue()


# -----------------------------
# 화면
# -----------------------------
st.title("🚶 안전 동행")
st.subheader("어르신을 위한 주변 보행 안전 지도")

st.markdown(
    """
    공사 구간, 계단, 절벽, 경사 및 노면 상태와 관련된
    주변 지도 정보를 확인할 수 있습니다.
    """
)

st.info(
    f"📍 탐색 기준 위치: **{SCHOOL_NAME}**\n\n"
    f"주소: {SCHOOL_ADDRESS}\n\n"
    "위치는 학교로 고정되어 있으며 실제 GPS 위치를 추적하지 않습니다."
)

with st.sidebar:
    st.header("🗺️ 탐색 설정")

    radius = st.slider(
        "주변 탐색 거리",
        min_value=200,
        max_value=2000,
        value=1000,
        step=200,
        format="%d m",
    )

    search_button = st.button(
        "🔎 주변 위험 요소 찾기",
        type="primary",
        use_container_width=True,
    )

    st.caption(
        "위험 정보는 공개 지도 데이터에 등록된 내용만 검색합니다."
    )


# 최초 실행 시 검색하고, 버튼을 누르면 다시 검색
if "hazards" not in st.session_state:
    st.session_state.hazards = None

if "search_error" not in st.session_state:
    st.session_state.search_error = None

if "last_radius" not in st.session_state:
    st.session_state.last_radius = None

if (
    st.session_state.hazards is None
    and st.session_state.search_error is None
) or search_button or st.session_state.last_radius != radius:

    st.session_state.hazards = None
    st.session_state.search_error = None
    st.session_state.last_radius = radius

    with st.spinner("주변 위험 정보를 조회하고 있습니다..."):
        try:
            st.session_state.hazards = fetch_hazards(
                SCHOOL_LAT,
                SCHOOL_LON,
                radius,
            )
        except Exception as exc:
            st.session_state.search_error = str(exc)


# 지도 생성: 데이터 검색 실패와 관계없이 표시
map_view = folium.Map(
    location=[SCHOOL_LAT, SCHOOL_LON],
    zoom_start=16,
    tiles="OpenStreetMap",
)

folium.Marker(
    [SCHOOL_LAT, SCHOOL_LON],
    tooltip=SCHOOL_NAME,
    popup=f"{SCHOOL_NAME}<br>{SCHOOL_ADDRESS}",
    icon=folium.Icon(color="blue", icon="home"),
).add_to(map_view)

folium.Circle(
    location=[SCHOOL_LAT, SCHOOL_LON],
    radius=radius,
    color="blue",
    fill=True,
    fill_opacity=0.06,
    tooltip=f"탐색 반경 {radius}m",
).add_to(map_view)


# 검색 결과를 지도에 표시
hazards = []

if st.session_state.hazards is not None:
    for item in st.session_state.hazards:
        point = get_coordinates(item)

        if point is None:
            continue

        tags = item.get("tags", {})

        hazards.append({
            "lat": point[0],
            "lon": point[1],
            "type": classify_hazard(tags),
            "name": tags.get("name", "이름 없는 위험 지점"),
            "tags": tags,
        })

for hazard in hazards:
    popup_text = (
        f"위험 종류: {hazard['type']}<br>"
        f"이름: {hazard['name']}"
    )

    folium.Marker(
        [hazard["lat"], hazard["lon"]],
        tooltip=f"🔴 {hazard['type']}",
        popup=popup_text,
        icon=folium.Icon(
            color="red",
            icon="warning-sign",
        ),
    ).add_to(map_view)


# 화면 배치
map_column, result_column = st.columns([2, 1])

with map_column:
    st.markdown("### 🗺️ 주변 위험 지도")

    st_folium(
        map_view,
        use_container_width=True,
        height=520,
        key="fixed_school_safety_map",
    )

with result_column:
    st.markdown("### 🚨 위험 감지 결과")

    if st.session_state.search_error:
        st.error("위험 데이터를 불러오지 못했습니다.")

        with st.expander("오류 원인 확인", expanded=True):
            st.code(st.session_state.search_error)

        st.caption(
            "인터넷 연결 또는 공개 데이터 서버 상태를 확인한 후 "
            "다시 검색해 주세요."
        )

    elif st.session_state.hazards is None:
        st.info("위험 정보를 검색해 주세요.")

    elif hazards:
        st.metric("검색된 위험 지점", len(hazards))

        st.warning(
            "주변에 위험 관련 지도 정보가 있습니다. "
            "이동 전 현장을 확인하세요."
        )

        if st.button(
            "🔊 경고음 재생",
            type="primary",
            use_container_width=True,
        ):
            st.audio(
                create_warning_sound(),
                format="audio/wav",
                autoplay=True,
            )

        for index, hazard in enumerate(hazards, start=1):
            with st.expander(
                f"🔴 {index}. {hazard['type']}"
            ):
                st.write(hazard["name"])
                st.caption(
                    f"위도: {hazard['lat']:.6f}\n\n"
                    f"경도: {hazard['lon']:.6f}"
                )

                if hazard["tags"]:
                    st.json(hazard["tags"])

    else:
        st.success("등록된 위험 관련 지도 정보를 찾지 못했습니다.")
        st.caption(
            "주변에 실제 위험이 없다는 뜻은 아닙니다. "
            "지도에 등록되지 않은 위험 요소가 있을 수 있습니다."
        )

st.divider()

st.caption(
    "지도 출처: OpenStreetMap | 위험 데이터: Overpass API. "
    "데이터가 누락되거나 오래되었을 수 있습니다. "
    "이 앱은 실시간 현장 감지나 안전을 보장하지 않습니다."
)
