
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

# 실제 도로를 따라 보행 경로 계산
import osmnx as ox
import networkx as nx
import folium
import streamlit as st
from streamlit_folium import st_folium

st.subheader("🚶 실제 도로 경로 찾기")

start = st.session_state.get("safe_start")
end = st.session_state.get("safe_end")


    except (nx.NetworkXNoPath, nx.NodeNotFound):
        st.error("두 위치를 연결하는 도로 경로를 찾지 못했어요.")
    except Exception as e:
        st.error(f"경로 계산에 실패했어요: {e}")

# 실제 도로를 따라가는 보행 경로
import osmnx as ox
import networkx as nx

st.divider()
st.subheader("🚶 실제 도로를 따라가는 경로")

points = st.session_state.route_points

starts = [p for p in points if p["role"] == "출발지"]
ends = [p for p in points if p["role"] == "도착지"]

if not starts or not ends:
    st.info("지도에서 출발지와 도착지를 각각 추가해 주세요.")

elif st.button("🗺️ 실제 도로 경로 찾기", type="primary"):
    start = starts[0]
    end = ends[0]

    try:
        from math import radians, sin, cos, asin, sqrt

        lat1, lon1 = radians(start["lat"]), radians(start["lon"])
        lat2, lon2 = radians(end["lat"]), radians(end["lon"])

        a = (
            sin((lat2 - lat1) / 2) ** 2
            + cos(lat1) * cos(lat2)
            * sin((lon2 - lon1) / 2) ** 2
        )
        distance = 6371000 * 2 * asin(sqrt(a))

        # 경로가 길수록 더 넓은 도로 검색 범위 사용
        radius = max(2000, min(distance * 1.5 + 1000, 15000))
        center = (
            (start["lat"] + end["lat"]) / 2,
            (start["lon"] + end["lon"]) / 2,
        )

        with st.spinner("보행 도로 데이터를 가져오는 중..."):
            G = ox.graph.graph_from_point(
                center,
                dist=radius,
                network_type="walk",
                simplify=True,
            )

        with st.spinner("도로를 따라 경로를 계산하는 중..."):
            source = ox.distance.nearest_nodes(
                G, X=start["lon"], Y=start["lat"]
            )
            target = ox.distance.nearest_nodes(
                G, X=end["lon"], Y=end["lat"]
            )

            route = nx.shortest_path(
                G, source, target, weight="length"
            )

            route_coords = [
                (G.nodes[n]["y"], G.nodes[n]["x"])
                for n in route
            ]

            # 도로의 실제 형상 좌표까지 포함해 표시
            route_line = ox.routing.route_to_gdf(
                G, route, weight="length"
            )

            route_coords = []
            for _, row in route_line.iterrows():
                geom = row.geometry
                coords = list(geom.coords)

                # 도로 좌표는 (경도, 위도) 순서
                segment = [(y, x) for x, y in coords]

                if route_coords and segment:
                    if route_coords[-1] == segment[0]:
                        segment = segment[1:]

                route_coords.extend(segment)

            total_m = sum(
                data.get("length", 0)
                for u, v in zip(route[:-1], route[1:])
                for data in [min(
                    G[u][v].values(),
                    key=lambda d: d.get("length", float("inf"))
                )]
            )

        route_map = folium.Map(
            location=route_coords[len(route_coords) // 2],
            zoom_start=16,
            tiles="OpenStreetMap",
        )

        folium.PolyLine(
            route_coords,
            color="#16866a",
            weight=7,
            opacity=0.9,
            tooltip="실제 보행 도로 경로",
        ).add_to(route_map)

        folium.Marker(
            [start["lat"], start["lon"]],
            tooltip="출발지",
            icon=folium.Icon(color="green"),
        ).add_to(route_map)

        folium.Marker(
            [end["lat"], end["lon"]],
            tooltip="도착지",
            icon=folium.Icon(color="red"),
        ).add_to(route_map)

        route_map.fit_bounds(route_coords)

        st_folium(
            route_map,
            height=500,
            use_container_width=True,
            key="actual_road_route",
        )

        st.success(f"도로 경로 계산 완료! 거리: {total_m / 1000:.2f}km")

        st.warning(
            "도로망 기준 최단 경로입니다. 계단, 턱, 경사, 공사 여부까지 "
            "확인한 무장애 경로는 아니므로 실제 이동 환경을 확인해 주세요."
        )

    except (nx.NetworkXNoPath, nx.NodeNotFound):
        st.error("출발지와 도착지를 연결하는 보행 도로를 찾지 못했어요.")
    except Exception as e:
        st.error(f"경로 계산 오류: {e}")
