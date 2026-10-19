import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="안전 동행",
    page_icon="🌼",
    layout="wide",
)

st.title("🌼 안전 동행")

if st.button("📍 위치 찾기", use_container_width=True):
    st.session_state["show_map"] = True

if st.session_state.get("show_map", False):
    latitude = 36.8151
    longitude = 127.1139

    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=17,
    )

    folium.Marker(
        [latitude, longitude],
        tooltip="오성고등학교",
        popup="오성고등학교",
        icon=folium.Icon(color="blue"),
    ).add_to(m)

    st_folium(
        m,
        height=480,
        use_container_width=True,
        key="oseong_map",
    )
