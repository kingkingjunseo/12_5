streamlit>=1.32,<2.0
import streamlit as st

st.set_page_config(
    page_title="안전한 길 안내",
    page_icon="🚶",
    layout="centered",
)

st.title("🚶 안전한 길 안내")
st.write("턱·계단·장애물 정보를 고려한 이동을 돕는 웹 앱 프로토타입입니다.")

st.warning(
    "현재 데모는 실제 길찾기나 도로 장애물 데이터를 조회하지 않습니다. "
    "이동 전 현장 표지와 주변 상황을 반드시 확인하세요."
)

with st.form("route_form"):
    start = st.text_input("출발지", placeholder="예: 서울시청")
    destination = st.text_input("도착지", placeholder="예: 경복궁")

    st.subheader("안전 조건")
    avoid_stairs = st.checkbox("계단이 없는 경로 우선", value=True)
    avoid_curbs = st.checkbox("보도 턱·단차 확인", value=True)
    avoid_obstacles = st.checkbox("공사·장애물 확인", value=True)
    mobility = st.selectbox("이동 방식", ["휠체어", "유모차", "보행", "기타"])

    submitted = st.form_submit_button("안전 경로 확인", use_container_width=True)

if submitted:
    if not start.strip() or not destination.strip():
        st.error("출발지와 도착지를 모두 입력해 주세요.")
    else:
        st.success(f"입력한 경로: {start.strip()} → {destination.strip()}")
        st.write(f"이동 방식: **{mobility}**")
        st.subheader("이동 전 확인 목록")

        items = []
        if avoid_stairs:
            items.append("계단 대신 경사로 또는 엘리베이터가 있는지 확인하세요.")
        if avoid_curbs:
            items.append("보도 턱과 횡단보도 진입부의 단차를 확인하세요.")
        if avoid_obstacles:
            items.append("공사 구간, 적치물, 좁은 통행로가 있는지 확인하세요.")
        items.append("횡단보도 신호와 주변 교통 상황을 확인하세요.")

        for item in items:
            st.markdown(f"- {item}")

        st.info(
            "아직 실제 지도 경로를 계산한 결과가 아닙니다. "
            "이 버전은 입력과 안전 체크리스트를 보여 주는 데모입니다."
        )

st.divider()
st.subheader("이 앱의 다음 개발 단계")
st.markdown(
    "- 지도 API를 연결해 실제 경로 표시\n"
    "- 경사로·계단·보도 턱·공사 구간 데이터 연동\n"
    "- 정보 출처와 마지막 업데이트 시각 표시"
)
st.caption("웨일OS 호환: 최신 브라우저에서 웹 주소로 접속하는 방식")
