
import io
import math
import struct
import threading
import wave

import av
import streamlit as st
from streamlit_webrtc import (
    WebRtcMode,
    VideoProcessorBase,
    webrtc_streamer,
)
from ultralytics import YOLO


# -------------------------
# 1. 기본 설정
# -------------------------
st.set_page_config(
    page_title="AI 안전 감지",
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 AI 주변 위험 감지")
st.write("카메라로 주변 물체를 감지하는 안전 보조 앱입니다.")


# -------------------------
# 2. AI 모델
# -------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


# -------------------------
# 3. 경고음 생성
# -------------------------
@st.cache_data
def create_beep():
    rate = 22050
    duration = 0.4
    frequency = 880

    samples = bytearray()

    for i in range(int(rate * duration)):
        value = int(
            9000 * math.sin(
                2 * math.pi * frequency * i / rate
            )
        )
        samples.extend(struct.pack("<h", value))

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(samples)

    return buffer.getvalue()


# -------------------------
# 4. 감지 대상 설정
# -------------------------
OBJECTS = {
    "person": "사람",
    "bicycle": "자전거",
    "car": "자동차",
    "motorcycle": "오토바이",
    "bus": "버스",
    "truck": "트럭",
}

st.sidebar.header("감지 설정")

selected_objects = st.sidebar.multiselect(
    "감지할 물체",
    options=list(OBJECTS.keys()),
    default=["bicycle", "car", "motorcycle", "truck"],
    format_func=lambda name: OBJECTS[name],
)

confidence = st.sidebar.slider(
    "감지 신뢰도",
    min_value=0.1,
    max_value=0.9,
    value=0.4,
    step=0.1,
)


# -------------------------
# 5. 모델 불러오기
# -------------------------
try:
    with st.spinner("AI 모델을 준비하고 있습니다..."):
        model = load_model()
except Exception as error:
    st.error("AI 모델을 불러오지 못했습니다.")
    st.code(str(error))
    st.info(
        "인터넷 연결과 requirements.txt의 패키지 설치 상태를 확인하세요."
    )
    st.stop()


# -------------------------
# 6. 영상 분석 클래스
# -------------------------
class SafetyDetector(VideoProcessorBase):

    def __init__(self):
        self.lock = threading.Lock()
        self.detected_objects = []
        self.error_message = ""

        # 카메라가 시작될 때 선택된 설정을 사용
        self.targets = set(selected_objects)
        self.threshold = confidence

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")

        try:
            results = model.predict(
                source=image,
                conf=self.threshold,
                imgsz=640,
                verbose=False,
            )

            result = results[0]
            found = set()

            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0].item())
                    class_name = model.names[class_id]

                    if class_name in self.targets:
                        found.add(
                            OBJECTS.get(class_name, class_name)
                        )

            with self.lock:
                self.detected_objects = sorted(found)
                self.error_message = ""

            # 감지된 물체에 테두리와 이름 표시
            image = result.plot()

        except Exception as error:
            with self.lock:
                self.error_message = str(error)

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24",
        )


# -------------------------
# 7. 카메라 실행
# -------------------------
st.subheader("📷 실시간 카메라")

# 설정을 바꾸면 새로운 카메라 세션을 사용
camera_key = (
    "safety-camera-"
    + "-".join(sorted(selected_objects))
    + f"-{confidence}"
)

ctx = webrtc_streamer(
    key=camera_key,
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=SafetyDetector,
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
    async_processing=True,
)

st.caption(
    "카메라를 시작하고 브라우저에서 카메라 권한을 허용하세요."
)


# -------------------------
# 8. 결과 자동 갱신
# -------------------------
@st.fragment(run_every="1s")
def show_detection():
    processor = ctx.video_processor

    st.subheader("📢 감지 결과")

    if processor is None:
        st.info("카메라를 시작하면 감지 결과가 표시됩니다.")
        return

    with processor.lock:
        detected = list(processor.detected_objects)
        error_message = processor.error_message

    if error_message:
        st.warning("일부 영상 분석 중 오류가 발생했습니다.")
        st.code(error_message)

    if detected:
        st.error(
            "⚠️ 주의 대상 감지: " + ", ".join(detected)
        )
        st.warning(
            "주변 상황을 직접 확인하고 안전한 거리를 유지하세요."
        )

        if st.button("🔊 경고음 재생", key="play_alarm"):
            st.audio(
                create_beep(),
                format="audio/wav",
            )
    else:
        st.success("선택한 주의 대상이 감지되지 않았습니다.")


show_detection()

st.divider()

st.caption(
    "이 앱은 물체를 인식하는 시제품입니다. "
    "물체가 감지되었다고 반드시 위험한 것은 아니며, "
    "감지되지 않았다고 안전이 보장되는 것도 아닙니다."
)


            
