
import streamlit as st
import streamlit.components.v1 as components
import requests
import folium

from streamlit_geolocation import streamlit_geolocation
from streamlit_folium import st_folium

st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="wide",
)

st.title("🚶 안전 동행")
st.subheader("현재 위치 및 주변 보행 주의 정보")

st.info(
    "위치 확인 후 지도에 내 위치를 표시합니다. "
    "위치 정확도가 낮으면 주변 위험 검색을 진행하지 않습니다."
)

# 1. 브라우저에서 위치 가져오기
location = streamlit_geolocation()

if not isinstance(location, dict):
    st.warning("위치 확인 버튼을 누르고 브라우저의 위치 권한을 허용해 주세요.")
    st.stop()

lat = location.get("latitude")
lon = location.get("longitude")
accuracy = location.get("accuracy")

if lat is None or lon is None:
    st.warning("아직 좌표를 받지 못했습니다. 위치 확인 버튼을 다시 눌러 주세요.")
    st.stop()

try:
    lat = float(lat)
    lon = float(lon)
    accuracy = float(accuracy) if accuracy is not None else None
except (ValueError, TypeError):
    st.error("좌표 또는 위치 정확도를 읽을 수 없습니다.")
    st.stop()

if not (-90 <= lat <= 90 and -180 <= lon <= 180):
    st.error("잘못된 좌표가 반환되었습니다.")
    st.stop()

st.write(f"**위도:** {lat:.6f}")
st.write(f"**경도:** {lon:.6f}")

if accuracy is None:
    st.warning("기기에서 위치 정확도 정보를 받지 못했습니다.")
elif accuracy > 1000:
    st.error(
        f"위치 오차가 약 {accuracy:.0f}m입니다. "
        "현재 위치가 부정확할 수 있어 위험 정보 검색을 중단했습니다."
    )
    st.info(
        "기기의 위치 권한을 확인하고 다시 시도해 주세요. "
        "데스크톱은 휴대전화보다 위치가 부정확할 수 있습니다."
    )
    st.stop()
else:
    st.success(f"위치 정보 수신 완료 · 표시된 정확도 약 ±{accuracy:.0f}m")

# 2. 지도 표시
st.subheader("🗺️ 내 현재 위치")

map_view = folium.Map(
    location=[lat, lon],
    zoom_start=17,
    control_scale=True,
)

folium.Marker(
    [lat, lon],
    tooltip="기기에서 받은 현재 좌표",
    popup=f"위도: {lat:.6f}<br>경도: {lon:.6f}",
    icon=folium.Icon(color="blue", icon="user", prefix="fa"),
).add_to(map_view)

st_folium(
    map_view,
    height=500,
    use_container_width=True,
    key=f"map_{lat:.5f}_{lon:.5f}",
)

# 3. 주변 보행 주의 정보 검색
st.subheader("🚧 주변 500m 보행 주의 정보")

@st.cache_data(ttl=180)
def find_hazards(latitude, longitude):
    query = f"""
    [out:json][timeout:20];
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
    ]

    errors = []

    for server in servers:
        try:
            response = requests.post(
                server,
                data={"data": query},
                timeout=30,
                headers={"User-Agent": "SafetyCompanion/1.0"},
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for element in data.get("elements", []):
                tags = element.get("tags", {})

                if "lat" in element and "lon" in element:
                    e_lat, e_lon = element["lat"], element["lon"]
                else:
                    center = element.get("center", {})
                    e_lat, e_lon = center.get("lat"), center.get("lon")

                if e_lat is None or e_lon is None:
                    continue

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
                    continue

                results.append({
                    "lat": float(e_lat),
                    "lon": float(e_lon),
                    "kind": kind,
                    "name": tags.get("name", "이름 미등록"),
                })

            return results, None

        except (requests.RequestException, ValueError) as error:
            errors.append(str(error))

    return [], " / ".join(errors)


if st.button("🔎 주변 주의 정보 검색", type="primary"):
    with st.spinner("주변 지도 데이터를 검색 중입니다..."):
        hazards, error = find_hazards(round(lat, 5), round(lon, 5))

    if error:
        st.error("주변 정보 서버에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요.")
        st.caption(error)
    elif not hazards:
        st.info("지도 데이터에서 해당 조건의 주의 정보를 찾지 못했습니다.")
    else:
        hazard_map = folium.Map(
            location=[lat, lon],
            zoom_start=17,
            control_scale=True,
        )

        folium.Marker(
            [lat, lon],
            tooltip="현재 위치",
            icon=folium.Icon(color="blue", icon="user", prefix="fa"),
        ).add_to(hazard_map)

        for item in hazards:
            folium.Marker(
                [item["lat"], item["lon"]],
                tooltip=item["kind"],
                popup=f'{item["kind"]}<br>이름: {item["name"]}',
                icon=folium.Icon(
                    color="red",
                    icon="exclamation-triangle",
                    prefix="fa",
                ),
            ).add_to(hazard_map)

        st_folium(
            hazard_map,
            height=520,
            use_container_width=True,
            key=f"hazards_{lat:.5f}_{lon:.5f}",
        )

        st.warning(f"지도 데이터에서 주의 정보 {len(hazards)}개를 찾았습니다.")
        for item in hazards:
            st.write(f"⚠️ {item['kind']} — {item['name']}")

st.caption(
    "주의: 이 앱은 지도에 등록된 일부 공사·계단·노면 정보만 표시합니다. "
    "실시간 위험을 모두 감지하지 못하므로 지도에 표시가 없어도 안전하다는 뜻은 아닙니다."
)
