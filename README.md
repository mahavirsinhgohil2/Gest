# Gest - Real-time Hand Gesture Recognition

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete, modular Python application for real-time hand and face gesture recognition using computer vision and machine learning.

## 🚀 Features

- **Real-time Detection**: Live hand gesture recognition using MediaPipe and OpenCV
- **Custom Training**: User-friendly GUI for training custom gestures
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Multiple ML Models**: Support for SVM and Random Forest classifiers
- **Robust Architecture**: Modular design with comprehensive error handling
- **Performance Monitoring**: Real-time FPS and latency tracking
- **System Automation**: Execute system actions via PyAutoGUI and pynput
- **Configuration Management**: YAML-based settings and gesture mappings
- **Comprehensive Testing**: Unit and integration tests included

## 📁 Project Structure

```
gest/
├── src/
│   ├── main.py                    # Entry point
│   ├── core/                      # Core functionality
│   │   ├── camera_manager.py      # Camera handling with recovery
│   │   ├── detection_engine.py    # MediaPipe integration
│   │   ├── feature_processor.py   # Feature extraction & normalization
│   │   ├── gesture_classifier.py  # ML classification
│   │   └── action_executor.py     # System action execution
│   ├── gui/                       # User interfaces
│   │   ├── main_window.py         # Main application GUI
│   │   ├── gesture_trainer.py     # Training interface
│   │   └── performance_monitor.py # Performance tracking
│   ├── config/                    # Configuration management
│   │   ├── settings.py            # Settings loader
│   │   └── gesture_mappings.py    # Gesture-action mappings
│   ├── models/                    # Data models
│   │   ├── gesture_model.py       # Gesture data structures
│   │   └── ml_models.py           # ML model utilities
│   ├── utils/                     # Utilities
│   │   ├── logger.py              # Logging configuration
│   │   ├── error_handler.py       # Error handling & recovery
│   │   └── validators.py          # Input validation
│   └── data/                      # Data collection
│       ├── dataset_collector.py   # Dataset management
│       └── gesture_recorder.py    # Recording utilities
├── tests/                         # Unit tests
├── config/                        # Configuration files
│   ├── settings.yaml              # Application settings
│   └── gesture_mappings.yaml      # Gesture-to-action mappings
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Webcam or internal camera
- Operating System: Windows 10+, macOS 10.14+, or Linux Ubuntu 18.04+

### Step 1: Clone the Repository

```bash
git clone https://github.com/mahavirsinhgohil2/Gest.git
cd Gest
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK:' if cap.isOpened() else 'Camera Failed'); cap.release()"

# Test MediaPipe
python -c "import mediapipe as mp; print('MediaPipe version:', mp.__version__)"
```

## 🚀 Quick Start

### Option 1: Run with Mode Selection

```bash
cd src
python main.py
```

This will show a dialog where you can choose:
- **Main Application**: Live gesture recognition
- **Training Mode**: Record and train custom gestures

### Option 2: Direct Training Mode

```bash
cd src
python -c "from gui.gesture_trainer import GestureTrainerGUI; app = GestureTrainerGUI(); app.run()"
```

### Option 3: Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python tests/test_camera.py
```

## 🎯 Usage Guide

### Training Custom Gestures

1. **Launch Training Mode**
   - Run the application and select "Training Mode"
   - Or run the trainer directly

2. **Record Gestures**
   - Enter a gesture name (e.g., "peace_sign")
   - Add a description
   - Set number of samples (recommended: 20-50)
   - Click "Start Recording"
   - Perform the gesture consistently during recording

3. **Train Model**
   - Record at least 2 different gestures
   - Click "Train Model"
   - Wait for training to complete
   - Save the trained model

4. **Test Recognition**
   - Use "Test Model" to verify gesture recognition
   - Adjust training if needed

### Live Gesture Recognition

1. **Launch Main Application**
   - Ensure you have a trained model
   - Camera will initialize automatically
   - Perform trained gestures to trigger actions

2. **Available Actions**
   - Volume control (thumbs up/down)
   - Screenshot (peace sign)
   - Mouse clicks (OK sign, closed fist)
   - Custom actions (configurable)

## ⚙️ Configuration

### Settings (config/settings.yaml)

```yaml
camera:
  device_id: 0              # Primary camera
  backup_device_ids: [1, 2] # Fallback cameras
  width: 640
  height: 480
  fps: 30

detection:
  hand_confidence: 0.7      # Detection threshold
  max_hands: 2              # Maximum hands to detect
  model_complexity: 1       # 0-2, higher = more accurate but slower

ml:
  model_type: "RandomForest" # or "SVM"
  test_size: 0.2            # Training/test split
```

## 🔧 Troubleshooting

### Common Issues

1. **Camera Access Denied**
   - **Windows**: Check camera privacy settings
   - **macOS**: Grant camera permission to Terminal/IDE
   - **Linux**: Add user to `video` group: `sudo usermod -a -G video $USER`

2. **Import Errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Performance Issues**
   - Lower camera resolution in settings
   - Reduce `model_complexity` in detection config
   - Close other applications using camera

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Dependencies

- **mediapipe**: Hand/face detection and tracking
- **opencv-python**: Computer vision and camera handling
- **scikit-learn**: Machine learning algorithms
- **PyAutoGUI**: System automation and control
- **loguru**: Advanced logging
- **PyYAML**: Configuration file parsing
- **numpy**: Numerical computations
- **tkinter**: GUI framework (included with Python)

---

Made with ❤️ for intuitive human-computer interaction