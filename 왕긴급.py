import streamlit as st
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급!",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태로 화면 위치 관리
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# 3. 파스텔톤 CSS
st.markdown("""
<style>
    .stApp {
        background-color: #fffaf0;
        font-family: 'Malgun Gothic', 'Nanum Gothic', sans-serif;
    }
    .title-banner {
        text-align: center;
        background: linear-gradient(135deg, #ffdeeb 0%, #e8f4ff 100%);
        padding: 25px;
        border-radius: 30px;
        box-shadow: 0 8px 16px rgba(255, 182, 193, 0.3);
        margin-bottom: 20px;
        border: 3px solid #ffffff;
    }
    .main-title {
        font-size: 2.8em;
        font-weight: 900;
        color: #ff5e7e;
        margin-bottom: 8px;
    }
    .card-box {
        border-radius: 30px;
        padding: 25px 20px 15px 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        border: 4px solid #ffffff;
    }
    .card-icon { font-size: 4em; margin-bottom: 8px; }
    .card-title { font-size: 1.8em; font-weight: 800; margin-bottom: 10px; }
    .card-desc { font-size: 1.05em; color: #555; min-height: 50px; line-height: 1.4; font-weight: 600; }
    .bg-pink { background-color: #fff0f3; }
    .title-pink { color: #ff4757; }
    .bg-yellow { background-color: #fff9db; }
    .title-yellow { color: #ffa502; }
    .bg-blue { background-color: #e8f4ff; }
    .title-blue { color: #1e90ff; }

    div.stButton > button {
        width: 100% !important;
        border-radius: 22px !important;
        font-size: 1.3em !important;
        font-weight: 800 !important;
        padding: 15px 0px !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08) !important;
    }
    div[data-testid="column"]:nth-child(1) div.stButton > button { background-color: #ff6b81 !important; color: white !important; }
    div[data-testid="column"]:nth-child(2) div.stButton > button { background-color: #eccc68 !important; color: white !important; }
    div[data-testid="column"]:nth-child(3) div.stButton > button { background-color: #70a1ff !important; color: white !important; }
    .back-btn div.stButton > button {
        background-color: #a4b0be !important;
        color: white !important;
        width: auto !important;
        padding: 8px 25px !important;
        font-size: 1em !important;
        margin-bottom: 15px;
    }
    .mock-map {
        border: 3px dashed #70a1ff;
        border-radius: 20px;
        background-color: #ffffff;
        padding: 25px;
        text-align: center;
        color: #3742fa;
        font-weight: bold;
        font-size: 1.2em;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 메인 홈 화면
if st.session_state['page'] == 'home':
    found_image = None
    for file in os.listdir('.'):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            found_image =
