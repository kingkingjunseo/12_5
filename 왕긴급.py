import streamlit as st
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급!",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 파스텔톤 커스텀 CSS
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
    .card-icon {
        font-size: 4em;
        margin-bottom: 8px;
    }
    .card-title {
        font-size: 1.8em;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .card-desc {
        font-size: 1.05em;
        color: #555;
        min-height: 50px;
        line-height: 1.4;
        font-weight: 600;
    }
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
    div[data-testid="column"]:nth-child(1) div.stButton > button {
        background-color: #ff6b81 !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-child(2) div.stButton > button {
        background-color: #eccc68 !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-child(3) div.stButton > button {
        background-color: #70a1ff !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 🌟 상단 천사 마스코트 캐릭터 로드
found_image = None
for file in os.listdir('.'):
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        found_image = file
        break

if found_image:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.image(found_image, use_container_width=True)
else:
    st.markdown('<div class="title-banner"><div class="main-title">BIG-GINGEUP!!</div></div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; font-size:1.3em; font-weight:800; color:#57606f; margin-top:-5px; margin-bottom:20px;">언제 어디서나 왕긴급한 일에 대비하기 위해선<br><span style="color:#ff4757; font-size:1.2em;">왕 긴 급!</span></div>', unsafe_allow_html=True)

cols = st.columns(3)

# 1. 자동 긴급 전화
with cols[0]:
    st.markdown('<div class="card-box bg-pink"><div class="card-icon">📞</div><div class="card-title title-pink">자동 긴급 전화</div><div class="card-desc">긴급상황 시 보호자와 구조대에게 바로 신고해요</div></div>', unsafe_allow_html=True)
    if st.button("긴급 신고 바로가기", key="btn_call"):
        try:
            st.switch_page("pages/자동 긴급 전화.py")
        except Exception:
            st.switch_page("자동 긴급 전화.py")

# 2. 주변감지경보
with cols[1]:
    st.markdown('<div class="card-box bg-yellow"><div class="card-icon">📡</div><div class="card-title title-yellow">주변 감지 경보</div><div class="card-desc">주변 장애물을 센서를 통해 감지해서 안전을 지켜요</div></div>', unsafe_allow_html=True)
    if st.button("위험 확인 바로가기", key="btn_detect"):
        try:
            st.switch_page("pages/주변감지경보.py")
        except Exception:
            st.switch_page("pages.주변감지경보.py")

# 3. 안전한 길 안내
with cols[2]:
    st.markdown('<div class="card-box bg-blue"><div class="card-icon">🗺️</div><div class="card-title title-blue">안전한 길 안내</div><div class="card-desc">안전한 길로만 안내하여 안전한 보행을 도와요</div></div>', unsafe_allow_html=True)
    if st.button("길 안내 바로가기", key="btn_path"):
        try:
            st.switch_page("pages/안전한 길 안내.py")
        except Exception:
            st.switch_page("안전한 길 안내.py")

st.divider()
st.caption("빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전을 지킵니다.")
