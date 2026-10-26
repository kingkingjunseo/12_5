
import json
import math
import time

import folium
import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="안전 동행",
    page_icon="🚶",
    layout="wide",
)

# 지도 시연용 기준 위치. 화면에는 좌표나 장소 이름을 표시하지 않음.
LAT = 36.84152810
LON = 127.14213325

OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

ALERT_DISTANCE = 60  # 위험 지점 60m 이내 접근 시 경보


# -----------------------------
# 위험 정보 가져오기
# -----------------------------
@st.cache_data(ttl=300, show_spinner=False)
def get_hazards(lat, lon, radius):
    query = f"""
    [out:json][timeout:12];
    (
      nwr(around:{radius},{lat},{lon})["highway"="construction"];
      nwr(around:{radius},{lat},{lon})["construction"];
      nwr(around:{radius},{lat},{lon})["barrier"="construction"];
      nwr(around:{radius},{lat},{lon})["highway"="steps"];
      nwr(around:{radius},{lat},{lon})["natural"="cliff"];
      nwr(around:{radius},{lat},{lon})["barrier"="cliff"];
      nwr(around:{radius},{lat},{lon})["hazard"];
      way(around:{radius},{lat},{lon})["incline"];
      way(around:{radius},{lat},{lon})
        ["highway"~"path|track"]
        ["smoothness"~"bad|very_bad|horrible|impassable"];
    );
    out center tags;
    """

    errors = []

    for server in OVERPASS_SERVERS:
        try:
            response = requests.post(
                server,
                data={"data": query},
                headers={"User-Agent": "SafetyCompanion/1.0"},
                timeout=(3, 12),
            )
            response.raise_for_status()
            data = response.json()

            hazards = []

            for item in data.get("elements", []):
                tags = item.get("tags", {})
                point_lat = item.get("lat")
                point_lon = item.get("lon")

                if point_lat is None or point_lon is None:
                    center = item.get("center", {})
                    point_lat = center.get("lat")
                    point_lon = center.get("lon")

                if point_lat is None or point_lon is None:
                    continue

                if tags.get("highway") == "construction" or "construction" in tags:
                    kind = "공사 구간"
                elif tags.get("highway") == "steps":
                    kind = "계단"
                elif tags.get("natural") == "cliff" or tags.get("barrier") == "cliff":
                    kind = "절벽"
                elif "hazard" in tags:
                    kind = "위험 구간"
                elif "incline" in tags:
                    kind = "경사 구간"
                elif tags.get("smoothness") in (
                    "bad", "very_bad", "horrible", "impassable"
                ):
                    kind = "노면 주의"
                else:
                    kind = "주의 구간"

                hazards.append({
                    "id": f'{item.get("type", "item")}-{item.get("id", "")}',
                    "lat": float(point_lat),
                    "lon": float(point_lon),
                    "kind": kind,
                })

            return hazards, None

        except (requests.RequestException, ValueError) as error:
            errors.append(str(error))

    return [], "위험 정보를 가져오지 못했습니다. 잠시 후 다시 시도해 주세요."


# -----------------------------
# 거리 계산
# -----------------------------
def distance_m(lat1, lon1, lat2, lon2):
    earth_radius = 6371000
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    )
    return earth_radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# -----------------------------
# 화면 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: #FFF9F1;
}
.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
}
h1, h2, h3 {
    color: #34483D;
}
div[data-testid="stAlert"] {
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚶 안전 동행")
st.subheader("어르신을 위한 주변 보행 안전 지도")
st.write(
    "주변의 공사 구간, 계단, 절벽, 경사 및 노면 상태 관련 "
    "지도 정보를 확인할 수 있습니다."
)

with st.sidebar:
    st.header("지도 설정")
    radius = st.slider(
        "주변 검색 범위",
        min_value=200,
        max_value=1500,
        value=800,
        step=100,
        format="%d m",
    )

    if st.button("위험 정보 새로고침", use_container_width=True):
        get_hazards.clear()
        st.rerun()

# 위치를 다시 찾는 절차 없이 고정 기준점으로 지도를 즉시 준비
with st.spinner("주변 위험 정보를 확인하고 있습니다..."):
    hazards, error = get_hazards(LAT, LON, radius)

if error:
    st.warning(error)

# -----------------------------
# 지도 표시
# -----------------------------
map_obj = folium.Map(
    location=[LAT, LON],
    zoom_start=16,
    tiles="OpenStreetMap",
)

folium.Marker(
    [LAT, LON],
    tooltip="현재 위치",
    popup="현재 위치",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(map_obj)

for hazard in hazards:
    folium.Marker(
        [hazard["lat"], hazard["lon"]],
        tooltip=hazard["kind"],
        popup=f'⚠️ {hazard["kind"]}',
        icon=folium.Icon(color="red", icon="warning-sign"),
    ).add_to(map_obj)

st_folium(
    map_obj,
    use_container_width=True,
    height=480,
    returned_objects=[],
)

st.caption(f"표시된 위험 지점: {len(hazards)}곳")

if hazards:
    with st.expander("주변 위험 지점 확인"):
        for hazard in hazards:
            st.write(f'🔴 {hazard["kind"]}')
else:
    st.info(
        "검색 범위에서 등록된 위험 정보를 찾지 못했습니다. "
        "위험이 없다는 뜻은 아닙니다."
    )

# -----------------------------
# 브라우저에서 실제 위치를 확인하고 자동 경보
# -----------------------------
# 이 코드는 지도에 표시된 위험 지점의 좌표를 브라우저에 전달합니다.
# 브라우저의 위치 권한이 허용되어야 실제 접근 여부를 확인할 수 있습니다.
hazards_json = json.dumps(hazards, ensure_ascii=False)

alarm_html = """
<div style="font-family:sans-serif;background:#fff4e5;
padding:12px;border-radius:12px;color:#34483D;">
  <strong id="alarm-status">📍 자동 위치 확인을 시작합니다.</strong>
  <div id="alarm-detail" style="font-size:13px;margin-top:5px;">
    브라우저의 위치 권한을 허용해 주세요.
  </div>
</div>

<script>
const hazards = HAZARDS_DATA;
const alertDistance = ALERT_DISTANCE;
const statusEl = document.getElementById("alarm-status");
const detailEl = document.getElementById("alarm-detail");

let lastAlertId = null;
let lastAlertTime = 0;
let audioContext = null;

function playAlarm() {
    try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) {
            statusEl.textContent = "⚠️ 이 브라우저에서는 경고음을 지원하지 않습니다.";
            return;
        }

        if (!audioContext) audioContext = new AudioCtx();

        if (audioContext.state === "suspended") {
            audioContext.resume().catch(() => {});
        }

        if (audioContext.state !== "running") {
            statusEl.textContent =
                "⚠️ 브라우저에서 소리 재생이 차단되었습니다. 소리 권한을 확인해 주세요.";
            return;
        }

        const now = audioContext.currentTime;

        [0, 0.32, 0.64].forEach((offset) => {
            const oscillator = audioContext.createOscillator();
            const gain = audioContext.createGain();

            oscillator.type = "sine";
            oscillator.frequency.value = 880;
            gain.gain.setValueAtTime(0.0001, now + offset);
            gain.gain.exponentialRampToValueAtTime(0.25, now + offset + 0.03);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + offset + 0.20);

            oscillator.connect(gain);
            gain.connect(audioContext.destination);
            oscillator.start(now + offset);
            oscillator.stop(now + offset + 0.22);
        });
    } catch (e) {
        statusEl.textContent = "⚠️ 경고음을 재생할 수 없습니다.";
    }
}

function distanceMeters(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const rad = x => x * Math.PI / 180;
    const dLat = rad(lat2 - lat1);
    const dLon = rad(lon2 - lon1);
    const a = Math.sin(dLat / 2) ** 2
        + Math.cos(rad(lat1)) * Math.cos(rad(lat2))
        * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function onPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    statusEl.textContent = "🟢 자동 경보 작동 중";
    detailEl.textContent = "주변 위험 지점과의 거리를 확인하고 있습니다.";

    let nearest = null;
    let nearestDistance = Infinity;

    for (const hazard of hazards) {
        const distance = distanceMeters(
            lat, lon, hazard.lat, hazard.lon
        );

        if (distance < nearestDistance) {
            nearestDistance = distance;
            nearest = hazard;
        }
    }

    if (nearest && nearestDistance <= alertDistance) {
        const now = Date.now();
        detailEl.textContent =
            "위험 지점 접근: " + nearest.kind
            + " · 약 " + Math.round(nearestDistance) + "m";

        // 같은 위험 지점에서 15초마다 반복 경보
        if (lastAlertId !== nearest.id || now - lastAlertTime > 15000) {
            playAlarm();
            lastAlertId = nearest.id;
            lastAlertTime = now;
        }
        statusEl.textContent = "🔴 위험 지점에 가까이 접근했습니다!";
    } else {
        // 위험 지점에서 충분히 멀어지면 다음 접근 경보를 허용
        if (nearestDistance > alertDistance + 40) {
            lastAlertId = null;
        }
        detailEl.textContent = nearest
            ? "가장 가까운 등록 위험 지점까지 약 "
                + Math.round(nearestDistance) + "m"
            : "현재 검색된 위험 지점이 없습니다.";
    }
}

function onLocationError(error) {
    statusEl.textContent = "📍 위치 정보를 확인할 수 없습니다.";
    if (error.code === 1) {
        detailEl.textContent = "브라우저 설정에서 위치 권한을 허용해 주세요.";
    } else {
        detailEl.textContent = "위치 신호가 약하거나 사용할 수 없습니다.";
    }
}

if ("geolocation" in navigator) {
    navigator.geolocation.watchPosition(
        onPosition,
        onLocationError,
        {
            enableHighAccuracy: true,
            maximumAge: 3000,
            timeout: 10000
        }
    );
} else {
    statusEl.textContent = "이 브라우저는 위치 확인을 지원하지 않습니다.";
}
</script>
"""

alarm_html = (
    alarm_html
    .replace("HAZARDS_DATA", hazards_json)
    .replace("ALERT_DISTANCE", str(ALERT_DISTANCE))
)

components.html(alarm_html, height=100, scrolling=False)

st.caption(
    "지도 자료는 OpenStreetMap 기반이며, 등록되지 않은 위험이나 "
    "위치 오차가 있을 수 있습니다."
)
