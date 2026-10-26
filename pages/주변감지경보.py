
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

# 고정 위치: 내부 계산용
LAT = 36.84152810
LON = 127.14213325

SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]


@st.cache_data(ttl=180, show_spinner=False)
def get_hazards(lat, lon, radius):
    query = f"""
    [out:json][timeout:20];
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

    for server in SERVERS:
        try:
            response = requests.post(
                server,
                data={"data": query},
                timeout=(8, 30),
                headers={"User-Agent": "SafetyCompanion/1.0"},
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data.get("elements"), list):
                return data["elements"]

            errors.append(f"응답 형식 오류: HTTP {response.status_code}")

        except requests.Timeout:
            errors.append("서버 응답 시간 초과")
        except requests.RequestException as exc:
            errors.append(f"서버 연결 오류: {exc}")
        except ValueError:
            errors.append("서버 응답을 해석할 수 없습니다.")

    raise RuntimeError("\n".join(errors))


def get_point(item):
    if "lat" in item and "lon" in item:
        return item["lat"], item["lon"]

    center = item.get("center", {})
    if "lat" in center and "lon" in center:
        return center["lat"], center["lon"]

    return None


def classify(tags):
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
    rate = 22050
    audio = io.BytesIO()
    frames = bytearray()

    for frequency in (880, 660):
        for i in range(int(rate * 0.25)):
            sample = int(
                9000 * math.sin(2 * math.pi * frequency * i / rate)
            )
            frames.extend(struct.pack("<h", sample))

    with wave.open(audio, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(frames)

    return audio.getvalue()


st.title("🚶 안전 동행")
st.subheader("어르신을 위한 주변 보행 안전 지도")
st.write(
    "주변의 공사 구간, 계단, 절벽, 경사 및 노면 상태 관련 "
    "지도 정보를 확인할 수 있습니다."
)
st.info("📍 현재 위치를 기준으로 주변 보행 안전 정보를 확인합니다.")

with st.sidebar:
    st.header("탐색 설정")
    radius = st.slider("주변 탐색 거리 (m)", 200, 2000, 1000, 200)
    search = st.button(
        "주변 위험 요소 찾기",
        type="primary",
        use_container_width=True,
    )

if "results" not in st.session_state:
    st.session_state.results = None
if "error" not in st.session_state:
    st.session_state.error = None
if "last_radius" not in st.session_state:
    st.session_state.last_radius = None

if (
    st.session_state.results is None
    and st.session_state.error is None
) or search or st.session_state.last_radius != radius:
    st.session_state.results = None
    st.session_state.error = None
    st.session_state.last_radius = radius

    with st.spinner("주변 위험 정보를 검색하고 있습니다..."):
        try:
            st.session_state.results = get_hazards(LAT, LON, radius)
        except RuntimeError as exc:
            st.session_state.error = str(exc)

map_view = folium.Map(
    location=[LAT, LON],
    zoom_start=16,
    tiles="OpenStreetMap",
)

folium.Marker(
    [LAT, LON],
    tooltip="현재 위치",
    popup="현재 위치",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(map_view)

folium.Circle(
    [LAT, LON],
    radius=radius,
    color="blue",
    fill=True,
    fill_opacity=0.05,
).add_to(map_view)

hazards = []

if st.session_state.results is not None:
    for item in st.session_state.results:
        point = get_point(item)
        if point is None:
            continue

        tags = item.get("tags", {})
        hazard = {
            "lat": point[0],
            "lon": point[1],
            "type": classify(tags),
            "name": tags.get("name", "이름 없는 위험 지점"),
            "tags": tags,
        }
        hazards.append(hazard)

        folium.Marker(
            point,
            tooltip=f"⚠️ {hazard['type']}",
            popup=f"위험 종류: {hazard['type']}",
            icon=folium.Icon(color="red", icon="warning-sign"),
        ).add_to(map_view)

left, right = st.columns([2, 1])

with left:
    st.subheader("🗺️ 주변 위험 지도")
    st_folium(
        map_view,
        use_container_width=True,
        height=520,
        key="safety_map",
    )

with right:
    st.subheader("🚨 탐색 결과")

    if st.session_state.error:
        st.error("위험 데이터를 불러오지 못했습니다.")
        st.code(st.session_state.error)

    elif st.session_state.results is None:
        st.info("위험 정보를 검색해 주세요.")

    elif hazards:
        st.metric("검색된 위험 지점", len(hazards))
        st.warning("위험 관련 지도 정보가 발견되었습니다.")

        if st.button("🔊 경고음 재생", use_container_width=True):
            st.audio(make_beep(), format="audio/wav", autoplay=True)

        for index, hazard in enumerate(hazards, 1):
            with st.expander(f"🔴 {index}. {hazard['type']}"):
                st.write(hazard["name"])
                st.json(hazard["tags"])

    else:
        st.success("등록된 위험 관련 지도 정보가 없습니다.")
        st.caption("위험 정보가 없다는 것이 실제로 안전하다는 뜻은 아닙니다.")

st.divider()
st.caption(
    "지도: OpenStreetMap · 위험 정보: 공개 지도 데이터. "
    "정보 누락이나 지연이 있을 수 있습니다."
)
