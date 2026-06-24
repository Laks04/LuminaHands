# 🌟 LuminaHands - Elastic Hand Display 
 
> A real-time hand tracking visual effect inspired by the LG Elastic Stretchable Display — built with Python, OpenCV, and MediaPipe.
 
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.35-orange?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-2.2.6-013243?style=flat-square&logo=numpy)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
 
---

<img width="1595" height="916" alt="Screenshot 2026-06-23 170905" src="https://github.com/user-attachments/assets/4140a5ea-3c35-45af-9c9d-09ef725209a7" />

 
## ✨ What is LuminaHands?
 
LuminaHands is a real-time webcam effect that tracks both your hands and renders:
 
- **Glowing LED dots** on all 21 finger joint landmarks per hand
- **Elastic fiber web lines** connecting both hands together
- **Slowly cycling colors** — left hand in purple/pink tones, right hand in mint/teal tones
- **Darkened ambient background** to make the glow effect pop
Inspired by the viral **LG Elastic Stretchable Display** demo and recreated entirely with free, open-source tools.
 
---
 
## 🛠️ Tech Stack
 
| Technology | Version | Role |
|------------|---------|------|
| Python | 3.10 | Core programming language |
| OpenCV | 4.13 | Webcam capture, video processing and drawing |
| MediaPipe | 0.10.35 | AI hand landmark detection (21 points per hand) |
| NumPy | 2.2.6 | Color computation and array operations |
 
---
 
## 🎨 Visual Effects
 
### LED Dots
Each of the **21 hand landmarks** (finger joints, knuckles, wrist) gets a glowing LED-style dot:
- Tiny white specular highlight at the center
- Colored core dot
- Soft wide bloom glow around it
- Colors slowly cycle through hues over time
### Color Palette
| Hand | Color Range |
|------|------------|
| Left hand | Soft purple → pink → lavender |
| Right hand | Mint → cyan → teal → green |
 
### Elastic Fiber Web
When both hands are detected, every landmark on hand 1 connects to every landmark on hand 2 via thin warm off-white fiber threads — 441 lines total (21 x 21). Opacity subtly pulses to give a living, elastic feel.
 
---
 
## 📁 Project Structure
 
```
LuminaHands/
│
├── luminahands.py           # Main script — run this
├── hand_landmarker.task     # MediaPipe hand model (auto-downloaded on first run)
├── test_camera.py           # Webcam diagnostic script
└── README.md                # This file
```
 
---
 
## 📋 Requirements
 
- Windows 10/11
- Python 3.10
- A working webcam (built-in or USB)
- Internet connection (first run only — to download the hand model ~9MB)
---
 
## 🚀 Installation
 
### Step 1 — Install Python 3.10
Download from: https://www.python.org/downloads/release/python-31011/
 
> During installation, make sure to check **"Add Python to PATH"**
 
### Step 2 — Clone the repository
```bash
git clone https://github.com/Laks04/LuminaHands.git
cd LuminaHands
```
 
### Step 3 — Install dependencies
```bash
py -m pip install opencv-python mediapipe numpy
```
 
### Step 4 — Run LuminaHands
```bash
py -3.10 luminahands.py
```
 
> On first run, the hand landmark model (~9MB) will be automatically downloaded and saved as `hand_landmarker.task`. After that, no internet is needed.
 
---
 
## 🎮 How to Use
 
1. Run the script — a webcam window opens
2. Show **one hand** → glowing colored dots appear on all 21 finger joints
3. Show **both hands** → elastic fiber web stretches between your hands
4. Move your hands apart and together to see the elastic stretch effect
5. Press **Q** to quit
---
 
## 💡 How It Works
 
```
Webcam Frame
     ↓
OpenCV captures each frame
     ↓
MediaPipe Tasks API detects both hands + 21 landmarks each
     ↓
Landmark Smoother reduces jitter between frames
     ↓
Draw elastic fiber web between both hands (441 thin lines)
     ↓
Draw glowing LED dots on all 21 landmarks per hand
     ↓
Display darkened frame with effects overlaid in real time
```
 
---
 
## ⚙️ Configuration
 
You can tweak these values in `luminahands.py`:
 
| Variable | Default | Effect |
|----------|---------|--------|
| `alpha` in `LandmarkSmoother` | `0.55` | Higher = more responsive, lower = smoother |
| `radius` in `draw_led_dot` | `5` | Dot size in pixels |
| `alpha` in `draw_fiber` | `0.18` | Fiber line opacity |
| Background `alpha` | `0.60` | Background darkness (0=black, 1=full bright) |
| Color shift speed | `18.0` | Higher = faster color cycling |
 
---
 
## 🔧 Troubleshooting
 
### Black or blank webcam window
- Check if your webcam has a **physical privacy shutter** — slide it open
- Go to **Windows Settings → Privacy & Security → Camera** and enable access
- Close any other app using the camera (Teams, Zoom, browser)
- Run the webcam diagnostic script:
```bash
py -3.10 test_camera.py
```
 
### Second hand not detected
- Make sure both hands are well lit
- Keep both hands fully visible in the frame
- Hold hands at roughly the same distance from the camera
### `pip` not recognized
Use `py -m pip install ...` instead of `pip install ...`
 
### MediaPipe import error
Make sure you are using Python 3.10 — MediaPipe does not fully support Python 3.13+
 
---
 
## 🙌 Credits
 
- Inspired by the **LG Elastic Stretchable Display** concept
- Hand tracking powered by **Google MediaPipe**
---
 
## 📄 License
 
MIT License — free to use, modify, and share.
 
---
 
<p align="center">Made with love using Python + OpenCV + MediaPipe</p>
