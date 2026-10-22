from pathlib import Path
import streamlit as st

# ========================================
# 1. 페이지 설정
# ========================================
st.set_page_config(
    page_title="왕긴급!",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent

# ========================================
# 2. 디자인 CSS 스타일
# ========================================
st.markdown("""
<style>
.stApp {
    background-color: #fffaf0;
    font-family: 'Malgun Gothic', 'Nanum Gothic', sans-serif;
}
.main-title {
    font-size: 2.8em;
    font-weight: 900;
    color: #ff5e7e;
    text-align: center;
    margin-bottom: 10px;
}
.intro-text {
    text-align: center;
    font-size: 1.3em;
    font-weight: 800;
    color: #57606f;
    margin: 15px 0 30px;
    line-height: 1.8;
}
.highlight-text {
    color: #ff4757;
    font-size: 1.2em;
}
.card-box {
    border-radius: 30px;
    padding: 30px 20px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
    margin-bottom: 15px;
    border: 4px solid white;
    min-height: 260px;
    box-sizing: border-box;
}
.card-icon {
    font-size: 3.5em;
    margin-bottom: 12px;
}
.card-title {
    font-size: 1.5em;
    font-weight: 800;
    margin-bottom: 12px;
}
.card-desc {
    font-size: 1em;
    color: #555;
    line-height: 1.6;
    font-weight: 600;
}
.bg-pink { background-color: #fff0f3; }
.title-pink { color: #ff4757; }
.bg-yellow { background-color: #fff9db; }
.title-yellow { color: #d99a00; }
.bg-blue { background-color: #e8f4ff; }
.title-blue { color: #1e90ff; }
</style>
""", unsafe_allow_html=True)

# ========================================
# 3. 상단 타이틀 및 소개 문구
# ========================================
st.markdown('<div class="main-title">BIG-GINGEUP!! 🚨</div>', unsafe_allow_html=True)

st.markdown("""
<div class="intro-text">
    언제 어디서나 왕긴급한 일에 대비하기 위해선
    <br>
    <span class="highlight-text">왕 긴 급!</span>
    <br>
    어르신들의 안전하고 편안한 일상을 지켜드립니다.
</div>
""", unsafe_allow_html=True)

st.divider()

# ========================================
# 4. 기능 소개 카드 영역 (3분할)
# ========================================
col1, col2, col3 = st.columns(3, gap="medium")

# 기능 1: 자동 긴급 전화
with col1:
    st.markdown("""
    <div class="card-box bg-pink">
        <div class="card-icon">📞</div>
        <div class="card-title title-pink">자동 긴급 전화</div>
        <div class="card-desc">
            긴급상황 발생 시 112, 119 및 지정된 보호자에게 즉시 연락하고 SOS 문자를 보낼 수 있도록 도와요.
        </div>
    </div>
    """, unsafe_allow_html=True)

# 기능 2: 주변 위험 감지
with col2:
    st.markdown("""
    <div class="card-box bg-yellow">
        <div class="card-icon">📡</div>
        <div class="card-title title-yellow">주변 위험 감지</div>
        <div class="card-desc">
            공사 구간, 계단, 경사로 등 보행 중 마주할 수 있는 주변 위험 요소를 지도와 데이터로 미리 확인해요.
        </div>
    </div>
    """, unsafe_allow_html=True)

# 기능 3: 안전한 길 안내
with col3:
    st.markdown("""
    <div class="card-box bg-blue">
        <div class="card-icon">🗺️</div>
        <div class="card-title title-blue">안전한 길 안내</div>
        <div class="card-desc">
            목적지까지의 경로를 지도에서 확인하고, 무장애 보행 환경을 점검하며 안전한 이동을 지원해요.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# 5. 하단 안내
# ========================================
st.divider()
st.caption("빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전을 지킵니다.")
