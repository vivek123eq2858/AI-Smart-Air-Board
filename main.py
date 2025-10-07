import cv2
import mediapipe as mp
from gestures import fingers_up, distance
from shapes import draw_shapes, detect_shape, select_shape, reshape_shape, move_shape
from text_detection import run_ocr_from_points

# ------------------ Setup ------------------ #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

drawing_mode = False
text_mode = False
points = []
shapes_drawn = []
selected_shape = None

# Fullscreen window
cv2.namedWindow("Smart Whiteboard", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Smart Whiteboard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    fingertip, thumbtip, middletip = None, None, None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            fingertip = (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h))
            thumbtip = (int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h))
            middletip = (int(hand_landmarks.landmark[12].x * w), int(hand_landmarks.landmark[12].y * h))
            fingers = fingers_up(hand_landmarks)

            # ---------------- Select shape/text ---------------- #
            if selected_shape is None and fingertip:
                hit = select_shape(fingertip, shapes_drawn)
                if hit:
                    selected_shape = hit
                else:
                    # Check if it's text
                    for shape in reversed(shapes_drawn):
                        if shape['type'] == 'Text':
                            pts = shape['points']
                            x_min = min(p[0] for p in pts)
                            x_max = max(p[0] for p in pts)
                            y_min = min(p[1] for p in pts)
                            y_max = max(p[1] for p in pts)
                            if x_min <= fingertip[0] <= x_max and y_min <= fingertip[1] <= y_max:
                                selected_shape = shape
                                break

            # ---------------- Resize ---------------- #
            if selected_shape and fingers[0] and fingers[1]:  # Thumb + index
                dist = distance(thumbtip, fingertip)
                if 'pinch_start' not in selected_shape:
                    selected_shape['pinch_start'] = dist
                else:
                    scale = dist / selected_shape['pinch_start']
                    selected_shape['pinch_start'] = dist

                    if selected_shape['type'] == 'Text':
                        selected_shape['scale'] = selected_shape.get('scale', 1.0) * scale
                        selected_shape['font_scale'] = max(0.5, min(5.0, selected_shape['scale']))
                    else:
                        reshape_shape(selected_shape, scale)

            # ---------------- Move ---------------- #
            if selected_shape and fingers[1] and fingers[2] and not any(fingers[i] for i in [0,3,4]):
                new_center = ((fingertip[0] + middletip[0]) // 2, (fingertip[1] + middletip[1]) // 2)

                if selected_shape['type'] == 'Text':
                    dx = new_center[0] - selected_shape['pos'][0]
                    dy = new_center[1] - selected_shape['pos'][1]
                    selected_shape['pos'] = new_center
                    selected_shape['points'] = [(x+dx, y+dy) for x, y in selected_shape['points']]
                else:
                    move_shape(selected_shape, new_center)

            # ---------------- Deselect ---------------- #
            if not (fingers[0] or (fingers[1] and fingers[2])):
                selected_shape = None

    key = cv2.waitKey(1) & 0xFF

    # ---------------- Drawing Mode ---------------- #
    if key == ord('d'):
        if not drawing_mode:
            drawing_mode = True
            points = []
        else:
            drawing_mode = False
            if len(points) > 5:
                shape_info = detect_shape(points)
                shapes_drawn.append(shape_info)
            points = []

    if drawing_mode and fingertip:
        points.append(fingertip)
        for i in range(1, len(points)):
            cv2.line(frame, points[i - 1], points[i], (255, 0, 0), 3)

    # ---------------- Text Mode ---------------- #
    if key == ord('t'):
        if not text_mode:
            text_mode = True
            points = []
        else:
            text_mode = False
            if len(points) > 5:
                detected = run_ocr_from_points(points, h, w)
                if detected:
                    shape_info = {'type': 'Text', 'text': detected, 'pos': points[0],
                                  'points': points.copy(), 'font_scale':1.0, 'scale':1.0}
                    shapes_drawn.append(shape_info)
            points = []

    if text_mode and fingertip:
        points.append(fingertip)
        for i in range(1, len(points)):
            cv2.line(frame, points[i - 1], points[i], (0, 0, 255), 3)

    # ---------------- Draw Stored Shapes & Text ---------------- #
    frame = draw_shapes(frame, shapes_drawn)

    # ---------------- Reset/Exit ---------------- #
    if key == ord('r'):
        shapes_drawn = []
        points = []
        selected_shape = None
        drawing_mode = False
        text_mode = False
    elif key == ord('q'):
        break

    cv2.imshow("Smart Whiteboard", frame)

cap.release()
cv2.destroyAllWindows()
