import streamlit as st
import os

# 페이지 설정
st.set_page_config(
    page_title="왕긴급! (BIG-GINGEUP)",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS를 통한 귀여운 테마 적용 ---
# 폰트, 큰 버튼, 파스텔 톤 색상, 둥근 테두리 적용
# 이미지 파일이 없어도 앱이 실행되도록 st.image 호출 시 에러 처리를 포함하는 것이 좋습니다.
# 여기서는 사용자가 제공한 이미지가 같은 경로에 있다고 가정합니다.

st.markdown("""
<style>
    /* 기본 폰트 크기 및 색상 */
    html, body, [data-testid="stSidebar"], .st-emotion-cache-12fm7u {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
        color: #333;
    }

    /* 페이지 제목 및 마스코트 */
    .title-banner {
        text-align: center;
        background-color: #fce4ec; /* 연분홍 */
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 30px;
    }
    .main-title {
        font-size: 3em;
        font-weight: bold;
        color: #e91e63; /* 짙은 핑크 */
        margin-bottom: 10px;
    }
    .slogan {
        font-size: 1.2em;
        color: #555;
    }

    /* 기능 카드 공통 스타일 */
    .emergency-card {
        border-radius: 25px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        margin-bottom: 20px;
    }
    .emergency-card:hover {
        transform: translateY(-5px);
    }
    .card-icon {
        font-size: 5em;
        margin-bottom: 15px;
    }
    .card-title {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-description {
        font-size: 1em;
        color: #666;
        margin-bottom: 25px;
        line-height: 1.4;
    }

    /* 큰 버튼 공통 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 15px !important;
        font-size: 1.3em !important;
        font-weight: bold !important;
        padding: 15px !important;
        border: none !important;
        cursor: pointer;
        transition: all 0.2s;
    }
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* 카드별 개별 색상 및 버튼 스타일 */
    /* 1. 자동 긴급 전화 (빨강) */
    .card-red { background-color: #ffebf0; }
    .card-red .card-title { color: #d32f2f; }
    .stButton.call-btn > button {
        background-color: #d32f2f !important;
        color: white !important;
    }
    .stButton.call-btn > button:hover {
        background-color: #b71c1c !important;
    }

    /* 2. 주변 위험 감지 (노랑) */
    .card-yellow { background-color: #fffde7; }
    .card-yellow .card-title { color: #f9a825; }
    .stButton.detect-btn > button {
        background-color: #fbc02d !important;
        color: white !important;
    }
    .stButton.detect-btn > button:hover {
        background-color: #f9a825 !important;
    }

    /* 3. 안전한 길 안내 (파랑) */
    .card-blue { background-color: #e3f2fd; }
    .card-blue .card-title { color: #1976d2; }
    .stButton.path-btn > button {
        background-color: #2196f3 !important;
        color: white !important;
    }
    .stButton.path-btn > button:hover {
        background-color: #1976d2 !important;
    }

    /* 지도 모의 UI */
    .mock-map {
        border: 2px solid #ddd;
        border-radius: 15px;
        background-color: #eee;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #666;
        font-weight: bold;
        margin-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)

# --- 메인 페이지 최상단: 마스코트 및 슬로건 ---
# 사용자 이미지가 있는지 확인
image_path = 'image_0.png'
if os.path.exists(image_path):
    # 이미지가 있으면 중앙에 크게 표시
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image_path, use_column_width=True)
else:
    # 이미지가 없으면 텍스트로 대체 (배포 시 에러 방지)
    st.markdown('<div class="title-banner"><div class="main-title">왕긴급!</div><div class="slogan">언제 어디서나 왕긴급한 일에 대비하기 위해선 왕 긴 급!</div></div>', unsafe_allow_html=True)

# --- 핵심 기능 3가지 (카드 형태) ---
st.markdown("---") # 구분선
cols = st.columns(3) # 3개의 열 생성

# 1. 자동 긴급 전화 카드
with cols[0]:
    st.markdown('<div class="emergency-card card-red">', unsafe_allow_html=True)
    st.markdown('<div class="card-icon">📞🚨</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">자동 긴급 전화</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-description">긴급상황 시 보호자와 구조대에게 바로 신고해요</div>', unsafe_allow_html=True)
    
    # 버튼 및 동작 시뮬레이션
    call_col = st.columns([1])
    with call_col[0]:
        # 'call-btn' 클래스를 stButton에 적용하기 위해 st.markdown을 사용
        call_btn = st.button("긴급 신고!", key="call_btn", help="보호자에게 전화를 겁니다.")
        # Streamlit button에 CSS class를 직접 적용할 수 없어 markdown을 사용하여 wrapping
        st.markdown("""
        <style>
            [data-testid="stButton"] button[key="call_btn"] {
                background-color: #d32f2f !important;
                color: white !important;
                width: 100% !important;
                border-radius: 15px !important;
                font-size: 1.3em !important;
            }
