import re
from urllib.parse import quote
import streamlit as st

st.set_page_config(
    page_title="안심 도움 센터",
    page_icon="🧓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "font_size" not in st.session_state:
    st.session_state.font_size = "큼"
if "guardian_name" not in st.session_state:
    st.session_state.guardian_name = ""
if "guardian_phone" not in st.session_state:
    st.session_state.guardian_phone = ""
if "location" not in st.session_state:
    st.session_state.location = ""
if "situation" not in st.session_state:
    st.session_state.situation = ""
if "show_sos" not in st.session_state:
    st.session_state.show_sos = False

# -----------------------------
# 글씨 크기 CSS 설정
# -----------------------------
FONT_SIZES = {
    "보통": "20px",
    "큼": "25px",
    "아주 큼": "30px",
}

font_size = FONT_SIZES.get(st.session_state.font_size, "25px")

st.markdown(
    f"""
    <style>
    .stApp {{
        background: #F8FAFC;
        color: #172033;
        font-size: {font_size};
    }}
    .block-container {{
        max-width: 760px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}
    h1, h2, h3, p, label, .stMarkdown {{
        line-height: 1.65;
    }}
    h1 {{ font-size: 2.1rem !important; }}
    h2 {{ font-size: 1.7rem !important; }}
    h3 {{ font-size: 1.4rem !important; }}
    p, label, [data-testid="stCaptionContainer"] {{
        font-size: {font_size} !important;
    }}
    div.stButton > button,
    div.stFormSubmitButton > button {{
        width: 100%;
        min-height: 68px;
        font-size: 24px !important;
        font-weight: 800;
        border-radius: 15px;
        border: 2px solid #CBD5E1;
        white-space: normal;
    }}
    div.stButton > button[kind="primary"] {{
        background: #B91C1C;
        color: white;
        border: 2px solid #991B1B;
    }}
    input, textarea {{
        font-size: 22px !important;
    }}
    .warning {{
        padding: 18px;
        border-radius: 14px;
        background: #FEF3C7;
        border: 2px solid #D97706;
        color: #78350F;
        font-size: 21px;
        font-weight: 700;
    }}
    a.call-link {{
        display: block;
        box-sizing: border-box;
        width: 100%;
        text-align: center;
        padding: 20px 12px;
        margin: 12px 0;
        border-radius: 15px;
        color: #FFFFFF !important;
        text-decoration: none !important;
        font-size: 25px;
        font-weight: 800;
        line-height: 1.5;
    }}
    .police {{ background: #B91C1C; }}
    .rescue {{ background: #1D4ED8; }}
    .family {{ background: #047857; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 유틸리티 함수
# -----------------------------
def normalize_phone(phone):
    phone = (phone or "").strip()
    cleaned = re.sub(r"[^0-9+]", "", phone)

    if not cleaned or cleaned.count("+") > 1:
        return ""
    if "+" in cleaned and not cleaned.startswith("+"):
        return ""

    digits = cleaned.replace("+", "")
    if not digits.isdigit() or not (8 <= len(digits) <= 15):
        return ""

    return cleaned

def clean_text(value, limit=300):
    return (value or "").strip()[:limit]

def sms_url(phone, message):
    return f"sms:{phone}?body={quote(message, safe='')}"

# -----------------------------
# 메인 상단 화면
# -----------------------------
st.title("🧓 안심 도움 센터")
st.subheader("어르신을 위한 쉬운 긴급 연락")

st.markdown(
    """
    <div class="warning">
    🚨 지금 위험하거나 많이 아프신가요?<br>
    아래의 112 또는 119 버튼을 눌러 주세요.<br>
    실제 위급 상황에서는 설정을 기다리지 마세요.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("### 🔠 글씨 크기")
st.selectbox(
    "읽기 편한 크기를 선택하세요.",
    options=["보통", "큼", "아주 큼"],
    key="font_size",
)

# -----------------------------
# 긴급 전화
# -----------------------------
st.write("## 📞 긴급 전화")

st.markdown(
    '<a class="call-link police" href="tel:112">🚔 112 경찰에 전화하기</a>',
    unsafe_allow_html=True,
)

st.markdown(
    '<a class="call-link rescue" href="tel:119">🚑 119 구급대에 전화하기</a>',
    unsafe_allow_html=True,
)

st.caption("전화 버튼을 누르면 통화 앱 또는 통화 확인 화면이 열립니다.")

# -----------------------------
# 보호자 설정 (Form 처리 수정)
# -----------------------------
st.divider()
st.write("## 👨‍👩‍👧 보호자 연락처")

with st.form("guardian_form"):
    g_name = st.text_input(
        "보호자 이름",
        value=st.session_state.guardian_name,
        placeholder="예: 아들 홍길동",
        max_chars=50,
    )
    g_phone = st.text_input(
        "보호자 전화번호",
        value=st.session_state.guardian_phone,
        placeholder="예: 010-1234-5678",
        max_chars=25,
    )

    submitted_guardian = st.form_submit_button("보호자 정보 저장", use_container_width=True)

if submitted_guardian:
    name_clean = clean_text(g_name, 50)
    phone_clean = normalize_phone(g_phone)

    if not name_clean:
        st.error("보호자 이름을 입력해 주세요.")
    elif not phone_clean:
        st.error("보호자 전화번호를 올바르게 확인해 주세요. (예: 010-1234-5678)")
    else:
        st.session_state.guardian_name = name_clean
        st.session_state.guardian_phone = phone_clean
        st.success("보호자 연락처가 성공적으로 저장되었습니다.")

if st.session_state.guardian_phone:
    st.markdown(
        f'<a class="call-link family" href="tel:{st.session_state.guardian_phone}">'
        f'📱 {st.session_state.guardian_name}에게 전화하기</a>',
        unsafe_allow_html=True,
    )
else:
    st.info("위 양식에 보호자 정보를 입력하고 저장 버튼을 눌러주세요.")

# -----------------------------
# 위치 및 상황 입력 (Form 처리 수정)
# -----------------------------
st.divider()
st.write("## 📍 현재 위치와 상황")

with st.form("situation_
