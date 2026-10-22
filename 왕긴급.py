
import streamlit as st
from pathlib import Path

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급!",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "pages"

# 2. 파스텔톤 커스텀 CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fffaf0;
        font-family: 'Malgun Gothic', 'Nanum Gothic', sans-serif;
    }

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
        margin-bottom: 8px;
    }

    .card-box {
        border-radius: 25px;
        padding: 22px 15px;
        text-align: center;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
        border: 4px solid #ffffff;
        min-height: 230px;
    }

    .card-icon {
        font-size: 3.5em;
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 1.5em;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .card-desc {
        font-size: 1em;
        color: #555555;
        line-height: 1.6;
        font-weight: 600;
    }

    .bg-pink { background-color: #fff0f3; }
    .title-pink { color: #ff4757; }

    .bg-yellow { background-color: #fff9db; }
    .title-yellow { color: #d99400; }

    .bg-blue { background-color: #e8f4ff; }
    .title-blue { color: #1e75d8; }

    /* 모든 버튼에 일관된 스타일 적용 */
    div.stButton > button {
        width: 100%;
        min-height: 54px;
        border-radius: 18px;
        font-size: 1.05em;
        font-weight: 800;
        border: 2px solid #ffffff;
        box-shadow: 0 5px 12px rgba(0, 0, 0, 0.08);
        background-color: #ff6b81;
        color: white;
    }

    div.stButton > button:hover {
        border-color: #ffb7c5;
        color: white;
        filter: brightness(0.96);
    }

    div.stButton > button:focus:not(:active) {
        border-color: #ff6b81;
        color: white;
    }

    @media (max-width: 700px) {
        .main-title { font-size: 2em; }
        .card-box { min-height: auto; }
        .card-title { font-size: 1.25em; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 페이지 이동 함수
def safe_switch_page(candidates, feature_name):
    """
    실제 존재하는 페이지 파일만 이동 대상으로 사용한다.
    후보 파일이 없으면 가능한 경로를 안내한다.
    """
    for relative_path in candidates:
        page_path = BASE_DIR / relative_path

        if page_path.is_file():
            try:
                st.switch_page(str(page_path))
                return
            except Exception as exc:
                st.error(
                    f"{feature_name} 페이지를 열지 못했어요. "
                    "파일 이름과 Streamlit 페이지 설정을 확인해 주세요."
                )
                st.caption(f"오류 정보: {exc}")
                return

    expected_paths = "\n".join(
        f"- `{path}`" for path in candidates
    )

    st.error(f"{feature_name} 페이지 파일을 찾을 수 없어요.")
    st.markdown(
        "GitHub 저장소에 다음 경로 중 하나로 파일이 있는지 확인해 주세요."
    )
    st.markdown(expected_paths)


# 4. 마스코트 이미지 표시
# 우선 지정한 파일명을 찾고, 없으면 기본 배너를 표시한다.
image_candidates = [
    "mascot.png",
    "mascot.jpg",
    "mascot.jpeg",
    "character.png",
    "character.jpg",
]

found_image = next(
    (
        BASE_DIR / name
        for name in image_candidates
        if (BASE_DIR / name).is_file()
    ),
    None,
)

if found_image:
    col_l, col_c, col_r = st.columns([1, 2, 1])

    with col_c:
        st.image(str(found_image), use_container_width=True)
else:
    st.markdown(
        """
        <div class="title-banner">
            <div class="main-title">BIG-GINGEUP!! 🚨</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:1.2em;
        font-weight:800;
        color:#57606f;
        margin-bottom:24px;
    ">
        언제 어디서나 왕긴급한 일에 대비하기 위해선
        <br>
        <span style="color:#ff4757;font-size:1.3em;">
            왕 긴 급!
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# 5. 기능 카드
cols = st.columns(3, gap="medium")

# 첫 번째 카드: 긴급 전화
with cols[0]:
    st.markdown(
        """
        <div class="card-box bg-pink">
            <div class="card-icon">📞</div>
            <div class="card-title title-pink">자동 긴급 전화</div>
            <div class="card-desc">
                긴급상황에 대비해<br>
                보호자와 신고 정보를 확인해요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "긴급 신고 바로가기",
        key="btn_call",
        use_container_width=True,
    ):
        safe_switch_page(
            [
                "pages/자동 긴급 전화.py",
                "pages/1_전화.py",
                "자동 긴급 전화.py",
            ],
            "자동 긴급 전화",
        )

# 두 번째 카드: 주변 위험 감지
with cols[1]:
    st.markdown(
        """
        <div class="card-box bg-yellow">
            <div class="card-icon">📡</div>
            <div class="card-title title-yellow">주변 위험 감지</div>
            <div class="card-desc">
                주변 장애물과 위험 요소를<br>
                확인할 수 있도록 도와줘요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "위험 확인 바로가기",
        key="btn_detect",
        use_container_width=True,
    ):
        safe_switch_page(
            [
                "pages/주변감지경보.py",
                "pages/2_감지.py",
                "주변감지경보.py",
            ],
            "주변 위험 감지",
        )

# 세 번째 카드: 안전한 길 안내
with cols[2]:
    st.markdown(
        """
        <div class="card-box bg-blue">
            <div class="card-icon">🗺️</div>
            <div class="card-title title-blue">안전한 길 안내</div>
            <div class="card-desc">
                지도에서 위치를 확인하고<br>
                이동 지점을 기록해요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "길 안내 바로가기",
        key="btn_path",
        use_container_width=True,
    ):
        safe_switch_page(
            [
                "pages/안전한 길 안내.py",
                "pages/3_길안내.py",
                "안전한 길 안내.py",
            ],
            "안전한 길 안내",
        )

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#777;
        font-size:0.9em;
        padding:10px;
    ">
        빅-긴급!! (BIG-GINGEUP)
        <br>
        어르신의 안전한 이동을 돕는 프로젝트
    </div>
    """,
    unsafe_allow_html=True,
)
