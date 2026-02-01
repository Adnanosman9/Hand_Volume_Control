# Hand Gesture Volume Control

Control your computer's volume using hand gestures detected through your webcam.

## Features

- **Thumb + Index Finger pinch** → Volume UP 🔊
- **Thumb + Middle Finger pinch** → Volume DOWN 🔉
- **Press 'q'** → Quit program
- **Executable support** - Can be compiled to `.exe` file

## Installation

```bash
pip install opencv-python mediapipe pyautogui
```

Download the hand detection model:

```bash
python -c "import urllib.request; urllib.request.urlretrieve('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task', 'hand_landmarker.task')"
```

## Usage

**As Python script:**

```bash
python hand_volume_control.py
```

**As executable:**

- Compile with PyInstaller: `pyinstaller --onefile --add-data "hand_landmarker.task;." hand_volume_control.py`
- Run the generated `.exe` file

## How It Works

1. **Hand Detection**: MediaPipe detects 21 landmarks on your hand
2. **Distance Calculation**: Measures distance between finger tips using Euclidean formula: `√[(x₂-x₁)² + (y₂-y₁)²]`
3. **Gesture Recognition**: When distance < 0.05 (5% of frame), fingers are "pinching"
4. **Volume Control**: PyAutoGUI simulates volume key presses

## Debugging Journey: The EXE Problem

### The Issue

When compiling the project to an `.exe` file using PyInstaller, the program would open a terminal window and immediately crash without any error message visible.

### The Investigation

Debugging was challenging because:

- The terminal closed instantly before errors could be read
- The program worked perfectly as a Python script
- No obvious errors in the code

### The Solution (Credit: Claude AI)

Claude identified that the issue was related to **MediaPipe's model file path**. When running as an executable, Python's working directory changes, and the hardcoded path `'hand_landmarker.task'` couldn't find the model file.

**The fix:**

```python
# Get the correct path for the model file
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(base_path, 'hand_landmarker.task')
```

This code detects whether the program is running as:

- **Script**: Uses the script's directory
- **Executable**: Uses PyInstaller's temporary folder (`sys._MEIPASS`)

### Key Takeaway

When packaging Python applications with external files (like ML models), always use dynamic path resolution instead of hardcoded strings. AI assistance (Claude) was instrumental in quickly identifying this common but non-obvious packaging issue.

## Requirements

- Python 3.7+
- Webcam
- Windows/Mac/Linux

## Files

- `hand_volume_control.py` - Main program (supports both script and exe)
- `hand_landmarker.task` - MediaPipe AI model (7.8 MB)

## Troubleshooting

**Hand not detected?**

- Ensure good lighting
- Keep hand visible in frame

**Volume not changing?**

- Check PyAutoGUI has keyboard control permissions

**EXE crashes immediately?**

- Ensure `hand_landmarker.task` is in the same directory as the `.exe`
- Use `--add-data` flag when compiling with PyInstaller

## Limitations

### ✅ What Works (Executable Version)

- Runs on other Windows computers **without Python installed**
- No need to install libraries (mediapipe, opencv-python, pyautogui)
- No source code required
- All dependencies bundled inside the `.exe`

### ❌ What Doesn't Work

- **Cross-platform**: Only runs on Windows (not macOS or Linux)
- **Older Windows versions**: May not run on Windows 7 or earlier
- **Different architectures**: Compiled for specific CPU architecture (x64/x86)

> **Note:** For cross-platform support, distribute the Python script instead of the executable.

---

**Built with:** OpenCV • MediaPipe • PyAutoGUI  
**Debugging assistance:** Claude AI (Anthropic)
