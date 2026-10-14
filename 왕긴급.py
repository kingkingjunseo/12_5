import streamlit as st
st.title('왕긴급')
st.write('왕 긴급 상황이신가요?')

import streamlit as st
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 왕긴급 커스텀 디자인
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="왕긴급 - 1초 긴급 대응 포털",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for King Emergency
st.markdown("""
<style>
    .stApp {
        background-color: #FAFAFA;
    }
    .main-header {
        font-size: 2.3rem;
        font-weight: 900;
        color: #D32F2F;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #424242;
        margin-bottom: 20px;
    }
    .sos-btn {
        display: inline-block;
        width: 100%;
        padding: 15px;
        background-color: #D32F2F;
        color: white !important;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        border-radius: 10px;
        text-decoration: none;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sos-btn-police {
        background-color: #1976D2;
    }
    .emergency-card {
        background-color: #FFEBEE;
        border-left: 6px solid #D32F2F;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Gemini API 설정 (예외 처리 포함)
# -----------------------------------------------------------------------------
@st.cache_resource
def get_gemini_model():
    """Gemini API 키 검증 및 모델 객체 반환"""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return None, "Secret에 'GEMINI_API_KEY'가 설정되지 않았습니다."
        
        genai.configure(api_key=api_key)
        # 요구사항 지정 모델 사용
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        return model, None
    except Exception as e:
        return None, f"API 초기화 오류: {str(e)}"

# -----------------------------------------------------------------------------
# 3. 사이드바 - [기능 1] 자동 긴급 전화 원클릭 연결
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📞 1. 원클릭 긴급 전화")
    st.error("위급 시 버튼을 누르면 전화 앱으로 즉시 연결됩니다.")
    
    st.markdown('<a href="tel:119" class="sos-btn">🚑 119 (소방 / 구급)</a>', unsafe_allow_html=True)
    st.markdown('<a href="tel:112" class="sos-btn sos-btn-police">POLICE 112 (경찰청)</a>', unsafe_allow_html=True)
    
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.markdown('<a href="tel:122" style="display:block; text-align:center; padding:10px; background:#424242; color:white; border-radius:5px; text-decoration:none; font-weight:bold;">⚓ 122 해양</a>', unsafe_allow_html=True)
    with col_sub2:
        st.markdown('<a href="tel:110" style="display:block; text-align:center; padding:10px; background:#424242; color:white; border-radius:5px; text-decoration:none; font-weight:bold;">📢 110 재난</a>', unsafe_allow_html=True)

    st.divider()
    st.caption("📱 **내 위치 문자 전송 템플릿**")
    my_loc = st.text_input("현재 위치", placeholder="예: 천안시 동남구 단국대 병원 근처")
    my_stat = st.text_input("현재 상태", placeholder="예: 낙상으로 다리 부상")
    sos_txt = f"[왕긴급 SOS]\n위치: {my_loc if my_loc else '위치미입력'}\n상황: {my_stat if my_stat else '긴급 구조 필요'}"
    st.text_area("복사용 텍스트", value=sos_txt, height=80)

# -----------------------------------------------------------------------------
# 4. 메인 화면 헤더
# -----------------------------------------------------------------------------
st.markdown("<p class='main-header'>🚨 왕긴급 (King Emergency)</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>1초가 시급한 골든타임! 자동 전화, 사이렌 경보, 응급실 길안내를 단 한 화면에서 작동하세요.</p>", unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 5. [기능 2] 주변 감지 경보 (SOS 사이렌)
# -----------------------------------------------------------------------------
st.markdown("### 🔔 2. 주변 감지 경보 (SOS 사이렌)")
st.write("붕괴, 매몰, 야간 침입 등 주변에 나의 존재와 위치를 소리로 크게 알려야 할 때 사용하세요.")

col_siren1, col_siren2 = st.columns([1, 2])

with col_siren1:
    siren_active = st.toggle("🚨 SOS 사이렌 소리 울리기", value=False)

with col_siren2:
    if siren_active:
        st.warning("🔊 사이렌 소리가 고음량으로 재생 중입니다! (주변에 위험 신호 전달 중)")
        # 내장된 웹 오디오 경보음 재생 (Base64/HTML5 Audio)
        st.components.v1.html("""
            <audio autoplay loop>
              <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
              사용 중인 브라우저가 오디오 재생을 지원하지 않습니다.
            </audio>
        """, height=50)
    else:
        st.info("토글을 켜면 고음역 경보 오디오가 연속으로 반복 재생됩니다.")

st.divider()

# -----------------------------------------------------------------------------
# 6. [기능 3] 주변 응급실 및 길안내
# -----------------------------------------------------------------------------
st.markdown("### 🗺️ 3. 응급실 빠른 길안내")
st.write("가장 가까운 응급의료센터를 확인하고 지도로 즉시 길안내를 받으세요.")

col_map1, col_map2, col_map3 = st.columns(3)

with col_map1:
    st.subheader("🏥 단국대학교병원")
    st.caption("📍 충청남도 천안시 동남구 망향로 201")
    st.markdown("[🗺️ 지도 앱으로 길안내 받기](https://maps.google.com/?cid=3778887737401261236)")

with col_map2:
    st.subheader("🏥 순천향대 천안병원")
    st.caption("📍 충청남도 천안시 동남구 순천향6길 31")
    st.markdown("[🗺️ 지도 앱으로 길안내 받기](https://maps.google.com/?cid=15165962927987570233)")

with col_map3:
    st.subheader("🏥 천안충무병원")
    st.caption("📍 충청남도 천안시 서북구 다가말3길 8")
    st.markdown("[🗺️ 지도 앱으로 길안내 받기](https://maps.google.com/?cid=1639249207143883510)")

st.divider()

# -----------------------------------------------------------------------------
# 7. 추가 AI 기능: Gemini AI 왕긴급 해결사 (gemini-2.5-flash-lite)
# -----------------------------------------------------------------------------
st.markdown("### 🤖 4. 왕긴급 AI 대처 가이드")
st.write("특수한 응급 상황 발생 시 AI에게 즉시 최우선 조치 사항을 물어보세요.")

model, err_msg = get_gemini_model()

if err_msg and not st.secrets.get("GEMINI_API_KEY"):
    st.info("💡 **안내**: AI 응급 지침을 확인하려면 Streamlit Secrets에 `GEMINI_API_KEY`를 설정하세요.")

col_q1, col_q2, col_q3 = st.columns(3)
quick_query = ""
if col_q1.button("🍖 기도 막힘 (하임리히법)"):
    quick_query = "음식물이 목에 걸려 숨을 못 쉴 때 응급처치"
if col_q2.button("☕ 심한 화상 처리"):
    quick_query = "뜨거운 물에 심하게 데였을 때 처리법"
if col_q3.button("🩸 깊은 출혈 지혈"):
    quick_query = "피가 많이 나는 상처 지혈법"

user_query = st.text_input("질문할 상황 입력:", value=quick_query, placeholder="예: 화학물질이 눈에 들어갔을 때")

if st.button("🚨 AI 긴급 행동지침 보기", type="primary"):
    if not user_query.strip():
        st.warning("상황을 입력해 주세요.")
    elif not model:
        st.error(f"AI 기능을 불러올 수 없습니다: {err_msg}")
    else:
        with st.spinner("왕긴급 AI 분석 중..."):
            try:
                prompt = f"""
                당신은 응급구조 전문가 '왕긴급 AI'입니다.
                다음 긴급 상황에 대해 즉시 취해야 할 3가지 단계별 행동지침을 작성하세요.

                상황: {user_query}

                [작성 규칙]
                1. 가장 중요한 최우선 조치를 첫 번째에 두껍게 표시.
                2. 절대로 해서는 안 되는 금지사항 1가지 명시.
                3. 답변은 3줄 내외로 아주 짧고 직관적으로 작성.
                4. "위급 상황 시 즉시 119로 연락하세요" 필수 포함.
                """
                response = model.generate_content(prompt)
                
                st.markdown("<div class='emergency-card'>", unsafe_allow_html=True)
                st.markdown("####
