import cv2
import mediapipe as mp
import pyautogui
import math
import sys
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Get the correct path for the model file
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(base_path, 'hand_landmarker.task')

# Use the model_path instead of hardcoded string
base = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base, num_hands=1)
landmarker = vision.HandLandmarker.create_from_options(options)
cap = cv2.VideoCapture(0)


def draw_hand(frame, hand):
    h, w, c = frame.shape
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (0, 9), (9, 10), (10, 11), (11, 12),
        (0, 13), (13, 14), (14, 15), (15, 16),
        (0, 17), (17, 18), (18, 19), (19, 20),
        (5, 9), (9, 13), (13, 17)
    ]
    for s, e in connections:
        sx, sy = int(hand[s].x * w), int(hand[s].y * h)
        ex, ey = int(hand[e].x * w), int(hand[e].y * h)
        cv2.line(frame, (sx, sy), (ex, ey), (255, 0, 0), 2)


while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = landmarker.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))

    if res.hand_landmarks:
        hand = res.hand_landmarks[0]
        draw_hand(frame, hand)

        if math.sqrt((hand[4].x - hand[8].x) ** 2 + (hand[4].y - hand[8].y) ** 2) < 0.05:
            pyautogui.press('volumeup')
        elif math.sqrt((hand[4].x - hand[12].x) ** 2 + (hand[4].y - hand[12].y) ** 2) < 0.05:
            pyautogui.press('volumedown')

    cv2.imshow('Hand Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()