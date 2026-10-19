import streamlit as st
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급! (BIG-GINGEUP)",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 세션 상태 초기화 (현재 보고 있는 페이지 저장)
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# 2. 통합 CSS 스타일링
st.markdown("""
<style>
    /* 기본 폰트 및 스타일 */
    html, body, [data-testid="stSidebar"] {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
        color: #333;
    }

    /* 상단 배너 */
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

    /* 카드 박스 디자인 */
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

    /* 카드 배경 및 제목 색상 */
    .bg-red { background-color: #ffebee; }
    .title-red { color: #c62828; }

    .bg-yellow { background-color: #fffde7; }
    .title-yellow { color: #f57f17; }

    .bg-blue { background-color: #e3f2fd; }
    .title-blue { color: #1565c0; }

    /* 큰 이동 버튼 스타일 */
    div.stButton > button {
        width: 100% !important;
        border-radius: 18px !important;
        font-size: 1.3em !important;
        font-weight: bold !important;
        padding: 15px 0px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.12) !important;
    }

    /* 버튼 개별 색상 지정 */
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

    /* 뒤로가기 버튼 */
    .back-btn div.stButton > button {
        background-color: #757575 !important;
        color: white !important;
        width: auto !important;
        padding: 8px 25px !important;
        font-size: 1em !important;
        margin-bottom: 20px;
    }

    /* 지도 모의 UI */
    .mock-map {
        border: 2px dashed #1976d2;
        border-radius: 15px;
        background-color: #ffffff;
        padding: 30px;
        text-align: center;
        color: #1565c0;
        font-weight: bold;
        font-size: 1.2em;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)


# --- [페이지 1: 메인 화면] ---
if st.session_state['page'] == 'home':
    # 마스코트 이미지 표시
    image_filename = 'image_0.png'
    if os.path.exists(image_filename):
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            st.image(image_filename, use_container_width=True)
    else:
        st.markdown('<div class="title-banner"><div class="main-title">BIG-GINGEUP!!</div><div class="slogan">언제 어디서나 왕긴급한 일에 대비하기 위해선<br>왕 긴 급!</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3개 카드 영역
    cols = st.columns(3)

    # 1. 자동 긴급 전화
    with cols[0]:
        st.markdown('<div class="card-box bg-red"><div class="card-icon">📞🚨</div><div class="card-title title-red">자동 긴급 전화</div><div class="card-desc">긴급상황 시 보호자와 구조대에게 바로 신고해요</div></div>', unsafe_allow_html=True)
        if st.button("🚨 긴급 신고 화면으로", key="go_call"):
            st.session_state['page'] = 'call'
            st.rerun()

    # 2. 주변 위험 감지
    with cols[1]:
        st.markdown('<div class="card-box bg-yellow"><div class="card-icon">📡⚠️</div><div class="card-title title-yellow">주변 위험 감지</div><div class="card-desc">주변 장애물을 센서를 통해 감지해서 안전을 지켜요</div></div>', unsafe_allow_html=True)
        if st.button("⚠️ 위험 감지 화면으로", key="go_detect"):
            st.session_state['page'] = 'detect'
            st.rerun()

    # 3. 안전한 길 안내
    with cols[2]:
        st.markdown('<div class="card-box bg-blue"><div class="card-icon">🗺️🚶</div><div class="card-title title-blue">안전한 길 안내</div><div class="card-desc">안전한 길로만 안내하여 안전한 보행을 도와요</div></div>', unsafe_allow_html=True)
        if st.button("🚶 길 안내 화면으로", key="go_path"):
            st.session_state['page'] = 'path'
            st.rerun()

    st.markdown("<br><hr
