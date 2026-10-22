from pathlib import Path
import streamlit as st

st.set_page_config(page_title="왕긴급!", page_icon="🚨", layout="wide", initial_sidebar_state="expanded")

BASE_DIR = Path(__file__).resolve().parent

st.markdown("""
<style>
.stApp { background-color: #fffaf0; font-family: 'Malgun Gothic', sans-serif; }
.main-title { font-size: 2.8em; font-weight: 900; color: #ff5e7e; text-align: center; }
.card-box { border-radius: 30px; padding: 25px 15px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-bottom: 12px; border: 4px solid white; min-height: 245px; }
.bg-pink { background-color: #fff0f3; }
.bg-yellow { background-color: #fff9db; }
.bg-blue { background-color: #e8f4ff; }
</style>
""", unsafe_allow_html=True)

def safe_switch_page(relative_path):
    page_path = BASE_DIR / relative_path
    if not page_path.is_file():
        st.error(f"페이지 파일을 찾을 수 없습니다: {relative_path}")
        return
    st.switch_page(relative_path)

st.title("BIG-GINGEUP!! 🚨")
st.markdown("<div style='text-align: center; font-size: 1.3em; font-weight: 800; color: #57606f;'>어르신들을 위한 왕 긴급 안전 플랫폼</div>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="card-box bg-pink">
        <div style="font-size: 3.5em;">📞</div>
        <div style="font-size: 1.5em; font-weight: 800; color: #ff4757;">자동 긴급 전화</div>
        <div style="font-size: 1em; color: #555; margin-top: 10px;">긴급상황 시 보호자와 구조대에게 바로 신고해요.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📞 긴급 신고 바로가기", key="btn_call", use_container_width=True):
        safe_switch_page("pages/자동 긴급 전화.py")

with col2:
    st.markdown("""
    <div class="card-box bg-yellow">
        <div style="font-size: 3.5em;">📡</div>
        <div style="font-size: 1.5em; font-weight: 800; color: #d99a00;">주변 위험 감지</div>
        <div style="font-size: 1em; color: #555; margin-top: 10px;">주변 장애물과 위험 요소를 감지하여 안전을 지켜요.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📡 위험 확인 바로가기", key="btn_detect", use_container_width=True):
        safe_switch_page("pages/주변감지경보.py")

with col3:
    st.markdown("""
    <div class="card-box bg-blue">
        <div style="font-size: 3.5em;">🗺️</div>
        <div style="font-size: 1.5em; font-weight: 800; color: #1e90ff;">안전한 길 안내</div>
        <div style="font-size: 1em; color: #555; margin-top: 10px;">안전한 경로를 안내하여 편안한 보행을 도와요.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🗺️ 길 안내 바로가기", key="btn_path", use_container_width=True):
        safe_switch_page("pages/안전한 길 안내.py")

st.divider()
st.caption("빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전을 지킵니다.")
