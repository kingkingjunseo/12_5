import streamlit as st
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급! (BIG-GINGEUP)",
    page_icon="👼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화 (현재 화면 위치 저장)
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# 2. 러블리 파스텔톤 CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경을 연한 크림 파스텔톤으로 설정 */
    .stApp {
        background-color: #fffaf0;
        font-family: 'Malgun Gothic', 'Nanum Gothic', sans-serif;
    }

    /* 메인 타이틀 파스텔 배너 */
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
    .slogan {
        font-size: 1.25em;
        color: #6c5ce7;
        font-weight: bold;
        line-height: 1.5;
    }

    /* 귀여운 파스텔 카드 박스 */
    .card-box {
        border-radius: 30px;
        padding: 30px 20px 20px 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        border: 4px solid #ffffff;
        transition: transform 0.2s ease-in-out;
    }
    .card-icon {
        font-size: 4.5em;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 1.9em;
        font-weight: 800;
        margin-bottom: 12px;
    }
    .card-desc {
        font-size: 1.1em;
        color: #555555;
        min-height: 55px;
        line-height: 1.5;
        font-weight: 600;
    }

    /* 카드별 파스텔 배경 색상 */
    .bg-pink { background-color: #fff0f3; }
    .title-pink { color: #ff4757; }

    .bg-yellow { background-color: #fff9db; }
    .title-yellow { color: #ffa502; }

    .bg-blue { background-color: #e8f4ff; }
    .title-blue { color: #1e90ff; }

    /* 동글동글 통통한 큰 버튼 */
    div.stButton > button {
        width: 100% !important;
        border-radius: 25px !important;
        font-size: 1.35em !important;
        font-weight: 800 !important;
        padding: 16px 0px !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1) !important;
        transition: all 0.2s !important;
    }
    div.stButton > button:active {
        transform: scale(0.96) !important;
    }

    /* 버튼 개별 파스텔 포인트 색상 */
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
        padding: 10px 30px !important;
        font-size: 1.1em !important;
        border-radius: 20px !important;
        margin-bottom: 15px;
    }

    /* 지도 파스텔 박스 */
    .mock-map {
        border: 3px dashed #70a1ff;
        border-radius: 20px;
        background-color: #ffffff;
        padding: 25px;
        text-align: center;
        color: #3742fa;
        font-weight: bold;
        font-size: 1.25em;
        margin-top: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)


# --- [화면 1: 메인 홈] ---
if st.session_state['page'] == 'home':
    # 마스코트 이미지 표시 (이미지가 있으면 사용, 없으면 귀여운 텍스트 배너)
    image_filename = 'image_0.png'
    if not os.path.exists(image_filename):
        image_filename = 'image_1.png'  # 다른 이름 대비 예비

    if os.path.exists(image_filename):
        col_l, col_c, col_r = st.columns([1.2, 1.6, 1.2])
        with col_c:
            st.image(image_filename, use_container_width=True)
            st.markdown('<div style="text-align:center; font-size:1.3em; font-weight:800; color:#6c5ce7; margin-top:-10px; margin-bottom:15px;">언제 어디서나 왕긴급한 일에 대비하기 위해선<br>✨ 왕 긴 급! ✨</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="title-banner"><div class="main-title">👼 BIG-GINGEUP!! 🚨</div><div class="slogan">언제 어디서나 왕긴급한 일에 대비하기 위해선<br>✨ 왕 긴 급! ✨</div></div>', unsafe_allow_html=True)

    st.write("")

    # 파스텔 3개 기능 카드
    cols = st.columns(3)

    # 1. 자동 긴급 전화
    with cols[0]:
        st.markdown('<div class="card-box bg-pink"><div class="card-icon">📞💖</div><div class="card-title title-pink">자동 긴급 전화</div><div class="card-desc">긴급상황 시 보호자와 구조대에게 바로 신고해요!</div></div>', unsafe_allow_html=True)
        if st.button("🚨 긴급 신고하기", key="go_call"):
            st.session_state['page'] = 'call'
            st.rerun()

    # 2. 주변 위험 감지
    with cols[1]:
        st.markdown('<div class="card-box bg-yellow"><div class="card-icon">📡✨</div><div class="card-title title-yellow">주변 위험 감지</div><div class="card-desc">주변 장애물을 센서를 통해 감지해서 안전을 지켜요!</div></div>', unsafe_allow_html=True)
        if st.button("⚠️ 위험 확인하기", key="go_detect"):
            st.session_state['page'] = 'detect'
            st.rerun()

    # 3. 안전한 길 안내
    with cols[2]:
        st.markdown('<div class="card-box bg-blue"><div class="card-icon">🗺️🧸</div><div class="card-title title-blue">안전한 길 안내</div><div class="card-desc">안전한 길로만 안내하여 안심 보행을 도와요!</div></div>', unsafe_allow_html=True)
        if st.button("🚶 길 안내받기", key="go_path"):
            st.session_state['page'] = 'path'
            st.rerun()

    st.divider()
    st.caption("💖 빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전하고 행복한 일상을 응원합니다.")


# --- [화면 2: 자동 긴급 전화] ---
elif st.session_state['page'] == 'call':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("👈 메인으로 돌아가기", key="back_home1"):
        st.session_state['page'] = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("📞 귀여운 수호천사 긴급 전화")
    st.write("위급할 때 주저하지 말고 아래 큰 버튼을 눌러주세요!")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.error("### 🚑 119 긴급 구조대")
        st.write("버튼을 누르면 119 구조대로 즉시 전화가 연결됩니다.")
        st.markdown('<a href="tel:119" style="display:inline-block; background-color:#ff4757; color:white; padding:18px 35px; border-radius:20px; font-size:1.4em; font-weight:800; text-decoration:none; box-shadow:0 4px 10px rgba(0,0,0,0.1);">📞 119 바로 전화걸기</a>', unsafe_allow_html=True)

    with col2:
        st.warning("### 👨‍👩‍👧‍👦 보호자 비상 알림")
        phone_num = st.text_input("보호자 연락처 입력:", "010-1234-5678")
        if st.button("💬 SOS 안심 문자 보내기"):
            st.success(f"🌸 [{phone_num}] 번호로 위치 정보와 함께 긴급 SOS가 보내졌습니다!")

    st.info("💡 **안내:** 등록해둔 연락처로 어르신의 현재 위치가 함께 전달됩니다.")


# --- [화면 3: 주변 위험 감지] ---
elif st.session_state['page'] == 'detect':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("👈 메인으로 돌아가기", key="back_home2"):
        st.session_state['page'] = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("📡 반짝반짝 주변 위험 감지기")
    st.write("스마트 센서가 걸어가시는 길 앞의 장애물을 살펴드립니다.")
    st.divider()

    st.subheader("🔍 현재 보행 센서 상태")
    
    if st.button("⚡ 주변 센서 다시 스캔하기"):
        st.success("✨ 주변 레이더 센서가 아주 잘 작동하고 있어요!")

    st.write("")
    
    c1, c2 = st.columns(2)
    with c1:
        st.warning("⚠️ **전방 감지 결과**\n\n앞쪽 1.5m 지점에 작은 문턱이 있어요. 걸림에 주의하세요! 🦶")
    with c2:
        st.info("🌈 **양옆 감지 결과**\n\n좌우 보행로는 깨끗하고 안전합니다! 편안하게 걸으세요 😊")


# --- [화면 4: 안전한 길 안내] ---
elif st.session_state['page'] == 'path':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("👈 메인으로 돌아가기", key="back_home3"):
        st.session_state['page'] = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("🗺️ 안심 안전 보행 길 안내")
    st.write("계단이나 가파른 언덕이 없는 평탄한 안심 길만 골라드려요!")
    st.divider()

    dest = st.text_input("가고 싶으신 곳을 적어주세요:", "경로당")
    
    if st.button("🔍 가장 안전한 길 찾기", key="search_path"):
        st.success(f"🌸 **'{dest}'**(으)로 가는 무장애(Barrier-Free) 최적 경로를 찾았어요!", icon="🍀")
        st.markdown(f'<div class="mock-map">📍 <b>[안심 보행 지도]</b><br><br>• 목적지: {dest}<br>• 예상 걸음: 편안한 도보 약 12분<br>• 길 특징: 계단 없음 🚫 / 높은 턱 없음 🚫 / 넓은 보도블록 🟢</div>', unsafe_allow_html=True)
        
        st.write("")
        st.link_button(f"🔗 카카오맵으로 '{dest}' 큰 지도 보기", f"https://map.kakao.com/?q={dest}")
