import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions
import urllib.request
import os
import time
import math
 
# ─── Download model ────────────────────────────────────────────────────────────
MODEL_PATH = "hand_landmarker.task"
MODEL_URL  = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
 
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmark model (~9MB)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Model downloaded!\n")
 
# ─── MediaPipe Setup ───────────────────────────────────────────────────────────
BaseOptions   = mp_python.BaseOptions
VisionRunMode = vision.RunningMode
 
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.35,
    min_hand_presence_confidence=0.35,
    min_tracking_confidence=0.35
)
detector = HandLandmarker.create_from_options(options)
 
# ─── Webcam ────────────────────────────────────────────────────────────────────
print("Looking for webcam...")
cap = None
for index in [0, 1, 2]:
    test = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    time.sleep(0.5)
    ret, frame = test.read()
    if ret and frame is not None and frame.size > 0:
        print(f"Found webcam at index {index}")
        cap = test
        break
    else:
        test.release()
 
if cap is None:
    print("ERROR: No webcam found!")
    input("Press Enter to exit...")
    exit()
 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
for _ in range(5):
    cap.read()
    time.sleep(0.1)
print("Camera ready!\n")
 
# ─── EXACT colors pixel-sampled from the video frames ─────────────────────────
# Left hand:  soft purple/pink/lavender (R high, B high, G medium)
# Right hand: soft mint/teal/green (G high, B medium, R low-medium)
# Both cycle slowly through hue over time
 
# Sampled RGB converted to HSV hues:
# Left:  R247 G197 B255 → purple-pink hue ~290° → HSV ~145
#        R220 G127 B220 → magenta       → HSV ~150
# Right: R207 G255 B243 → mint-green    → HSV ~165
#        R171 G255 B231 → cyan-green    → HSV ~160
 
# Per-landmark base HSV hues (0-179 OpenCV scale)
# Left hand cycles in purple/pink range
LEFT_BASE = [
    148, 150, 152, 154, 156,   # wrist + thumb  (purple-pink)
    144, 146, 148, 150,         # index
    140, 142, 144, 146,         # middle
    136, 138, 140, 142,         # ring
    132, 134, 136, 138          # pinky
]
# Right hand cycles in mint/teal/green range
RIGHT_BASE = [
    163, 161, 159, 157, 155,   # wrist + thumb  (cyan-mint)
    165, 163, 161, 159,         # index
    160, 158, 156, 154,         # middle
    155, 153, 151, 149,         # ring
    150, 148, 146, 144          # pinky
]
 
def get_dot_color_bgr(hand_idx, lm_idx, t):
    # Slow hue drift — full cycle every ~20 seconds
    shift = (t * 18.0) % 180.0
    base  = LEFT_BASE[lm_idx] if hand_idx == 0 else RIGHT_BASE[lm_idx]
    hue   = int((base + shift) % 180)
    sat   = 140   # NOT fully saturated — matches the soft pastel look
    val   = 255
    hsv   = np.uint8([[[hue, sat, val]]])
    bgr   = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
    return tuple(int(c) for c in bgr)
 
# ─── Draw LED dot: exact look from video ──────────────────────────────────────
# Video shows: small bright colored dot + wide very soft bloom around it
def draw_led_dot(img, cx, cy, color, radius=5):
    # Wide soft outer bloom (very transparent)
    for r, a in [(radius+20, 0.018), (radius+14, 0.035),
                 (radius+9,  0.07),  (radius+5,  0.14),
                 (radius+2,  0.25)]:
        ov = img.copy()
        cv2.circle(ov, (cx, cy), r, color, -1, cv2.LINE_AA)
        cv2.addWeighted(ov, a, img, 1-a, 0, img)
    # Solid colored core
    cv2.circle(img, (cx, cy), radius, color, -1, cv2.LINE_AA)
    # Bright near-white center highlight
    highlight = tuple(min(255, int(c*0.5 + 255*0.5)) for c in color)
    cv2.circle(img, (cx, cy), max(2, radius-2), highlight, -1, cv2.LINE_AA)
    # Tiny pure white specular
    cv2.circle(img, (cx, cy), max(1, radius-3), (255,255,255), -1, cv2.LINE_AA)
 
# ─── Draw fiber line: thin, semi-transparent, anti-aliased ───────────────────
# Fiber color from video: warm off-white R~197 G~192 B~191 (BGR: 191,192,197)
FIBER_COLOR = (191, 192, 197)
 
def draw_fiber(img, p1, p2, alpha=0.18):
    ov = img.copy()
    cv2.line(ov, p1, p2, FIBER_COLOR, 1, cv2.LINE_AA)
    cv2.addWeighted(ov, alpha, img, 1-alpha, 0, img)
 
# ─── Smoothing: landmark position smoother to reduce jitter ──────────────────
class LandmarkSmoother:
    def __init__(self, alpha=0.55):
        self.alpha = alpha   # higher = more responsive, lower = smoother
        self.prev  = {}      # hand_idx -> list of (x,y)
 
    def smooth(self, hand_idx, pts):
        if hand_idx not in self.prev:
            self.prev[hand_idx] = pts
            return pts
        smoothed = []
        for i, (x, y) in enumerate(pts):
            px, py = self.prev[hand_idx][i]
            sx = int(self.alpha * x + (1 - self.alpha) * px)
            sy = int(self.alpha * y + (1 - self.alpha) * py)
            smoothed.append((sx, sy))
        self.prev[hand_idx] = smoothed
        return smoothed
 
    def reset(self, hand_idx):
        if hand_idx in self.prev:
            del self.prev[hand_idx]
 
# ─── Main Loop ─────────────────────────────────────────────────────────────────
smoother   = LandmarkSmoother(alpha=0.55)
timestamp_ms = 0
t = 0.0   # time for color animation
 
print("! LuminaHands !")
print("Show both hands to your webcam")
print("Press Q to quit\n")
 
while cap.isOpened():
    ret, frame = cap.read()
    if not ret or frame is None:
        time.sleep(0.03)
        continue
 
    frame = cv2.flip(frame, 1)
    h, w  = frame.shape[:2]
    t    += 0.016   # ~60fps time step
 
    # Detect on original frame
    rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect_for_video(mp_img, timestamp_ms)
    timestamp_ms += 33
 
    hand_list  = result.hand_landmarks
    hand_count = len(hand_list)
 
    # Darken background — matches video's ambient dim look
    display = cv2.convertScaleAbs(frame, alpha=0.60, beta=0)
 
    # Build smoothed point lists
    all_pts = []
    for hidx, landmarks in enumerate(hand_list):
        raw = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        pts = smoother.smooth(hidx, raw)
        all_pts.append(pts)
 
    # Reset smoother for hands that disappeared
    if hand_count < 2:
        for idx in range(hand_count, 2):
            smoother.reset(idx)
 
    # ── 1. Draw cross-hand fiber web (ONLY between the two hands) ─────────────
    if hand_count == 2:
        pts1, pts2 = all_pts[0], all_pts[1]
        for i in range(21):
            for j in range(21):
                # Subtle alpha variation gives depth like in video
                a = 0.13 + 0.07 * math.sin(i * 0.8 + j * 0.5 + t * 1.5)
                a = max(0.07, min(0.22, a))
                draw_fiber(display, pts1[i], pts2[j], alpha=a)
 
    # ── 2. Draw LED dots on all 21 landmarks — NO connecting lines ────────────
    for hidx, pts in enumerate(all_pts):
        for lm_idx, (x, y) in enumerate(pts):
            color = get_dot_color_bgr(hidx, lm_idx, t)
            draw_led_dot(display, x, y, color, radius=5)
 
    # ── Status bar ────────────────────────────────────────────────────────────
    cv2.rectangle(display, (0, 0), (w, 40), (0, 0, 0), -1)
    if hand_count == 2:
        cv2.putText(display, "LuminaHands ACTIVE",
                    (w//2-145, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 160, 255), 2)
    elif hand_count == 1:
        cv2.putText(display, "Show second hand...",
                    (w//2-105, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (140, 210, 255), 2)
    else:
        cv2.putText(display, "Show both hands to camera",
                    (w//2-145, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (180, 180, 180), 2)
 
    cv2.putText(display, f"Hands: {hand_count}/2", (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
    cv2.putText(display, "Q: Quit", (w-80, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (130, 130, 130), 1)
 
    cv2.imshow("LuminaHands", display)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
detector.close()
print("Closed!")