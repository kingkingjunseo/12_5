
import streamlit as st
from pathlib import Path

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="왕긴급!",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 현재 파일이 위치한 폴더
BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# 2. 파스텔톤 커스텀 CSS
# ==========================================
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
        padding: 25px 16px 20px 16px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
        border: 4px solid #ffffff;
        min-height: 245px;
        box-sizing: border-box;
    }

    .card-icon {
        font-size: 3.5em;
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 1.5em;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .card-desc {
        font-size: 1em;
        color: #555555;
        min-height: 55px;
        line-height: 1.6;
        font-weight: 600;
    }

    .bg-pink {
        background-color: #fff0f3;
    }

    .title-pink {
        color: #ff4757;
    }

    .bg-yellow {
        background-color: #fff9db;
    }

    .title-yellow {
        color: #d99a00;
    }

    .bg-blue {
        background-color: #e8f4ff;
    }

    .title-blue {
        color: #1e90ff;
    }

    div.stButton > button {
        width: 100%;
        min-height: 58px;
        border-radius: 22px;
        font-size: 1.05em;
        font-weight: 800;
        padding: 12px 8px;
        border: 3px solid #ffffff;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    }

    div.stButton > button:hover {
        border-color: #ffffff;
        filter: brightness(0.96);
    }

    @media (max-width: 768px) {
        .main-title {
            font-size: 2em;
        }

        .card-box {
            padding: 20px 10px;
            min-height: 220px;
        }

        .card-title {
            font-size: 1.2em;
        }

        .card-icon {
            font-size: 2.8em;
        }

        .card-desc {
            font-size: 0.9em;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 3. 페이지 이동 함수
# ==========================================
def safe_switch_page(relative_path):
    """페이지 파일의 존재를 확인한 후 이동합니다."""

    page_path = BASE_DIR / relative_path

    if not page_path.is_file():
        st.error(
            f"페이지 파일을 찾을 수 없습니다: {relative_path}"
        )
        st.info(
            "GitHub 저장소에서 pages 폴더와 파일 이름을 확인해 주세요."
        )
        return

    try:
        st.switch_page(str(page_path))
    except Exception as error:
        st.error(f"페이지 이동 오류: {error}")


# ==========================================
# 4. 상단 마스코트 이미지
# ==========================================
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

found_image = None

for image_name in image_candidates:
    image_path = BASE_DIR / image_name

    if image_path.is_file():
        found_image = image_path
        break

if found_image is not None:
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.image(
            str(found_image),
            use_container_width=True,
        )
else:
    st.markdown(
        """
        <div class="title-banner">
            <div class="main-title">BIG-GINGEUP!! 🚨</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 5. 소개 문구
# ==========================================
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
        언제 어디서나 왕긴급한 일에 대비하기 위해선
        <br>
        <span style="color: #ff4757; font-size: 1.2em;">
            왕 긴 급!
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 6. 기능별 카드
# ==========================================
cols = st.columns(3, gap="medium")


# ------------------------------------------
# 기능 1. 자동 긴급 전화
# ------------------------------------------
with cols[0]:
    st.markdown(
        """
        <div class="card-box bg-pink">
            <div class="card-icon">📞</div>
            <div class="card-title title-pink">
                자동 긴급 전화
            </div>
            <div class="card-desc">
                긴급상황 시 보호자와 구조대에게
                바로 신고할 수 있도록 도와요.
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


# ------------------------------------------
# 기능 2. 주변 위험 감지
# ------------------------------------------
with cols[1]:
    st.markdown(
        """
        <div class="card-box bg-yellow">
            <div class="card-icon">📡</div>
            <div class="card-title title-yellow">
                주변 위험 감지
            </div>
            <div class="card-desc">
                주변 장애물을 센서로 감지하여
                안전한 보행을 도와요.
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


# ------------------------------------------
# 기능 3. 안전한 길 안내
# ------------------------------------------
with cols[2]:
    st.markdown(
        """
        <div class="card-box bg-blue">
            <div class="card-icon">🗺️</div>
            <div class="card-title title-blue">
                안전한 길 안내
            </div>
            <div class="card-desc">
                안전한 경로를 안내하여
                편안한 보행을 도와요.
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


# ==========================================
# 7. 버튼 색상
# ==========================================
st.markdown(
    """
    <style>
    /* 버튼 색상 */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1)
    div.stButton > button {
        background-color: #ff6b81;
        color: white;
    }

    div[data-testid="stHorizontalBlock"] > div:nth-child(2)
    div.stButton > button {
        background-color: #eccc68;
        color: white;
    }

    div[data-testid="stHorizontalBlock"] > div:nth-child(3)
    div.stButton > button {
        background-color: #70a1ff;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 8. 하단 안내
# ==========================================
st.divider()

st.caption(
    "빅-긴급!! (BIG-GINGEUP) © 노인분들의 안전을 지킵니다."
)
