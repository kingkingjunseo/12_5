좋아\! 기존 SafeCall 앱의 기본 구조는 유지하면서, 장애가 있는 노인도 쉽게 사용할 수 있도록 화면과 기능을 바꿔 줄게. 큰 글씨, 단순한 화면, 명확한 안내, 보호자 연락 기능을 중심으로 설계했어.

# 🚨 SafeCall Senior — 어르신 맞춤형 긴급 도움 앱

## 1. 앱 기획 및 화면 구성

# 안심 도움 센터

어르신을 위한 쉬운 긴급 연락

# 긴급 도움 요청

어려우시면 아래 전화 버튼을 눌러 주세요.

## 112 경찰

위험할 때

## 119 구급

아프거나 다쳤을 때

## 👨‍👩‍👧 보호자에게 전화

가족이나 돌봄 담당자에게 연락

큰 글씨와 높은 대비

시력이 좋지 않은 어르신도 읽기 쉽게

누르기 쉬운 큰 버튼

손 떨림이나 운동 장애를 고려한 간단한 조작

쉬운 안내와 보호자 문자

짧은 문장으로 상황을 설명하고 도움 요청

## 2. `app.py`

아래 코드는 기존 버전을 어르신 맞춤형으로 수정한 완성본이야. 별도의 AI API나 데이터베이스 없이 실행할 수 있어.

주요 변경점은 다음과 같아.

- 글씨 크기를 조절하는 기능
- 큰 버튼과 단순한 화면 구성
- 112·119·보호자 전화 연결
- 보호자에게 보낼 긴급 문자 작성
- 현재 위치와 상황을 입력하는 기능
- 화면에 표시되는 정보를 읽기 쉽게 구성

python
```

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
# 화면 설정
# -----------------------------
st.session_state.setdefault("font_size", "큼")
st.session_state.setdefault("guardian_name", "")
st.session_state.setdefault("guardian_phone", "")
st.session_state.setdefault("location", "")
st.session_state.setdefault("situation", "")
st.session_state.setdefault("show_sos", False)

FONT_SIZES = {
    "보통": "20px",
    "큼": "25px",
    "아주 큼": "30px",
}

font_size = FONT_SIZES[st.session_state.font_size]

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
    .info-card {{
        padding: 18px;
        border-radius: 16px;
        margin: 12px 0;
        background: #FFFFFF;
        border: 2px solid #CBD5E1;
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
# 유틸리티
# -----------------------------
def normalize_phone(phone):
    phone = (phone or "").strip()
    cleaned = re.sub(r"[^0-9+]", "", phone)

    if not cleaned:
        return ""

    if cleaned.count("+") > 1:
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
# 상단
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
    '<a class="call-link police" href="tel:112">'
    '🚔 112 경찰에 전화하기</a>',
    unsafe_allow_html=True,
)

st.markdown(
    '<a class="call-link rescue" href="tel:119">'
    '🚑 119 구급대에 전화하기</a>',
    unsafe_allow_html=True,
)

st.caption(
    "전화 버튼을 누르면 기기에 따라 통화 앱 또는 "
    "통화 확인 화면이 열립니다."
)

# -----------------------------
# 보호자 설정
# -----------------------------
st.divider()
st.write("## 👨‍👩‍👧 보호자 연락처")

with st.form("guardian_form"):
    st.text_input(
        "보호자 이름",
        key="guardian_name_input",
        placeholder="예: 아들 홍길동",
        max_chars=50,
    )
    st.text_input(
        "보호자 전화번호",
        key="guardian_phone_input",
        placeholder="예: 010-1234-5678",
        max_chars=25,
    )

    st.form_submit_button(
        "보호자 정보 저장",
        use_container_width=True,
    )

    # 폼 제출 시 값은 세션 상태에 보관됩니다.
    # 아래 처리는 폼 밖에서 실행합니다.

if "guardian_name_input" in st.session_state:
    current_name = st.session_state.guardian_name_input
    current_phone = st.session_state.guardian_phone_input

    # 저장 버튼 제출 여부를 별도로 추적합니다.
    # 버튼을 누르지 않아도 입력된 값을 저장한 것으로
    # 취급하지 않도록 별도 제출 상태를 사용합니다.

# Streamlit 폼의 제출 상태를 명시적으로 처리하기 위해
# 일반 버튼 대신 저장 여부를 확인하는 별도 폼을 사용합니다.
# 아래의 연락처 적용 버튼으로 입력을 확정합니다.
if st.button("입력한 보호자 정보 적용", use_container_width=True):
    name = clean_text(
        st.session_state.get("guardian_name_input", ""), 50
    )
    phone = normalize_phone(
        st.session_state.get("guardian_phone_input", "")
    )

    if not name:
        st.error("보호자 이름을 입력해 주세요.")
    elif not phone:
        st.error("보호자 전화번호를 확인해 주세요.")
    else:
        st.session_state.guardian_name = name
        st.session_state.guardian_phone = phone
        st.success("보호자 연락처를 적용했습니다.")

if st.session_state.guardian_phone:
    st.markdown(
        f'<a class="call-link family" '
        f'href="tel:{st.session_state.guardian_phone}">'
        f'📱 {st.session_state.guardian_name}에게 전화하기</a>',
        unsafe_allow_html=True,
    )
else:
    st.info("보호자 정보를 먼저 입력하고 적용해 주세요.")

# -----------------------------
# 위치와 상황
# -----------------------------
st.divider()
st.write("## 📍 현재 위치와 상황")

with st.form("situation_form"):
    st.text_input(
        "현재 위치",
        key="location_input",
        placeholder="예: 서울시 ○○구 ○○아파트",
        max_chars=200,
    )

    st.text_area(
        "어떤 도움이 필요하신가요?",
        key="situation_input",
        placeholder="예: 넘어져서 일어나기 어렵습니다.",
        max_chars=500,
        height=130,
    )

    st.form_submit_button(
        "상황 정보 저장",
        use_container_width=True,
    )

if "location_input" in st.session_state:
    st.session_state.location = clean_text(
        st.session_state.location_input, 200
    )

if "situation_input" in st.session_state:
    st.session_state.situation = clean_text(
        st.session_state.situation_input, 500
    )

# -----------------------------
# SOS
# -----------------------------
st.divider()
st.write("## 🆘 긴급 도움 요청")

st.write(
    "아래 버튼을 누르면 긴급 전화와 보호자 연락 방법을 "
    "한 화면에서 확인할 수 있습니다."
)

if st.button(
    "🚨 긴급 도움 요청 화면 열기",
    type="primary",
    use_container_width=True,
):
    st.session_state.show_sos = True

if st.session_state.show_sos:
    st.error(
        "도움이 필요하면 아래 버튼으로 직접 전화해 주세요."
    )

    st.markdown(
        '<a class="call-link police" href="tel:112">'
        '🚔 112 경찰 전화</a>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<a class="call-link rescue" href="tel:119">'
        '🚑 119 구급대 전화</a>',
        unsafe_allow_html=True,
    )

    phone = st.session_state.guardian_phone
    name = st.session_state.guardian_name

    if phone:
        st.markdown(
            f'<a class="call-link family" href="tel:{phone}">'
            f'📱 {name}에게 전화</a>',
            unsafe_allow_html=True,
        )

        message = (
            "[긴급 도움 요청]\n"
            "도움이 필요합니다. 가능한 한 빨리 연락해 주세요.\n"
            f"위치: {st.session_state.location or '미입력'}\n"
            f"상황: {st.session_state.situation or '미입력'}"
        )

        st.markdown(
            f'<a class="call-link family" '
            f'href="{sms_url(phone, message)}">'
            '✉️ 보호자에게 문자 작성하기</a>',
            unsafe_allow_html=True,
        )

    st.write("### 신고에 사용할 정보")
    st.write(
        f"**위치:** {st.session_state.location or '아직 입력하지 않았습니다.'}"
    )
    st.write(
        f"**상황:** {st.session_state.situation or '아직 입력하지 않았습니다.'}"
    )

    st.info(
        "문자는 자동 전송되지 않습니다. 문자 앱에서 내용을 확인하고 "
        "직접 전송해 주세요."
    )

    if st.button("화면 닫기", use_container_width=True):
        st.session_state.show_sos = False
        st.rerun()

# -----------------------------
# 안전 안내
# -----------------------------
st.divider()
st.write("## ❤️ 꼭 알아두세요")

st.markdown(
    """
    - 이 앱은 자동으로 전화를 걸거나 구조를 요청하지 않습니다.
    - 전화 연결은 사용하는 휴대전화와 브라우저에 따라 다릅니다.
    - 위치를 자동 추적하지 않으므로 주소를 직접 입력해야 합니다.
    - 보호자 정보는 별도 데이터베이스에 저장하지 않습니다.
    - 이 앱은 응급 서비스나 보호자의 응답을 확인할 수 없습니다.
    - 실제 위급 상황에서는 112 또는 119로 직접 연락하세요.
    """
)
```

## 3. `requirements.txt`

text
```

streamlit>=1.40.0,<2.0.0
```

추가 라이브러리는 필요하지 않아.

## 4. Secrets 설정

이 앱은 외부 AI API를 사용하지 않으므로 Secrets 설정은 필요하지 않아. `GEMINI_API_KEY`나 `secrets.toml`도 만들 필요 없어.

## 5. GitHub 업로드 및 배포

1. [GitHub](<https://github.com/?utm_source=chatgpt.com>)에서 `safecall-senior` 저장소를 만들어.
2. 위의 `app.py`와 `requirements.txt`를 저장소 최상위에 올려.
3. [Streamlit Community Cloud](<https://share.streamlit.io/?utm_source=chatgpt.com>)에 GitHub 계정으로 로그인해.
4. `Create app`에서 저장소와 `main` 브랜치를 선택해.
5. Main file path에 `app.py`를 입력하고 `Deploy`를 눌러.

공식 안내: [Streamlit 앱 배포 방법](<https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy?utm_source=chatgpt.com>)

## 6. 중요한 테스트 사항

배포 전 보호자 정보를 입력하고, 글씨 크기 변경, SOS 화면, 전화 링크를 확인해 줘. 전화가 실제로 자동 발신되는 것은 아니며, 문자도 사용자가 직접 전송해야 해.

장애가 있는 어르신을 위한 추가 개선 방향으로는 화면 읽어주기, 음성으로 도움 요청하기, 버튼 오작동 방지, 보호자에게 위치 정보를 안전하게 공유하기 등을 고려할 수 있어. 다만 웹 브라우저만으로 음성 인식이나 백그라운드 긴급 감지를 항상 보장할 수는 없어.
