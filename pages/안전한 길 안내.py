import streamlit as st
import openrouteservice
from openrouteservice import convert
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="무장애 안전 경로 안내", page_icon="♿", layout="wide")

st.title("♿ 무장애 안전 경로 안내")
st.write("장소를 검색하고 휠체어 경로 프로필로 경로를 계산하는 웹 앱입니다.")

st.warning(
    "경로는 OpenStreetMap 기반 데이터로 계산됩니다. 실제 보도 턱, 임시 공사, "
    "엘리베이터 고장 등 모든 현장 상황을 보장하지 않으므로 이동 전 주변 상황을 확인하세요."
)

api_key = None
try:
    api_key = st.secrets.get("ORS_API_KEY")
except Exception:
    api_key = None

if not api_key:
    st.error("OpenRouteService API 키가 아직 설정되지 않았어요. 아래 설정 방법을 먼저 완료해 주세요.")
    st.markdown(
        "1. OpenRouteService 계정을 만들고 API 키를 발급받으세요: "
        "[API 키 발급 사이트](https://openrouteservice.org/dev/#/signup)\\n"
        "2. Streamlit Cloud에서 앱의 **Settings → Secrets**를 여세요.\\n"
        "3. 아래 한 줄을 추가하고 저장한 뒤 앱을 재실행하세요."
    )
    st.code('ORS_API_KEY = "여기에_발급받은_API_키"')
    st.stop()

with st.form("route_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_text = st.text_input("출발지", placeholder="예: 서울시청")
    with col2:
        end_text = st.text_input("도착지", placeholder="예: 경복궁")

    st.caption("장소 이름이나 주소를 입력하세요. 한국 내 장소를 권장합니다.")
    avoid_steps = st.checkbox("계단 회피 우선", value=True)
    max_incline = st.slider("허용할 최대 경사도(도)", min_value=3, max_value=15, value=6)
    submitted = st.form_submit_button("무장애 경로 찾기", type="primary")

if submitted:
    if not start_text.strip() or not end_text.strip():
        st.error("출발지와 도착지를 모두 입력해 주세요.")
        st.stop()

    client = openrouteservice.Client(key=api_key, timeout=30)

    try:
        with st.spinner("장소를 검색하고 경로를 계산하고 있어요..."):
            start_result = client.pelias_search(text=start_text.strip(), size=1)
            end_result = client.pelias_search(text=end_text.strip(), size=1)

            if not start_result.get("features") or not end_result.get("features"):
                st.error("장소를 찾지 못했어요. 더 구체적인 주소나 장소 이름으로 다시 검색해 주세요.")
                st.stop()

            start_feature = start_result["features"][0]
            end_feature = end_result["features"][0]
            start_lon, start_lat = start_feature["geometry"]["coordinates"][:2]
            end_lon, end_lat = end_feature["geometry"]["coordinates"][:2]
            start_label = start_feature.get("properties", {}).get("label", start_text)
            end_label = end_feature.get("properties", {}).get("label", end_text)

            options = {}
            if avoid_steps:
                options["avoid_features"] = ["steps"]
            options["profile_params"] = {
                "restrictions": {
                    "maximum_incline": int(max_incline)
                }
            }

            route = client.directions(
                coordinates=((start_lon, start_lat), (end_lon, end_lat)),
                profile="wheelchair",
                format="json",
                instructions=True,
                language="ko",
                units="m",
                options=options,
            )

        route_data = route["routes"][0]
        geometry = convert.decode_polyline(route_data["geometry"])
        route_coords = geometry["coordinates"]  # [longitude, latitude]

        st.success("경로 계산이 완료됐어요.")
        metric1, metric2 = st.columns(2)
        metric1.metric("경로 거리", f'{route_data["summary"]["distance"] / 1000:.2f} km')
        metric2.metric("예상 소요 시간", f'{max(1, round(route_data["summary"]["duration"] / 60))}분')

        map_center = [(start_lat + end_lat) / 2, (start_lon + end_lon) / 2]
        route_map = folium.Map(location=map_center, zoom_start=14, control_scale=True)
        folium.Marker(
            [start_lat, start_lon],
            tooltip="출발지",
            popup=start_label,
            icon=folium.Icon(color="green", icon="play"),
        ).add_to(route_map)
        folium.Marker(
            [end_lat, end_lon],
            tooltip="도착지",
            popup=end_label,
            icon=folium.Icon(color="red", icon="flag"),
        ).add_to(route_map)
        folium.PolyLine(
            locations=[[lat, lon] for lon, lat in route_coords],
            tooltip="계산된 휠체어 경로",
            weight=6,
        ).add_to(route_map)

        min_lat = min([lat for lon, lat in route_coords])
        max_lat = max([lat for lon, lat in route_coords])
        min_lon = min([lon for lon, lat in route_coords])
        max_lon = max([lon for lon, lat in route_coords])
        route_map.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

        st.subheader("지도")
        st_folium(route_map, use_container_width=True, height=520)

        st.subheader("이동 안내")
        for segment in route_data.get("segments", []):
            for step in segment.get("steps", []):
                instruction = step.get("instruction")
                if instruction:
                    distance = step.get("distance", 0)
                    st.write(f"- {instruction} ({distance:.0f} m)")

        st.caption(
            "주의: '휠체어 경로'는 데이터베이스에 기록된 도로 특성을 바탕으로 계산한 결과입니다. "
            "실제 경사, 턱, 공사, 통행 가능 여부가 완전히 반영되지 않을 수 있습니다."
        )

    except openrouteservice.exceptions.ApiError as exc:
        st.error("경로 API에서 오류가 반환됐어요. API 키, 사용량 제한, 입력한 장소를 확인해 주세요.")
        st.code(str(exc))
    except Exception as exc:
        st.error("요청을 처리하지 못했어요. 잠시 후 다시 시도해 주세요.")
        st.code(str(exc))

else:
    st.info("출발지와 도착지를 입력한 뒤 '무장애 경로 찾기'를 눌러 주세요.")
    st.markdown("### 작동 방식")
    st.write("1. 장소 이름을 좌표로 검색합니다.")
    st.write("2. 휠체어 경로 프로필로 경로를 요청합니다.")
    st.write("3. 지도와 이동 안내를 표시합니다.")
    st.write("실제 경로 계산에는 API 키와 인터넷 연결이 필요합니다.")
