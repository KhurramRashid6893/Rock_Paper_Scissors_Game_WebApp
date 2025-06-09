import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.max_num_hands = max_num_hands 

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def get_landmarks(self, frame):
        """
        Detect hand landmarks in a frame.
        Returns a list of (id, x, y) for each landmark in the first detected hand.
        """
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Use first detected hand
            h, w, _ = frame.shape
            landmark_list = []

            for idx, lm in enumerate(hand_landmarks.landmark):
                x, y = int(lm.x * w), int(lm.y * h)
                landmark_list.append((idx, x, y))

            return landmark_list
        return []

    def draw_landmarks(self, frame):
        """
        Draw hand landmarks on the frame.
        """
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame
