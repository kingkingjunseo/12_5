import streamlit as st
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급! (BIG-GINGEUP)",
    page_icon="👼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화 (화면 전환용)
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

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
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    /* 귀여운 파스텔 카드 박스 */
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

    /* 카드별 파스텔 색상 */
    .bg-pink { background-color: #fff0f3; }
    .title-pink { color: #ff4757; }

    .bg-yellow { background-color: #fff9db; }
    .title-yellow { color: #ffa502; }

    .bg-blue { background-color: #e8f4ff; }
    .title-blue { color: #1e90ff; }

    /* 동글동글 통통한 이동 버튼 */
    div.stButton > button {
        width: 100% !important;
        border-radius: 22px !important;
        font-size: 1.3em !important;
        font-weight: 800 !important;
        padding: 15px 0px !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08) !important;
    }

    /* 버튼 포인트 색상 */
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

    /* 뒤로가기 버튼 */
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


# --- [화면 1: 메인 홈] ---
if st.session_state['page'] == 'home':
    
    # 🌟 저장소에 있는 이미지 파일 자동 감지 및 안전 로딩 🌟
    possible_files = ['image_0.png', 'image_13935c.png', 'image_12aa84.png', 'image.png']
    found_image = None

    # 폴더 내 존재하는 파일 탐색
    for file in possible_files:
        if os.path.exists(file):
            found_image = file
            break
            
    # 폴더 안에 이미지 파일(png, jpg)이 하나라도 있다면 자동 탐색
    if not found_image:
        for file in os.listdir('.'):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                found_image = file
                break

    # 안전한 이미지 표시 처리 (오류 완전 방지)
    image_loaded = False
    if found_image:
        try:
            col_l, col_c, col_r = st.columns([1, 2, 1])
            with col_c:
                st.image(found_image, use_container_width=True)
            image_loaded = True
        except Exception:
            image_loaded = False

    # 이미지를 불러오지 못한 경우 귀여운 텍스트 배너로 대체
    if not image_loaded:
        st.markdown('<div class="title-banner"><div class="main-title">👼 BIG-GINGEUP!! 🚨</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; font-size:1.3em; font-weight:800; color:#57606f; margin-top:-5px; margin-bottom:20px;">언제 어디서나 왕긴급한 일에 대비하기 위해선<br><span style="color:#ff4757; font-size:1.2em;">왕 긴 급!</span></div>', unsafe_allow_html=True)

    # 파스텔 3개 기능 카드
    cols = st.columns(3)

    # 1. 자동 긴급 전화
    with cols[0]:
        st.markdown('<div class="card-box bg-pink"><div class="card-icon">📞💖</div><div class="card-title title-pink">자동 긴급 전화</div><div class="card-desc">긴급상황 시 보호자와 구조대에게 바로 신고해요</div></div>', unsafe_allow_html=True)
        if st.button("🚨 긴급 신고 바로가기", key="go_call"):
            st.session_state['page'] = 'call'
            st.rerun()

    # 2. 주변 위험 감지
    with cols[1]:
        st.markdown('<div class="card-box bg-yellow"><div class="card-icon">📡✨</div><div class="card-title title-yellow">주변 위험 감지</div><div class="card-desc">주변 장애물을 센서를 통해 감지해서 안전을 지켜요</div></div>', unsafe_allow_html=True)
        if st.button("⚠️ 위험 확인 바로가기", key="go_detect"):
            st.session_state['page'] = 'detect'
            st.rerun()

    # 3. 안전한 길 안내
    with cols[2]:
        st.markdown('<div class="card-box bg-blue"><div class="card-icon">🗺️🧸</div><div class="card-title title-blue">안전한 길 안내</div><div class="card-desc">안전한 길로만 안내하여 안전한 보행을 도와요</div></div>', unsafe_allow_html=True)
        if st.button("🚶 길 안내 바로가기", key="go_path"):
            st.session_state['page'] = 'path'
            st.rerun()

    st.divider()
    st.caption("💖 빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전을 지킵니다.")


# --- [화면 2: 자동 긴급 전화] ---
elif st.session_state['page'] == 'call':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("👈 메인으로 돌아가기", key="back_home1"):
        st.session_state['page'] = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("📞 자동 긴급 전화 서비스")
    st.write("긴급 상황 시 버튼 한 번으로 도움을 요청하세요.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.error("### 🚑 119 긴급 구조대")
        st.write("클릭 시 119로 즉시 전화가 연결됩니다.")
        st.markdown('<a href="tel:119" style="display:inline-block; background
