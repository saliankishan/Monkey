# 🖐️ Hand Gesture Image Display

A Python-based computer vision project that uses hand gesture recognition to display different images in real time through a webcam.

The application uses **MediaPipe** to detect hand landmarks and **OpenCV** to process webcam input and display images based on recognized gestures.

## 🚀 Features

* Real-time hand detection using a webcam
* Hand landmark tracking
* Recognition of multiple hand gestures
* Display different images based on detected gestures
* Support for detecting two hands
* Five different image outputs
* Interactive webcam interface

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe

## 📂 Project Structure

```text
fun/
│
├── images/
│   ├── pic1.png
│   ├── pic2.png
│   ├── pic3.png
│   ├── pic4.png
│   └── pic5.png
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ✋ Hand Gestures

The application recognizes different hand gestures and displays the corresponding image.

| Gesture                               | Output   |
| ------------------------------------- | -------- |
| Index finger near the camera center   | pic1.png |
| Thumbs up                             | pic2.png |
| Index finger pointing                 | pic3.png |
| Finger-heart gesture using both hands | pic4.png |
| Both hands open                       | pic5.png |

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hand-gesture-image-display.git
```

### 2. Navigate to the project directory

```bash
cd hand-gesture-image-display
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

## 📷 How It Works

1. The application accesses the webcam.
2. MediaPipe detects hands and identifies hand landmarks.
3. The program analyzes finger positions and distances.
4. The detected gesture is matched with predefined conditions.
5. OpenCV displays the corresponding image.

## 📋 Requirements

* Python 3.9 or a compatible version supported by your installed MediaPipe release
* Webcam
* OpenCV
* MediaPipe

## 🎯 Project Objective

The objective of this project is to demonstrate real-time hand gesture recognition using computer vision.

It combines hand landmark detection, gesture-based interaction, and image display to create a simple touch-free application.

## 👨‍💻 Author

**Kishan D Salian**

## 📜 License

This project is intended for educational and personal use.
