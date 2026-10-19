import re
from urllib.parse import quote
import streamlit as st

# 1. 페이지 기본 설정 (모바일 최적화)
st.set_page_config(
    page_title="장애 노인 맞춤형 자동 긴급 전화",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. 세션 상태 초기화
if "guardian_name" not in st.session_state:
    st.session_state.guardian_name = ""
if "guardian_phone" not in st.session_state:
    st.session_state.guardian_phone = ""
if "user_location" not in st.session_state:
    st.session_state.user_location = ""
if "user_situation" not in st.session_state:
    st.session_state.user_situation = ""

# 3. 이미지 스케치 스타일 반영 커스텀 CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EBF3FA;
        color: #1E293B;
    }
    .main-box {
        background-color: #D6E8F7;
        border: 2px solid #5B8FB9;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        font-size: 32px;
        font-weight: 900;
        color: #1B365D;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sub-banner {
        background-color: #FFFFFF;
        border: 3px solid #E63946;
        border-radius: 15px;
        padding: 18px;
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        color: #B91C1C;
        margin-bottom: 25px;
        position: relative;
    }
    .star-icon {
        color: #F59E0B;
        font-size: 30px;
        margin-right: 8px;
    }
    .speech-bubble {
        background: #FFFFFF;
        border: 2px solid #475569;
        border-radius: 20px;
        padding: 15px 20px;
        font-size: 20px;
        font-weight: 700;
        color: #334155;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.08);
    }
    a.call-btn-112 {
        display: block;
        background-color: #1D4ED8;
        color: white !important;
        text-align: center;
        padding: 22px;
        font-size: 28px;
        font-weight: 900;
        border-radius: 16px;
        text-decoration: none !important;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    a.call-btn-119 {
        display: block;
        background-color: #DC2626;
        color: white !important;
        text-align: center;
        padding: 22px;
        font-size: 28px;
        font-weight: 900;
        border-radius: 16px;
        text-decoration: none !important;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    a.call-btn-guardian {
        display: block;
        background-color: #15803D;
        color: white !important;
        text-align: center;
        padding: 22px;
        font-size: 26px;
        font-weight: 900;
        border-radius: 16px;
        text-decoration: none !important;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    a.sms-btn {
        display: block;
        background-color: #4B5563;
        color: white !important;
        text-align: center;
        padding: 18px;
        font-size: 22px;
        font-weight: 800;
        border-radius: 12px;
        text-decoration: none !important;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 4. 유틸리티 함수
def normalize_phone(phone):
    cleaned = re.sub(r"[^0-9]", "", phone or "")
    return cleaned if len(cleaned) >= 8 else ""

def get_sms_link(phone, msg):
    return f"sms:{phone}?body={quote(msg)}"

# --- 메인 화면 시작 ---

# 이미지 상단 박스 "자동 긴급 전화"
st.markdown('<div class="main-box">🚨 자동 긴급 전화</div>', unsafe_allow_html=True)

# 이미지 중앙 붉은 테두리 상자 "★ 112, 119, 보호자에게 자동 전화"
st.markdown(
    '<div class="sub-banner"><span class="star-icon">⭐</span>112, 119, 보호자에게 자동 전화</div>',
    unsafe_allow_html=True,
)

# 이미지 하단 말풍선 안내 메시지
st.markdown(
    '<div class="speech-bubble">🗣️ "도움이 필요한 긴급상황시 전화가 가는 자동 긴급 전화!"<br><small style="color:#64748B; font-weight:normal;">원하시는 버튼을 누르면 전화 통화 화면으로 바로 연결됩니다.</small></div>',
    unsafe_allow_html=True,
)

st.divider()

# 5. 비상 전화 버튼 영역
st.write("### 📞 원클릭 긴급 통화 연결")

st.markdown('<a href="tel:112" class="call-btn-112">🚔 112 경찰 긴급 전화</a>', unsafe_allow_html=True)
st.markdown('<a href="tel:119" class="call-btn-119">🚑 119 구급대 긴급 전화</a>', unsafe_allow_html=True)

if st.session_state.guardian_phone:
    st.markdown(
        f'<a href="tel:{st.session_state.guardian_phone}" class="call-btn-guardian">👨‍👩‍👧 {st.session_state.guardian_name} (보호자) 전화 걸기</a>',
        unsafe_allow_html=True,
    )
    
    # 보호자 SMS 긴급 발신 기능
    sos_message = f"[긴급 SOS 요청]\n위급 상황이 발생했습니다.\n- 위치: {st.session_state.user_location or '미입력'}\n- 상황: {st.session_state.user_situation or '도움 필요'}"
    sms_href = get_sms_link(st.session_state.guardian_phone, sos_message)
    st.markdown(f'<a href="{sms_href}" class="sms-btn">✉️ 보호자에게 위치/상황 SOS 문자 보내기</a>', unsafe_allow_html=True)
else:
    st.info("💡 아래 [보호자 연락처 등록] 양식에서 보호자 번호를 설정하시면 가족 전화 연결 및 SOS 문자 버튼이 생성됩니다.")

st.divider()

# 6. 보호자 연락처 & 위치 정보 설정 양식
st.write("### ⚙️ 보호자 정보 및 위치 설정")

with st.form("settings_form"):
    g_name = st.text_input("보호자 이름/관계", value=st.session_state.guardian_name, placeholder="예: 아들 홍길동")
    g_phone = st.text_input("보호자 전화번호", value=st.session_state.guardian_phone, placeholder="예: 010-1234-5678")
    u_loc = st.text_input("현재 자주 있는 위치 / 주소", value=st.session_state.user_location, placeholder="예: 서울시 종로구 ○○아파트 101호")
    u_sit = st.text_area("특이사항 / 평소 지병", value=st.session_state.user_situation, placeholder="예: 거동 불편, 거통 증상 발생 시 구급차 필요")

    save_btn = st.form_submit_button("설정 정보 저장하기", use_container_width=True)

if save_btn:
    clean_p = normalize_phone(g_phone)
    if g_phone and not clean_p:
        st.error("전화번호 형식이 올바르지 않습니다. 다시 확인해 주세요.")
    else:
        st.session_state.guardian_name = g_name if g_name else "보호자"
        st.session_state.guardian_phone = clean_p
        st.session_state.user_location = u_loc
        st.session_state.user_situation = u_sit
        st.success("보호자 정보 및 상황 정보가 저장되었습니다.")
        st.rerun()

st.caption("🔒 모든 정보는 단말기(세션)에만 전송되며 외부 서버에 별도로 저장되지 않아 안전합니다.")
