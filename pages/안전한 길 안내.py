
import streamlit as st
import folium
import openrouteservice
from openrouteservice import convert
from streamlit_folium import st_folium

st.set_page_config(
    page_title="안전한 길 안내",
    page_icon="♿",
    layout="wide",
)

st.markdown("""
<style>
.block-container {padding-top: 1rem; max-width: 1600px;}
header {visibility: visible;}
.hero {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(110deg, #e8f1ff, #f7fbff);
    border: 1px solid #d6e5ff;
    margin-bottom: 18px;
}
.hero h1 {color: #174581; font-size: 30px; margin: 0;}
.hero p {color: #526b8b; margin-bottom: 0;}
.panel-title {
    font-size: 20px;
    font-weight: 750;
    color: #174581;
    margin: 8px 0 16px 0;
}
.metric {
    background: #f1f6ff;
    border: 1px solid #dce8fa;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}
.metric-label {font-size: 13px; color: #647995;}
.metric-value {font-size: 22px; font-weight: 800; color: #174581;}
.safe {
    background: #e9f8ef;
    color: #087443;
    border-radius: 10px;
    padding: 12px;
    margin: 10px 0;
}
</style>

<div class="hero">
    <h1>♿ 안전한 길 안내</h1>
    <p>장애물을 피하고, 모두가 편리한 길을 찾아드립니다.</p>
</div>
""", unsafe_allow_html=True)

try:
    api_key = st.secrets.get("ORS_API_KEY", "")
except Exception:
    api_key = ""

left, center, right = st.columns([1, 1.7, 1.1], gap="medium")

with left:
    st.markdown('<div class="panel-title">📍 출발지 · 도착지</div>',
                unsafe_allow_html=True)

    with st.form("route_form"):
        start = st.text_input("🟢 출발지", "서울역")
        end = st.text_input("🔴 도착지", "서울시청")

        st.markdown("### 🛡️ 안전 경로 설정")
        wheelchair = st.checkbox("휠체어 이동 우선", value=True)
        avoid_steps = st.checkbox("계단 회피 우선", value=True)
        curb_check = st.checkbox("보도 턱 정보 확인", value=True)
        incline_limit = st.checkbox("경사도 제한 사용", value=False)
        max_incline = st.slider(
            "허용 경사도(도)", 3, 15, 6,
            disabled=not incline_limit
        )

        submitted = st.form_submit_button(
            "🔎 안전 경로 찾기",
            type="primary",
            use_container_width=True,
        )

    st.caption("지도 정보가 실제 현장과 다를 수 있으므로 이동 전 확인하세요.")

with center:
    st.markdown('<div class="panel-title">🗺️ 경로 지도</div>',
                unsafe_allow_html=True)
    map_area = st.empty()

with right:
    st.markdown('<div class="panel-title">🧭 경로 정보</div>',
                unsafe_allow_html=True)
    details = st.empty()


def make_map(start_point=None, end_point=None, route_points=None):
    m = folium.Map(
        location=[37.5665, 126.9780],
        zoom_start=13,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    if start_point:
        folium.Marker(
            start_point,
            tooltip="출발지",
            icon=folium.Icon(color="green", icon="play"),
        ).add_to(m)

    if end_point:
        folium.Marker(
            end_point,
            tooltip="도착지",
            icon=folium.Icon(color="red", icon="flag"),
        ).add_to(m)

    if route_points:
        folium.PolyLine(
            route_points,
            color="#246be8",
            weight=6,
            opacity=0.9,
            tooltip="계산된 경로",
        ).add_to(m)

        m.fit_bounds(route_points, padding=(25, 25))

    return m


if "route_result" not in st.session_state:
    with map_area:
        st_folium(
            make_map(),
            use_container_width=True,
            height=650,
            returned_objects=[],
            key="initial_map",
        )

    with details:
        st.info("출발지와 도착지를 입력한 뒤 경로를 검색하세요.")
        st.markdown("**주요 확인 항목**")
        st.write("🟢 계단 회피")
        st.write("🟠 보도 턱 확인")
        st.write("🟣 공사 및 장애물 확인")

if submitted:
    if not start.strip() or not end.strip():
        st.error("출발지와 도착지를 모두 입력해 주세요.")

    elif not api_key:
        st.error("OpenRouteService API 키를 먼저 설정해 주세요.")
        st.code('ORS_API_KEY = "발급받은_API_키"')
        st.markdown(
            "[API 키 발급 사이트](https://openrouteservice.org/dev/#/signup)"
        )

    else:
        try:
            client = openrouteservice.Client(
                key=api_key,
                timeout=30,
            )

            with st.spinner("장소 검색 및 경로 계산 중..."):
                origin = client.pelias_search(
                    text=start.strip(),
                    size=1,
                )
                destination = client.pelias_search(
                    text=end.strip(),
                    size=1,
                )

                if not origin.get("features") or not destination.get("features"):
                    st.error("장소를 찾지 못했습니다. 주소를 더 구체적으로 입력해 주세요.")
                    st.stop()

                sf = origin["features"][0]
                ef = destination["features"][0]

                slon, slat = sf["geometry"]["coordinates"][:2]
                elon, elat = ef["geometry"]["coordinates"][:2]

                options = {}

                if avoid_steps and not wheelchair:
                    options["avoid_features"] = ["steps"]

                if incline_limit and wheelchair:
                    options["profile_params"] = {
                        "restrictions": {
                            "maximum_incline": int(max_incline)
                        }
                    }

                profile = (
                    "wheelchair"
                    if wheelchair
                    else "foot-walking"
                )

                route = client.directions(
                    coordinates=((slon, slat), (elon, elat)),
                    profile=profile,
                    format="json",
                    instructions=True,
                    language="ko",
                    units="m",
                    options=options or None,
                )

            route_data = route["routes"][0]
            decoded = convert.decode_polyline(route_data["geometry"])

            points = [
                (lat, lon)
                for lon, lat in decoded["coordinates"]
            ]

            summary = route_data["summary"]

            st.session_state["route_result"] = {
                "start": sf.get("properties", {}).get("label", start),
                "end": ef.get("properties", {}).get("label", end),
                "start_point": (slat, slon),
                "end_point": (elat, elon),
                "points": points,
                "distance": summary["distance"] / 1000,
                "minutes": round(summary["duration"] / 60),
                "segments": route_data.get("segments", []),
                "wheelchair": wheelchair,
                "curb_check": curb_check,
                "avoid_steps": avoid_steps,
            }

        except openrouteservice.exceptions.ApiError as exc:
            st.error("경로 API 오류입니다. API 키와 사용량을 확인해 주세요.")
            st.code(str(exc))

        except Exception as exc:
            st.error("경로 계산 중 문제가 발생했습니다.")
            st.code(str(exc))


result = st.session_state.get("route_result")

if result:
    with center:
        st.markdown("### 추천 경로")

        st_folium(
            make_map(
                start_point=result["start_point"],
                end_point=result["end_point"],
                route_points=result["points"],
            ),
            use_container_width=True,
            height=650,
            returned_objects=[],
            key="route_map",
        )

    with right:
        a, b = st.columns(2)

        with a:
            st.markdown(
                f'<div class="metric">'
                f'<div class="metric-label">총 거리</div>'
                f'<div class="metric-value">{result["distance"]:.2f} km</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with b:
            st.markdown(
                f'<div class="metric">'
                f'<div class="metric-label">예상 시간</div>'
                f'<div class="metric-value">약 {result["minutes"]}분</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="safe">✓ 경로 계산 완료</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**출발지**")
        st.write("🟢 " + result["start"])

        st.markdown("**도착지**")
        st.write("🔴 " + result["end"])

        st.divider()
        st.markdown("### 🧭 경로 안내")

        count = 0
        for segment in result["segments"]:
            for step in segment.get("steps", []):
                instruction = step.get("instruction", "")
                if instruction:
                    st.write(
                        f"• {instruction} "
                        f"({step.get('distance', 0):.0f}m)"
                    )
                    count += 1

                if count >= 12:
                    break

            if count >= 12:
                break

        if count == 0:
            st.write("세부 안내 정보가 없습니다.")

        st.divider()
        st.markdown("### ⚠️ 안전 확인")

        if result["avoid_steps"]:
            st.write("✓ 계단 회피 옵션 요청")

        if result["wheelchair"]:
            st.write("✓ 휠체어 경로 프로필 사용")

        if result["curb_check"]:
            st.warning(
                "보도 턱 정보가 모든 구간에 제공되는 것은 아닙니다."
            )

        st.caption(
            "실제 공사, 보도 턱, 엘리베이터 고장 등은 "
            "완전히 반영되지 않을 수 있습니다. 현장 상황을 확인하세요."
        )
