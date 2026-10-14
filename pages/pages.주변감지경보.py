
import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import json

st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="centered"
)

st.title("🚶 안전 동행")
st.header("어르신 보행 안전 도우미")

st.markdown("""
<style>
.stApp { font-size: 20px; }
.stButton button {
    min-height: 55px;
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.warning(
    "이 앱은 지도에 등록된 보행 주의 정보를 검색합니다. "
    "눈앞의 장애물이나 다가오는 자동차를 직접 감지하지는 않습니다."
)

# 브라우저에서 GPS 위치를 가져옴
components.html("""
<div style="font-family:sans-serif;text-align:center">
  <button onclick="getLocation()"
    style="font-size:20px;padding:14px;width:100%">
    📍 현재 위치 가져오기
  </button>
  <p id="status">위치 확인 버튼을 눌러 주세요.</p>
  <script>
  function getLocation() {
    const status = document.getElementById("status");
    if (!navigator.geolocation) {
      status.innerText = "이 브라우저는 위치 기능을 지원하지 않습니다.";
      return;
    }
    status.innerText = "위치를 확인하는 중...";
    navigator.geolocation.getCurrentPosition(
      function(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        status.innerText =
          "위도: " + lat.toFixed(5) +
          ", 경도: " + lon.toFixed(5);
        const url = "https://www.openstreetmap.org/?mlat="
          + lat + "&mlon=" + lon + "#map=17/" + lat + "/" + lon;
        const link = document.createElement("a");
        link.href = url;
        link.target = "_blank";
        link.innerText = "내 위치를 지도에서 확인";
        status.appendChild(document.createElement("br"));
        status.appendChild(link);
      },
      function(error) {
        status.innerText =
          "위치를 가져오지 못했습니다. 브라우저 권한과 GPS 설정을 확인해 주세요.";
      }
    );
  }
  </script>
</div>
""", height=150)

st.info(
    "참고: 위 위치 기능은 브라우저 안에서 작동합니다. "
    "이 간단한 버전은 GPS 좌표를 Streamlit 서버로 전달하지 않으므로 "
    "좌표를 이용한 자동 주변 위험 검색은 아직 연결되지 않았습니다."
)

st.subheader("🚧 주변 주의 정보")

lat_input = st.number_input(
    "위도",
    min_value=-90.0,
    max_value=90.0,
    value=37.5665,
    format="%.6f"
)

lon_input = st.number_input(
    "경도",
    min_value=-180.0,
    max_value=180.0,
    value=126.9780,
    format="%.6f"
)

if st.button("주변 500m 검색", type="primary"):
    query = f"""
    [out:json][timeout:25];
    (
      nwr(around:500,{lat_input},{lon_input})["construction"];
      nwr(around:500,{lat_input},{lon_input})["highway"="steps"];
      nwr(around:500,{lat_input},{lon_input})["barrier"="construction"];
    );
    out center tags;
    """

    try:
        with st.spinner("주변 지도 정보를 검색하고 있습니다..."):
            response = requests.post(
                "https://overpass-api.de/api/interpreter",
                data={"data": query},
                timeout=35
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
                "이름": tags.get("name", "이름 미등록")
            })

        if results:
            st.error(f"주의 요소 {len(results)}개를 찾았습니다.")
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("검색 조건에 해당하는 지도 정보가 없습니다.")

    except requests.RequestException:
        st.error("지도 서버 연결에 실패했습니다. 잠시 후 다시 시도해 주세요.")
    except ValueError:
        st.error("지도 데이터를 읽을 수 없습니다.")

st.caption(
    "안전 동행은 보행 보조용 시제품이며, 실제 위험을 모두 감지하거나 "
    "안전을 보장하지 않습니다."
)
