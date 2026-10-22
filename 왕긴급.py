
import streamlit as st
from pathlib import Path

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="왕긴급!",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 현재 실행 중인 파이썬 파일의 폴더
BASE_DIR = Path(__file__).resolve().parent


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
        border-radius: 30px;
        padding: 25px 20px 15px 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
        border: 4px solid #ffffff;
        min-height: 225px;
        box-sizing: border-box;
    }

    .card-icon {
        font-size: 4em;
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 1.8em;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .card-desc {
        font-size: 1.05em;
        color: #555555;
        min-height: 50px;
        line-height: 1.5;
        font-weight: 600;
    }

    .bg-pink { background-color: #fff0f3; }
    .title-pink { color: #ff4757; }

    .bg-yellow { background-color: #fff9db; }
    .title-yellow { color: #ffa502; }

    .bg-blue { background-color: #e8f4ff; }
    .title-blue { color: #1e90ff; }

    div.stButton > button {
        width: 100%;
        min-height: 58px;
        border-radius: 22px;
        font-size: 1.1em;
        font-weight: 800;
        padding: 12px 8px;
        border: 3px solid #ffffff;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        border-color: #ffffff;
    }

    /* 각 기능 버튼의 색상 */
    div[data-testid="column"]:nth-child(1)
    div.stButton > button {
        background-color: #ff6b81;
        color: white;
    }

    div[data-testid="column"]:nth-child(2)
    div.stButton > button {
        background-color: #e0b83f;
        color: white;
    }

    div[data-testid="column"]:nth-child(3)
    div.stButton > button {
        background-color: #70a1ff;
        color: white;
    }

    @media (max-width: 768px) {
        .main-title {
            font-size: 2em;
        }

        .card-box {
            padding: 20px 12px;
            min-height: 200px;
        }

        .card-title {
            font-size: 1.35em;
        }

        .card-icon {
            font-size: 3em;
        }

        .card-desc {
            font-size: 0.95em;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 3. 안전한 페이지 이동 함수
def safe_switch_page(relative_path):
    """페이지 파일이 존재하는지 확인한 뒤 이동합니다."""
    page_file = BASE_DIR / relative_path

    if not page_file.is_file():
        st.error(
            f"페이지 파일을 찾을 수 없습니다: {relative_path}"
        )
        st.info(
            "GitHub 저장소에서 파일 이름과 폴더 위치를 확인해 주세요."
        )
        return

    try:
        # Streamlit 페이지 경로는 메인 스크립트 기준 상대 경로
        st.switch_page(relative_path)
    except Exception as exc:
        st.error(f"페이지 이동 중 오류가 발생했습니다: {exc}")


# 4. 상단 마스코트 이미지 찾기
# 원하는 이미지 파일명을 우선적으로 찾습니다.
image_candidates = [
    "mascot.png",
    "logo.png",
    "main.png",
    "mascot.jpg",
    "logo.jpg",
    "main.jpg",
    "mascot.jpeg",
    "logo.jpeg",
    "main.jpeg",
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
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
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


# 5. 소개 문구
st.markdown(
    """
    <div style="
        text-align: center;
        font-size: 1.3em;
        font-weight: 800;
        color: #57606f;
        margin-top: 5px;
        margin-bottom: 25px;
    ">
        언제 어디서나 왕긴급한 일에 대비하기 위해선<br>
        <span style="color: #ff4757; font-size: 1.2em;">
            왕 긴 급!
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)


# 6. 기능별 카드 및 버튼
cols = st.columns(3, gap="medium")


# 기능 1: 자동 긴급 전화
with cols[0]:
    st.markdown(
        """
        <div class="card-box bg-pink">
            <div class="card-icon">📞</div>
            <div class="card-title title-pink">자동 긴급 전화</div>
            <div class="card-desc">
                긴급상황 시 보호자와 구조대에게
                바로 신고해요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "📞 긴급 신고 바로가기",
        key="btn_call",
        use_container_width=True,
    ):
        safe_switch_page("pages/자동 긴급 전화.py")


# 기능 2: 주변 위험 감지
with cols[1]:
    st.markdown(
        """
        <div class="card-box bg-yellow">
            <div class="card-icon">📡</div>
            <div class="card-title title-yellow">주변 위험 감지</div>
            <div class="card-desc">
                주변 장애물을 센서로 감지하여
                안전을 지켜요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "📡 위험 확인 바로가기",
        key="btn_detect",
        use_container_width=True,
    ):
        safe_switch_page("pages/주변감지경보.py")


# 기능 3: 안전한 길 안내
with cols[2]:
    st.markdown(
        """
        <div class="card-box bg-blue">
            <div class="card-icon">🗺️</div>
            <div class="card-title title-blue">안전한 길 안내</div>
            <div class="card-desc">
                안전한 경로를 안내하여
                보행을 도와요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🗺️ 길 안내 바로가기",
        key="btn_path",
        use_container_width=True,
    ):
        safe_switch_page("pages/안전한 길 안내.py")


# 7. 하단 안내
st.divider()

st.caption(
    "빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전을 지킵니다."
)
