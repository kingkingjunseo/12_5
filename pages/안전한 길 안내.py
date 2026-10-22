
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="무장애 좌표 지도",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ 무장애 길 안내 지도")
st.caption("지도에서 위치를 선택하고 위도·경도를 확인하세요.")

# 초기 데이터
if "route_points" not in st.session_state:
    st.session_state.route_points = []

if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

if "point_role" not in st.session_state:
    st.session_state.point_role = "경유지"

st.markdown(
    """
    **사용 방법**
    1. 지도에서 원하는 위치를 클릭하세요.
    2. 선택한 위치의 위도와 경도를 확인하세요.
    3. 출발지, 도착지 또는 경유지로 추가하세요.
    """
)

# 지도 중심: 서울
points = st.session_state.route_points

if points:
    center = [points[-1]["lat"], points[-1]["lon"]]
else:
    center = [37.5665, 126.9780]

map_obj = folium.Map(
    location=center,
    zoom_start=13,
    control_scale=True,
    tiles="OpenStreetMap",
)

# 기존 지점 표시
for i, point in enumerate(points):
    if point["role"] == "출발지":
        color = "green"
    elif point["role"] == "도착지":
        color = "red"
    else:
        color = "blue"

    folium.Marker(
        location=[point["lat"], point["lon"]],
        tooltip=point["role"],
        popup=(
            f'{point["role"]}<br>'
            f'위도: {point["lat"]:.6f}<br>'
            f'경도: {point["lon"]:.6f}'
        ),
        icon=folium.Icon(color=color),
    ).add_to(map_obj)

# 지점이 두 개 이상이면 연결선 표시
if len(points) >= 2:
    folium.PolyLine(
        locations=[
            [point["lat"], point["lon"]]
            for point in points
        ],
        color="#16866a",
        weight=5,
        opacity=0.85,
        tooltip="직접 지정한 지점 연결선",
    ).add_to(map_obj)

map_result = st_folium(
    map_obj,
    height=500,
    use_container_width=True,
    key="coordinate_map",
)

# 지도 클릭 좌표 저장
if map_result and map_result.get("last_clicked"):
    location = map_result["last_clicked"]
    st.session_state.selected_location = {
        "lat": float(location["lat"]),
        "lon": float(location["lng"]),
    }

st.divider()
st.subheader("📍 선택한 좌표")

selected = st.session_state.selected_location

if selected:
    lat = selected["lat"]
    lon = selected["lon"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("위도 (Latitude)", f"{lat:.6f}")

    with col2:
        st.metric("경도 (Longitude)", f"{lon:.6f}")

    st.code(f"{lat:.6f}, {lon:.6f}", language="text")

    col1, col2 = st.columns([1, 1])

    with col1:
        role = st.selectbox(
            "이 위치의 종류",
            ["출발지", "경유지", "도착지"],
            key="selected_role",
        )

    with col2:
        label = st.text_input(
            "위치 이름 (선택)",
            placeholder="예: 학교 정문",
            key="selected_label",
        )

    if st.button("➕ 선택한 위치 추가", type="primary",
                 use_container_width=True):
        new_point = {
            "lat": lat,
            "lon": lon,
            "role": role,
            "label": label.strip() or role,
        }

        if role in ["출발지", "도착지"]:
            # 출발지와 도착지는 각각 하나씩 유지
            st.session_state.route_points = [
                p for p in st.session_state.route_points
                if p["role"] != role
            ]

        st.session_state.route_points.append(new_point)
        st.rerun()
else:
    st.info("위치를 선택하려면 위 지도를 클릭하세요.")

# 기록 목록
st.divider()
st.subheader("🧭 저장한 위치 목록")

points = st.session_state.route_points

if points:
    for index, point in enumerate(points):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**{point['role']} · {point['label']}**")
                st.text(
                    f"위도: {point['lat']:.6f} | "
                    f"경도: {point['lon']:.6f}"
                )

            with col2:
                if st.button(
                    "삭제",
                    key=f"delete_{index}",
                ):
                    st.session_state.route_points.pop(index)
                    st.rerun()

    if len(points) >= 2:
        st.success(
            f"{len(points)}개 지점을 지도에 표시하고 연결했어요."
        )
        st.caption(
            "연결선은 직접 지정한 지점을 직선으로 이은 것입니다. "
            "실제 도로를 따라가는 경로가 아닙니다."
        )

    coordinate_text = "\n".join(
        f"{p['label']}: 위도 {p['lat']:.6f}, "
        f"경도 {p['lon']:.6f}"
        for p in points
    )

    st.download_button(
        "📥 좌표 목록 다운로드",
        data=coordinate_text,
        file_name="coordinates.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.caption("아직 저장한 위치가 없어요.")

# 무장애 체크리스트
st.divider()
st.subheader("♿ 무장애 이동 점검")

check_items = [
    "보도에 턱이나 단차가 없는지 확인",
    "이용 가능한 경사로가 있는지 확인",
    "계단을 피할 수 있는지 확인",
    "보행로 폭과 장애물 확인",
    "횡단보도와 보행 신호 확인",
    "공사 및 통행 제한 여부 확인",
]

checked_items = []

for item in check_items:
    if st.checkbox(item, key=f"access_{item}"):
        checked_items.append(item)

st.progress(len(checked_items) / len(check_items))
st.write(f"확인 완료: {len(checked_items)} / {len(check_items)}개")

st.warning(
    "이 앱은 선택한 좌표와 지점 간 직선을 표시합니다. "
    "실제 도로 경로, 턱, 계단, 경사, 공사 여부를 자동 확인하지 않습니다. "
    "현장 정보를 별도로 확인해 주세요."
)

st.caption(
    "지도 배경: OpenStreetMap · 위치 좌표: 지도 클릭으로 선택"
)
