import os
import streamlit as st
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 설정 (모바일 최적화)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="어르신 대중교통 긴급 SOS",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (버튼 크기 극대화 및 시인성 확보)
st.markdown("""
    <style>
    .big-btn-119 {
        display: block;
        width: 100%;
        background-color: #ff4b4b;
        color: white !important;
        text-align: center;
        padding: 22px;
        font-size: 28px;
        font-weight: bold;
        border-radius: 15px;
        text-decoration: none;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .big-btn-112 {
        display: block;
        width: 100%;
        background-color: #1c83e1;
        color: white !important;
        text-align: center;
        padding: 22px;
        font-size: 28px;
        font-weight: bold;
        border-radius: 15px;
        text-decoration: none;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .big-btn-guardian {
        display: block;
        width: 100%;
        background-color: #28a745;
        color: white !important;
        text-align: center;
        padding: 22px;
        font-size: 28px;
        font-weight: bold;
        border-radius: 15px;
        text-decoration: none;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 사이드바 - 보호자 연락처 및 정보 설정
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ 긴급 연락처 설정")
st.sidebar.info("보호자 번호를 미리 등록해 두시면 위급 상황 시 원클릭으로 전화가 걸립니다.")

guardian_phone = st.sidebar.text_input(
    "보호자 전화번호 입력",
    value="010-0000-0000",
    help="'-' 기호 없이 숫자만 입력해도 동작합니다."
)
guardian_phone_clean = guardian_phone.replace("-", "").strip()

# -----------------------------------------------------------------------------
# 3. 메인 화면 - 비상 전화 걸기 (HTML URI Scheme 활용)
# -----------------------------------------------------------------------------
st.title("🚨 어르신 대중교통 긴급 SOS")
st.caption("위급 상황 시 아래 버튼을 누르면 전화 걸기 화면으로 즉시 이동합니다.")

st.subheader("1. 즉시 전화 걸기")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '<a href="tel:119" class="big-btn-119">🚑 119 구급대</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<a href="tel:112" class="big-btn-112">police 112 경찰신고</a>',
        unsafe_allow_html=True
    )

if guardian_phone_clean:
    st.markdown(
        f'<a href="tel:{guardian_phone_clean}" class="big-btn-guardian">📞 보호자 전화 연결 ({guardian_phone})</a>',
        unsafe_allow_html=True
    )
else:
    st.warning("사이드바에서 보호자 전화번호를 입력해주세요.")

st.divider()

# -----------------------------------------------------------------------------
# 4. 긴급 메시지 작성 및 위치 전달
# -----------------------------------------------------------------------------
st.subheader("2. 긴급 상황 위치 & SMS 문자 발송")

location_info = st.text_input(
    "현재 타신 대중교통 정보 (버스 번호, 지하철역 등)",
    placeholder="예: 300번 버스 정류장 부근 / 2호선 강남역 승강장"
)

symptom_info = st.text_area(
    "상황 설명 (간단히 입력)",
    placeholder="예: 어지러워서 도움이 필요합니다."
)

# AI 문장 요약 기능 (Gemini 2.5 Flash-Lite)
ai_generated_msg = ""
if st.button("🤖 AI 긴급 신고문 자동 작성하기"):
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    
    if not api_key:
        st.error("Gemini API 키가 설정되지 않았습니다. Secrets 설정을 확인해주세요.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            
            prompt = f"""
            다음 정보를 바탕으로 112, 119 또는 보호자에게 문자로 전송할 매우 명확하고 간결한 긴급 SOS 메시지를 작성해줘.
            - 현재 위치/대중교통: {location_info if location_info else '위치 미입력'}
            - 증상 및 상황: {symptom_info if symptom_info else '응급 상황 발생'}
            
            [조건]
            1. 첫 줄에 [긴급 SOS 요청] 명시
            2. 3문장 이내로 핵심만 전달
            3. 경어체 사용
            """
            
            with st.spinner("AI가 신고 문장을 작성 중입니다..."):
                response = model.generate_content(prompt)
                ai_generated_msg = response.text
                st.success("신고 문장 작성 완료!")
                st.text_area("생성된 긴급 메시지", value=ai_generated_msg, height=120)
        except Exception as e:
            st.error(f"AI 문장 생성 중 오류가 발생했습니다: {str(e)}")

# SMS 문장 조합 및 전송 링크 생성
default_msg = f"[긴급 SOS] 도움이 필요합니다.\n위치: {location_info if location_info else '미입력'}\n상황: {symptom_info if symptom_info else '위급 상황'}"
final_sms_text = ai_generated_msg if ai_generated_msg else default_msg

if guardian_phone_clean:
    import urllib.parse
    encoded_sms = urllib.parse.quote(final_sms_text)
    sms_link = f"sms:{guardian_phone_clean}?body={encoded_sms}"
    
    st.markdown(
        f'<a href="{sms_link}" style="display:inline-block; padding:12px 20px; background-color:#6c757d; color:white; text-decoration:none; border-radius:8px; font-weight:bold;">💬 보호자에게 긴급 문자 전송하기</a>',
        unsafe_allow_html=True
    )

st.divider()
st.caption("💡 참고: 버튼을 누르면 스마트폰의 통화/문자 앱으로 연결되며, 실제 통화 버튼이나 전송 버튼을 누르셔야 연결이 완료됩니다.")
