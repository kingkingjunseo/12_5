import streamlit as st
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급! (BIG-GINGEUP)",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 통합 CSS 스타일링 (모든 스타일을 한 곳에서 안전하게 정의)
st.markdown("""
<style>
    /* 기본 폰트 및 스타일 */
    html, body, [data-testid="stSidebar"] {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
        color: #333;
    }

    /* 페이지 배너 */
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

    /* 카드 스타일 */
    .card-box {
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
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

    /* 카드별 배경색 및 제목색 */
    .bg-red { background-color: #ffebee; }
    .title-red { color: #c62828; }

    .bg-yellow { background-color: #fffde7; }
    .title-yellow { color: #f57f17; }

    .bg-blue { background-color: #e3f2fd; }
    .title-blue { color: #1565c0; }

    /* 큰 버튼 공통 커스텀 */
    div.stButton > button {
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 1.3em !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }

    /* 버튼 개별 색상 지정 */
    /* 1번 버튼 (긴급 전화) */
    div[data-testid="column"]:nth-child(1) div.stButton > button {
        background-color: #d32f2f !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-child(1) div.stButton > button:hover {
        background-color: #b71c1c !important;
    }

    /* 2번 버튼 (위험 감지) */
    div[data-testid="column"]:nth-child(2) div.stButton > button {
        background-color: #fbc02d !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-child(2) div.stButton > button:hover {
        background-color: #f9a825 !important;
    }

    /* 3번 버튼 (길 안내) */
    div[data-testid="column"]:nth-child(3) div.stButton > button {
        background-color: #1976d2 !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-child(3) div.stButton > button:hover {
        background-color: #1565c0 !important;
    }

    /* 가상 지도 UI */
    .mock-map {
        border: 2px dashed #90caf9;
        border-radius: 12px;
        background-color: #ffffff;
        padding: 15px;
        text-align: center;
        color: #1565c0;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 최상단 마스코트 및 슬로건
# 업로드한 이미지 파일명이 image_0.png 또는 image_12aa84.png 인지 확인하세요.
image_filename = 'image_0.png'

if os.path.exists(image_filename):
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.image(image_filename, use_container_width=True)
else:
    # 이미지가 없을 경우 대체 텍스트 출력
    st.markdown("""
    <div class="title-banner">
        <div class="main-title">BIG-GINGEUP!!</div>
        <div class="slogan">언제 어디서나 왕긴급한 일에 대비하기 위해선<br>왕 긴 급!</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. 메인 3가지 기능 (카드 레이아웃)
cols = st.columns(3)

# --- 1) 자동 긴급 전화 ---
with cols[0]:
    st.markdown("""
    <div class="card-box bg-red">
        <div class="card-icon">📞🚨</div>
        <div class="card-title title-red">자동 긴급 전화</div>
        <div class="card-desc">긴급상황 시 보호자와 구조대에게 바로 신고해요</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("긴급 신고!", key="btn_call"):
        st.error("⚠️ [시뮬레이션] 긴급 신호를 전송합니다!\n\n- 보호자 (010-1234-5678) 호출 중...\n- 119 구조대 위치 정보 전송 완료!")

# --- 2) 주변 위험 감지 ---
with cols[1]:
    st.markdown("""
    <div class="card-box bg-yellow">
        <div class="card-icon">📡⚠️</div>
        <div class="card-title title-yellow">주변 위험 감지</div>
        <div class="card-desc">주변 장애물을 센서를 통해 감지해서 안전을 지켜요</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("위험 확인!", key="btn_detect"):
        st.success("✅ [센서 작동 중]\n\n현재 주변 3m 이내에 위험 장애물이 없습니다. 안심하고 보행하세요!")

# --- 3) 안전한 길 안내 ---
with cols[2]:
    st.markdown("""
    <div class="card-box bg-blue">
        <div class="card-icon">🗺️🚶</div>
        <div class="card-title title-blue">안전한 길 안내</div>
        <div class="card-desc">안전한 길로만 안내하여 안전한 보행을 도와요</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("경로 찾기!", key="btn_path"):
        st.session_state['show_map_input'] = True

# 경로 찾기 버튼 눌렀을 때 입력창 표시
if st.session_state.get('show_map_input', False):
    st.markdown("---")
    st.subheader("🗺️ 안전 보행 경로 탐색")
    destination = st.text_input("목적지를 입력하세요 (예: 집, 노인복지관, 병원):", "우리집")
    
    if st.button("경로 검색 시작"):
        st.info(f"<b>'{destination}'</b>(으)로 가는 경사 없는 최적의 안전 경로를 찾았습니다.", icon="ℹ️")
        st.markdown(f"""
        <div class="mock-map">
            📍 [안전 지도] {destination}까지 도보 약 15분 소요<br>
            (계단 없음 / 턱 없음 / 보행자 전용 도로)
        </div>
        """, unsafe_allow_html=True)

# 5. 푸터
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #888; font-size: 0.9em;">빅-긴급!! (BIG-GINGEUP) © 2026. 노인분들의 안전한 일상을 응원합니다.</div>', unsafe_allow_html=True)
