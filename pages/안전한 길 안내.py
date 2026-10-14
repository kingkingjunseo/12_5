import streamlit as st

st.set_page_config(page_title="안전한 길 안내", page_icon="🚶", layout="centered")

st.title("안전한 길 안내")
st.write("턱, 계단, 장애물 확인을 돕는 웹 앱 프로토타입입니다.")

st.warning(
    "현재 버전은 실제 지도 경로나 도로 장애물 데이터를 조회하지 않습니다. "
    "이동 전 현장 표지와 주변 상황을 확인하세요."
)

with st.form("route_form"):
    start = st.text_input("출발지", placeholder="예: 서울시청")
    destination = st.text_input("도착지", placeholder="예: 경복궁")

    st.subheader("안전 조건")
    avoid_stairs = st.checkbox("계단이 없는 경로 우선", value=True)
    avoid_curbs = st.checkbox("보도 턱과 단차 확인", value=True)
    avoid_obstacles = st.checkbox("공사와 장애물 확인", value=True)
    mobility = st.selectbox("이동 방식", ["휠체어", "유모차", "보행", "기타"])

    submitted = st.form_submit_button("안전 경로 확인")

if submitted:
    if not start.strip() or not destination.strip():
        st.error("출발지와 도착지를 모두 입력해 주세요.")
    else:
        st.success("입력한 경로: " + start.strip() + " -> " + destination.strip())
        st.write("이동 방식: " + mobility)
        st.subheader("이동 전 확인 목록")

        if avoid_stairs:
            st.write("- 계단 대신 경사로나 엘리베이터가 있는지 확인하세요.")
        if avoid_curbs:
            st.write("- 보도 턱과 횡단보도 진입부의 단차를 확인하세요.")
        if avoid_obstacles:
            st.write("- 공사 구간, 적치물, 좁은 통행로가 있는지 확인하세요.")

        st.write("- 횡단보도 신호와 주변 교통 상황을 확인하세요.")
        st.info(
            "이 결과는 실제 길찾기 결과가 아니라 확인용 체크리스트입니다. "
            "실제 안전 경로를 제공하려면 지도 API와 최신 접근성 데이터가 필요합니다."
        )

st.divider()
st.subheader("향후 추가할 기능")
st.write("1. 실제 지도 경로 표시")
st.write("2. 경사로, 계단, 턱, 공사 구간 데이터 연동")
st.write("3. 데이터 출처와 업데이트 시각 표시")
