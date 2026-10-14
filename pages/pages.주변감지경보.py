
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="안전 동행",
    page_icon="🦯",
    layout="centered"
)

st.title("🦯 안전 동행")
st.header("어르신 보행 안전 도우미")

st.markdown("""
<style>
.stApp {
    font-size: 22px;
}
div.stButton > button {
    width: 100%;
    min-height: 65px;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.subheader("🚨 주변 위험 안내")

st.info(
    "이 앱은 보행 안전을 돕는 시제품입니다. "
    "현재 주변 위험을 자동으로 확인하려면 "
    "실제 위치 및 위험 정보 데이터가 필요합니다."
)

# 사용자가 확인한 위험 정보 입력
danger = st.selectbox(
    "주변에서 확인한 상황을 선택하세요.",
    [
        "특이 사항 없음",
        "공사 구역",
        "보도 위 장애물",
        "차량 통행 주의",
        "보행로 파손",
        "기타 위험"
    ]
)

if st.button("위험 여부 확인"):
    if danger == "특이 사항 없음":
        st.success("선택한 항목에 위험 정보가 없습니다.")
        st.write("이 결과가 실제 주변의 안전을 보장하지는 않습니다.")
    else:
        st.error("⚠️ 주의하세요!")
        st.markdown(f"## {danger}")
        st.write("주변을 살피고 안전한 경로를 이용하세요.")

        components.html("""
        <button onclick="playAlarm()"
            style="font-size:24px;padding:18px;width:100%">
            🔊 경보음 재생
        </button>
        <script>
        function playAlarm() {
            const audio = new AudioContext();
            const oscillator = audio.createOscillator();
            const gain = audio.createGain();
            oscillator.connect(gain);
            gain.connect(audio.destination);
            oscillator.frequency.value = 880;
            gain.gain.value = 0.2;
            oscillator.start();
            oscillator.stop(audio.currentTime + 0.7);
        }
        </script>
        """, height=100)

st.divider()
st.caption(
    "안전 동행 | 어르신의 안전한 보행을 돕기 위한 보조 도구"
)
