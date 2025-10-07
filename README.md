# AI-Smart-Air-Board

AI-Smart-Air-Board is a smart whiteboard application that uses computer vision and hand gesture recognition to draw, move, resize, and add text to shapes in real-time using your webcam.

## Features

- **Draw Shapes:** Use hand gestures to draw shapes on the board.
- **Text Recognition:** Add text by drawing a region and running OCR.
- **Move & Resize:** Select, move, and resize shapes or text using intuitive gestures.
- **Gesture Controls:** Switch between drawing and text modes, reset, and exit with keyboard shortcuts.

## Requirements

- Python 3.7+
- [OpenCV](https://opencv.org/) (`cv2`)
- [MediaPipe](https://google.github.io/mediapipe/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (for text recognition)
- Other dependencies: see `requirements.txt` if provided

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/vivek123eq2858/AI-Smart-Air-Board.git
   cd AI-Smart-Air-Board
   ```

2. **Install dependencies:**
   ```sh
   pip install opencv-python mediapipe pytesseract
   ```

3. **Install Tesseract OCR:**
   - Download and install from [here](https://github.com/tesseract-ocr/tesseract).
   - Make sure `tesseract` is added to your system PATH.

## Usage

1. **Run the application:**
   ```sh
   python main.py
   ```

2. **Controls:**
   - `d` : Toggle drawing mode
   - `t` : Toggle text mode
   - `r` : Reset board
   - `q` : Quit application

3. **Gestures:**
   - **Draw:** Use your index finger to draw.
   - **Select:** Point at a shape/text to select.
   - **Resize:** Pinch (thumb + index) to resize.
   - **Move:** Use index + middle finger to move.

## File Structure

- `main.py` : Main application logic
- `gestures.py` : Hand gesture utilities
- `shapes.py` : Shape drawing and manipulation functions
- `text_detection.py` : OCR and text region detection

## Screenshots

*(Add screenshots or GIFs here if available)*

## License

MIT License

---

**Contributors:**  
- [Vivek Sharma](https://github.com/vivek123eq2858)

