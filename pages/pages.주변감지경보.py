
import streamlit as st
import streamlit.components.v1 as components
from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    WebRtcMode,
)
from ultralytics import YOLO
import av
import cv2
import threading
import time
import io
import wave
import math
import struct

# ----------------------------
# 1. 페이지 설정
# ----------------------------
st.set_page_config(
    page_title="AI 안전 감지",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AI 주변 위험 감지 시스템")
st.write(
    "카메라 영상에서 지정한 물체를 감지하고 "
    "주의가 필요한 대상이 발견되면 경고합니다."
)

# ----------------------------
# 2. AI 모델 불러오기
# ----------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

with st.spinner("AI 모델을 불러오는 중..."):
    model = load_model()

# ----------------------------
# 3. 경고 대상 설정
# ----------------------------
OBJECTS = {
    "person": "사람",
    "bicycle": "자전거",
    "car": "자동차",
    "motorcycle": "오토바이",
    "bus": "버스",
    "truck": "트럭",
}

st.subheader("감지할 대상 선택")

selected_objects = st.multiselect(
    "선택한 물체가 발견되면 경고합니다.",
    options=list(OBJECTS.keys()),
    default=["bicycle", "car", "motorcycle", "truck"],
    format_func=lambda x: OBJECTS[x]
)

confidence = st.slider(
    "AI 감지 신뢰도 기준",
    min_value=0.1,
    max_value=0.9,
    value=0.4,
    step=0.1
)

# ----------------------------
# 4. 실시간 감지 결과 공유
# ----------------------------
result_lock = threading.Lock()

detection_state = {
    "objects": [],
    "last_detection": 0.0,
}

# ----------------------------
# 5. 카메라 영상 분석
# ----------------------------
class SafetyDetector(VideoProcessorBase):
    def __init__(self):
        self.last_run = 0.0

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")

        # 너무 잦은 추론을 줄여 처리 부담 완화
        now = time.time()

        if now - self.last_run >= 0.25:
            self.last_run = now

            results = model.predict(
                image,
                conf=confidence,
                imgsz=640,
                verbose=False
            )

            found = []

            for box in results[0].boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                if class_name in selected_objects:
                    found.append(OBJECTS[class_name])

            with result_lock:
                detection_state["objects"] = found
                detection_state["last_detection"] = now

            # 감지된 물체에 테두리 표시
            image = results[0].plot()

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )

# ----------------------------
# 6. 경보음 생성
# ----------------------------
def create_beep():
    sample_rate = 22050
    duration = 0.35
    frequency = 880

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        samples = bytearray()

        for i in range(int(sample_rate * duration)):
            value = int(
                10000 * math.sin(
                    2 * math.pi * frequency * i / sample_rate
                )
            )
            samples.extend(struct.pack("<h", value))

        wav.writeframes(samples)

    return buffer.getvalue()

# ----------------------------
# 7. 카메라 시작
# ----------------------------
st.subheader("📷 실시간 카메라")

webrtc_streamer(
    key="safety-camera",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=SafetyDetector,
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
    async_processing=True,
)

# ----------------------------
# 8. 경고 화면
# ----------------------------
st.subheader("📢 감지 결과")

with result_lock:
    detected = list(detection_state["objects"])
    last_detection = detection_state["last_detection"]

# 오래된 결과를 현재 결과로 오인하지 않도록 처리
if time.time() - last_detection > 2:
    detected = []

if detected:
    st.error(
        "⚠️ 주의 대상 감지: "
        + ", ".join(sorted(set(detected)))
    )

    st.warning(
        "주변을 확인하고 안전한 거리를 유지하세요."
    )

    # 경고음 재생은 브라우저의 자동 재생 정책에 따라
    # 사용자 조작이 필요할 수 있음
    st.audio(
        create_beep(),
        format="audio/wav",
        autoplay=True
    )
else:
    st.success("현재 감지된 경고 대상이 없습니다.")

st.caption(
    "주의: 이 프로그램은 물체 감지용 시제품입니다. "
    "실제 위험 여부를 판정하거나 모든 위험을 감지하지는 못합니다."
)

