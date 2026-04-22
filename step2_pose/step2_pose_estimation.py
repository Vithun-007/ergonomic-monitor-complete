import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class PoseDetector:
    def __init__(self):
        base = python.BaseOptions(model_asset_path="models/pose_landmarker_full.task")
        opts = vision.PoseLandmarkerOptions(
            base_options=base,
            running_mode=vision.RunningMode.VIDEO
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(opts)

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        ts = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        res = self.landmarker.detect_for_video(mp_img, ts)
        return res.pose_landmarks[0] if res.pose_landmarks else None

    def draw(self, frame, landmarks, severity):
        h, w, _ = frame.shape
        color = (0,255,0) if severity < 0.4 else (0,255,255) if severity < 0.7 else (0,0,255)

        for lm in landmarks:
            cv2.circle(frame, (int(lm.x*w), int(lm.y*h)), 4, color, -1)