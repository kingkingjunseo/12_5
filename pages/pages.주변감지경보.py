
st.subheader("📍 현재 위치 확인")

location = gps_component(key="gps_location")

if not isinstance(location, dict):
    st.info("위치 확인 버튼을 눌러 주세요.")
    st.stop()

if location.get("error"):
    st.error(location["error"])
    st.stop()

lat = location.get("latitude")
lon = location.get("longitude")
accuracy = location.get("accuracy")

if lat is None or lon is None or accuracy is None:
    st.info("아직 위치 정보가 없습니다. 위치 확인 버튼을 눌러 주세요.")
    st.stop()

lat = float(lat)
lon = float(lon)
accuracy = float(accuracy)

st.write(f"위도: {lat:.6f}")
st.write(f"경도: {lon:.6f}")
st.write(f"위치 오차: 약 ±{accuracy:.0f}m")

if accuracy > 200:
    st.warning(
        "위치 정확도가 낮습니다. "
        "주변 위험 정보를 검색하기 전에 위치를 다시 확인해 주세요."
    )
    st.stop()

st.success("위치 좌표를 받았습니다.")

# 기존 지도 코드에서 현재 위치로 이 좌표를 사용해.
# folium.Map(location=[lat, lon], zoom_start=17)
