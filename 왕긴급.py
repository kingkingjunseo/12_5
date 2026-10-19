import streamlit as st
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급! (BIG-GINGEUP)",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 통합 CSS 스타일링
st.markdown("""
<style>
    html, body, [data-testid="stSidebar"] {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
        color: #333;
    }
    .title-banner {
        text-align: center;
        background-color: #fce4ec;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 2.8em;
        font-weight: bold;
        color: #e91e63;
        margin-bottom: 5px;
    }
    .slogan {
        font-size: 1.2em;
        color: #555;
        font-weight: bold;
    }
    .card-box {
        border-radius: 25px;
        padding: 25px 20px 15px 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.06);
        margin-bottom: 10px;
    }
    .card-icon {
        font-size: 4em;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-desc {
        font-size: 1.05em;
        color: #555;
        min-height: 50px;
        line-height: 1.4;
    }
    .bg-red { background-color: #ffebee; }
    .title-red { color: #c62828; }
    .bg-yellow { background-color: #fffde7; }
    .title-yellow { color: #f57f17; }
    .bg-blue { background-color: #e3f2fd; }
    .title-blue { color: #1565c0; }
    div.stButton > button {
        width: 100% !important;
        border-radius: 18px !important;
        font-size: 1.3em !important;
        font-weight: bold !important;
        padding: 15px 0px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.12) !important;
    }
    div[data-testid="column"]:nth-child(1) div.stButton > button {
        background-color: #d32f2f !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-child(2) div.stButton > button {
        background-color: #fbc02d !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-child(3) div.stButton > button {
        background-color: #1976d2 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 상단 마스코트 및 슬로건
image_filename = 'image_0.png'
if os.path.exists(image_filename):
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.image(image_filename, use_container_width=True)
else:
    st.markdown('<div class="title-banner"><div class="main-title">BIG-GINGEUP!!</div><div class="slogan">언제 어디서나 왕긴급한 일에 대비하기 위해선 왕 긴 급!</div></div>', unsafe_allow_html=True)

st.write("")

# 4. 3개 카드 영역 및 페이지 이동
cols = st.columns(3)

# 1. 자동 긴급 전화
with cols[0]:
    st.markdown('<div class="card-box bg-red"><div class="card-icon">📞🚨</div><div class="card-title title-red">자동 긴급 전화</div><div class="card-desc">긴급상황 시 보호자와 구조대에게 바로 신고해요</div></div>', unsafe_allow_html=True)
    if st.button("🚨 긴급 신고 바로가기", key="go_call"):
        st.switch_page("pages/1_call.py")

# 2. 주변 위험 감지
with cols[1]:
    st.markdown('<div class="card-box bg-yellow"><div class="card-icon">📡⚠️</div><div class="card-title title-yellow">주변 위험 감지</div><div class="card-desc">주변 장애물을 센서를 통해 감지해서 안전을 지켜요</div></div>', unsafe_allow_html=True)
    if st.button("⚠️ 위험 감지 바로가기", key="go_detect"):
        st.switch_page("pages/2_detect.py")

# 3. 안전한 길 안내
with cols[2]:
    st.markdown('<div class="card-box bg-blue"><div class="card-icon">🗺️🚶</div><div class="card-title title-blue">안전한 길 안내</div><div class="card-desc">안전한 길로만 안내하여 안전한 보행을 도와요</div></div>', unsafe_allow_html=True)
    if st.button("🚶 길 안내 바로가기", key="go_path"):
        st.switch_page("pages/3_path.py")

st.divider()
st.caption("빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전을 지킵니다.")
