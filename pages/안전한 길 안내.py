
import streamlit as st

st.set_page_config(
    page_title="무장애 길 안내",
    page_icon="♿",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }
    div[data-testid="stMetric"] {
        background: #f0f7f4;
        border: 1px solid #d8e9e1;
        border-radius: 12px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("♿ 무장애 길 안내")
st.write("이동할 장소를 기록하고, 이동 경로의 접근성 정보를 확인해 보세요.")

# 세션 상태 초기화
if "route_saved" not in st.session_state:
    st.session_state.route_saved = False

if "checks" not in st.session_state:
    st.session_state.checks = {}

# 장소 입력
st.subheader("📍 이동 정보")

with st.form("route_form"):
    col1, col2 = st.columns(2)

    with col1:
        start = st.text_input(
            "출발지",
            placeholder="예: 학교 정문",
        )

    with col2:
        destination = st.text_input(
            "도착지",
            placeholder="예: 도서관 입구",
        )

    route_notes = st.text_area(
        "경로 설명",
        placeholder="예: 정문에서 오른쪽으로 이동한 뒤 경사로를 이용합니다.",
        height=100,
    )

    submitted = st.form_submit_button(
        "이동 정보 저장",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if not start.strip() or not destination.strip():
        st.warning("출발지와 도착지를 모두 입력해 주세요.")
    elif start.strip() == destination.strip():
        st.warning("출발지와 도착지를 다르게 입력해 주세요.")
    else:
        st.session_state.start = start.strip()
        st.session_state.destination = destination.strip()
        st.session_state.route_notes = route_notes.strip()
        st.session_state.route_saved = True
        st.session_state.checks = {}
        st.success("이동 정보를 저장했어요.")

# 이동 정보 표시
if st.session_state.route_saved:
    st.divider()
    st.subheader("🧭 나의 이동 경로")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("출발지", st.session_state.start)
    with col2:
        st.metric("도착지", st.session_state.destination)

    if st.session_state.route_notes:
        st.info(st.session_state.route_notes)

    st.caption(
        "이 화면은 사용자가 입력한 경로 설명을 표시합니다. "
        "실제 지도 경로를 자동으로 계산하지는 않습니다."
    )

# 접근성 체크리스트
st.divider()
st.subheader("✅ 무장애 환경 체크리스트")
st.write("이동 전에 각 항목을 확인하고 체크하세요.")

items = [
    ("턱", "이동 경로에 높은 턱이나 단차가 없는지"),
    ("경사로", "경사로가 있고 안전하게 이용할 수 있는지"),
    ("계단", "계단을 피할 수 있는 대체 경로가 있는지"),
    ("보도", "보행로가 충분히 넓고 장애물이 없는지"),
    ("엘리베이터", "필요한 엘리베이터가 이용 가능한지"),
    ("횡단보도", "횡단보도와 보행 신호를 이용할 수 있는지"),
    ("공사", "공사나 임시 통행 제한이 있는지"),
    ("바닥", "바닥이 미끄럽거나 파손된 곳이 없는지"),
]

for key, description in items:
    st.session_state.checks.setdefault(key, False)

    st.session_state.checks[key] = st.checkbox(
        f"**{key}** — {description}",
        value=st.session_state.checks[key],
        key=f"check_{key}",
    )

checked = sum(st.session_state.checks.values())
total = len(items)

st.progress(checked / total)
st.write(f"확인 완료: **{checked}/{total}개**")

if checked == total:
    st.success("모든 항목을 확인했어요. 출발 전 현장 상황도 확인해 주세요.")
elif checked >= 5:
    st.info("대부분 확인했어요. 남은 항목도 확인해 보세요.")
else:
    st.caption("체크리스트는 실제 현장 점검을 대신하지 않습니다.")

# 사용자 경로 메모
st.divider()
st.subheader("📝 추가 메모")

extra_notes = st.text_area(
    "추가로 기록할 내용",
    placeholder="예: 정문 오른쪽에 경사로가 있음",
    key="extra_notes",
)

if st.button("메모 확인"):
    if extra_notes.strip():
        st.text_area(
            "작성한 메모",
            value=extra_notes,
            height=100,
            disabled=True,
        )
    else:
        st.warning("먼저 메모를 입력해 주세요.")

# 초기화
st.divider()

if st.button("전체 기록 초기화"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.caption(
    "무장애 길 안내 도우미 · 외부 API 없이 동작하는 기록 및 점검 앱"
)
