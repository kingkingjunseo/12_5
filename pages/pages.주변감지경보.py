
import streamlit as st
import requests
import pandas as pd
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="centered",
)

st.title("🚶 안전 동행")
st.header("어르신 보행 안전 도우미")

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 20px;
}
.stButton button {
    min-height: 60px;
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.warning(
    "이 앱은 지도에 등록된 보행 주의 정보를 검색합니다. "
    "눈앞의 장애물이나 다가오는 자동차를 직접 감지하지는 않습니다."
)

st.subheader("📍 현재 위치")

location = streamlit_geolocation()

if not isinstance(location, dict):
    st.info("위치 확인 버튼을 누르고 위치 권한을 허용해 주세요.")
    st.stop()

lat = location.get("latitude")
lon = location.get("longitude")

if lat is None or lon is None:
    st.info("현재 위치를 가져오지 못했습니다. 위치 권한을 확인해 주세요.")
    st.stop()

try:
    lat = float(lat)
    lon = float(lon)
except (TypeError, ValueError):
    st.error("위치 정보가 올바르지 않습니다.")
    st.stop()

if not (-90 <= lat <= 90 and -180 <= lon <= 180):
    st.error("올바르지 않은 GPS 좌표입니다.")
    st.stop()

st.success("현재 위치를 확인했습니다.")

st.subheader("🚧 주변 보행 주의 정보")

if st.button("주변 500m 검색", type="primary", use_container_width=True):
    query = f"""
    [out:json][timeout:25];
    (
      nwr(around:500,{lat},{lon})["construction"];
      nwr(around:500,{lat},{lon})["highway"="steps"];
      nwr(around:500,{lat},{lon})["barrier"="construction"];
    );
    out center tags;
    """

    try:
        with st.spinner("주변 지도 정보를 검색하고 있습니다..."):
            response = requests.post(
                "https://overpass-api.de/api/interpreter",
                data={"data": query},
                timeout=35,
            )
            response.raise_for_status()
            data = response.json()

        results = []

        for item in data.get("elements", []):
            tags = item.get("tags", {})

            if "construction" in tags or tags.get("barrier") == "construction":
                kind = "공사 관련 정보"
            elif tags.get("highway") == "steps":
                kind = "계단"
            else:
                kind = "보행 주의 정보"

            results.append({
                "종류": kind,
                "이름": tags.get("name", "이름 미등록"),
            })

        st.session_state["results"] = results
        st.session_state["searched"] = True

    except requests.RequestException:
        st.error("지도 서버 연결에 실패했습니다. 잠시 후 다시 시도해 주세요.")
    except ValueError:
        st.error("지도 데이터를 읽을 수 없습니다.")

if st.session_state.get("searched", False):
    results = st.session_state.get("results", [])

    if results:
        st.error(f"지도에서 보행 주의 정보 {len(results)}개를 찾았습니다.")
        st.dataframe(
            pd.DataFrame(results),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("검색 조건에 해당하는 정보가 없습니다.")

    st.caption(
        "검색 결과가 없더라도 주변이 안전하다는 뜻은 아닙니다."
    )

