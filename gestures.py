import numpy as np

def fingers_up(hand_landmarks):
    """
    Returns a list of boolean values for fingers [thumb, index, middle, ring, pinky]
    True if finger is up.
    """
    tips = [4, 8, 12, 16, 20]  # landmarks for thumb, index, middle, ring, pinky
    fingers_status = []

    for i, tip in enumerate(tips):
        if i == 0:  # Thumb
            fingers_status.append(hand_landmarks.landmark[tip].x > hand_landmarks.landmark[tip-2].x)
        else:
            fingers_status.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y)
    return fingers_status

def distance(p1, p2):
    """Euclidean distance between two points"""
    return np.hypot(p1[0]-p2[0], p1[1]-p2[1])
