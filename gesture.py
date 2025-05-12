from enum import Enum
import math
import cv2
import mediapipe as mp

class GestureRecogniser:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=1)
        self.mp_drawing = mp.solutions.drawing_utils

    def classify_image(self, img):
        # Convert BGR to RGB for Mediapipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if not results.multi_hand_landmarks:
            return "UNKNOWN"

        landmarks = results.multi_hand_landmarks[0].landmark
        landmark_points = [(lm.x, lm.y) for lm in landmarks]

        fingers = self._check_fingers_extended(landmark_points)

        if not any(fingers[1:]):
            return "ROCK"
        elif all(fingers[1:]):
            return "PAPER"
        elif fingers[1] and fingers[2] and not (fingers[3] or fingers[4]):
            return "SCISSORS"
        else:
            return "UNKNOWN"

    def _check_fingers_extended(self, landmarks):
        fingers = []

        # Thumb (horizontal check based on x-axis)
        thumb_tip_x = landmarks[4][0]
        thumb_mcp_x = landmarks[2][0]
        thumb_extended = thumb_tip_x > thumb_mcp_x  # for right hand
        fingers.append(thumb_extended)

        # Fingers (tip higher than pip in y-axis for each)
        finger_ids = [(8, 6), (12, 10), (16, 14), (20, 18)]
        for tip_idx, pip_idx in finger_ids:
            tip_y = landmarks[tip_idx][1]
            pip_y = landmarks[pip_idx][1]
            fingers.append(tip_y < pip_y)

        return fingers  # [thumb, index, middle, ring, pinky]
