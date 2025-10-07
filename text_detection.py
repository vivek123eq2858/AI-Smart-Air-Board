import numpy as np
import easyocr
import cv2

reader = easyocr.Reader(['en'])
ocr_result = ""

def run_ocr_from_points(points, h, w):
    global ocr_result

    if len(points) < 5:
        ocr_result = ""
        return ""

    pts = np.array(points)
    x_min, y_min = np.min(pts[:, 0]), np.min(pts[:, 1])
    x_max, y_max = np.max(pts[:, 0]), np.max(pts[:, 1])

    # Expand ROI a little
    x_min, y_min = max(0, x_min - 10), max(0, y_min - 10)
    x_max, y_max = min(w, x_max + 10), min(h, y_max + 10)

    # Skip if ROI too small
    if x_max - x_min < 30 or y_max - y_min < 30:
        ocr_result = ""
        return ""

    # Create blank canvas and draw strokes
    temp = np.zeros((h, w), dtype=np.uint8)
    for i in range(1, len(points)):
        cv2.line(temp, points[i-1], points[i], 255, 6)

    crop = temp[y_min:y_max, x_min:x_max]

    # Convert to 3-channel for EasyOCR
    crop = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)

    result = reader.readtext(crop)

    if result:
        ocr_result = " ".join([r[1] for r in result])
        print(f"[OCR] Detected text: {ocr_result}")
    else:
        ocr_result = ""
        print("[OCR] No text detected.")

    return ocr_result
