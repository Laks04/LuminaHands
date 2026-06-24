# 🌟 LuminaHands
 
> A real-time hand tracking visual effect inspired by the LG Elastic Stretchable Display — built with Python, OpenCV, and MediaPipe.
 
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.35-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![Cost](https://img.shields.io/badge/Cost-Free%20Forever-brightgreen?style=flat-square)
 
---
 
## ✨ What is LuminaHands?
 
LuminaHands is a real-time webcam effect that tracks both your hands and renders:
 
- 🔴🟣🟢 **Glowing LED dots** on all 21 finger joint landmarks per hand
- 🕸️ **Elastic fiber web lines** connecting both hands together
- 🎨 **Slowly cycling colors** — left hand in purple/pink tones, right hand in mint/teal tones
- 🌑 **Darkened ambient background** to make the glow effect pop
Inspired by the viral **LG Elastic Stretchable Display** demo and recreated entirely with free, open-source tools.
 
---
 
## 🎬 Demo
 
| One Hand | Two Hands |
|----------|-----------|
| Glowing dots appear on all 21 joints | Elastic fiber web stretches between both hands |
| Colors slowly shift through hues | Colors cycle independently per hand |
 
---
 
## 🛠️ Tech Stack
 
| Library | Version | Purpose |
|---------|---------|---------|
| Python | 3.10 | Programming language |
| OpenCV | 4.13 | Webcam capture & drawing |
| MediaPipe | 0.10.35 | AI hand landmark detection |
| NumPy | 2.2.6 | Array & color computation |
 
---
 
## 📋 Requirements
 
- Windows 10/11 (tested on Windows with Python 3.10)
- A working webcam (built-in or USB)
- Python 3.10 installed
- Internet connection (first run only — to download the hand model ~9MB)
---
 
## 🚀 Installation
 
### Step 1 — Install Python 3.10
Download from: https://www.python.org/downloads/release/python-31011/
 
> ⚠️ During installation, make sure to check **"Add Python to PATH"**
 
### Step 2 — Install dependencies
Open PowerShell or terminal and run:
 
```bash
py -m pip install opencv-python mediapipe numpy
```
 
### Step 3 — Clone or download this repo
```bash
git clone https://github.com/yourusername/luminahands.git
cd luminahands
```
 
### Step 4 — Run LuminaHands
```bash
py -3.10 luminahands.py
```
 
Or with full Python path (Windows):
```bash
C:\Users\YourName\AppData\Local\Python\pythoncore-3.10-64\python.exe luminahands.py
```
 
> 📥 On first run, the hand landmark model (~9MB) will be automatically downloaded and saved locally. After that, no internet is needed.
 
---
 
## 🎮 How to Use
 
1. Run the script
2. A webcam window will open
3. Show **one hand** → glowing colored dots appear on all finger joints
4. Show **both hands** → elastic fiber web stretches between your hands
5. Move your hands apart and together to see the elastic effect
6. Press **Q** to quit
---
 
## 🎨 Visual Effects Explained
 
### LED Dots
Each of the **21 hand landmarks** (finger joints, knuckles, wrist) gets a glowing LED-style dot:
- Tiny **white specular** highlight at the center
- **Colored core** dot
- **Soft wide bloom** glow around it
- Colors **slowly cycle** through hues over time
### Color Palette
| Hand | Color Range |
|------|------------|
| Left hand | Soft purple → pink → lavender |
| Right hand | Mint → cyan → teal → green |
 
### Elastic Fiber Web
When both hands are detected, **every landmark on hand 1 connects to every landmark on hand 2** via thin warm off-white fiber threads — 441 lines total (21 × 21). Opacity subtly pulses to give a living, elastic feel.
 
### Smoothing
A landmark position smoother reduces jitter between frames, making the tracking feel fluid and natural.
 
---
 
## 📁 Project Structure
 
```
luminahands/
│
├── luminahands.py          # Main script
├── hand_landmarker.task    # Auto-downloaded on first run (~9MB)
└── README.md               # This file
```
 
---
 
## 💡 How It Works
 
```
Webcam Frame
     ↓
OpenCV captures frame
     ↓
MediaPipe Tasks API detects both hands + 21 landmarks each
     ↓
Landmark Smoother reduces jitter
     ↓
Draw elastic fiber web between hands (thin off-white lines)
     ↓
Draw LED glowing dots on all landmarks (colored + bloom)
     ↓
Display darkened frame with effects overlaid
```
 
---
 
## ⚙️ Configuration
 
You can tweak these values in `luminahands.py`:
 
| Variable | Default | Effect |
|----------|---------|--------|
| `alpha` in `LandmarkSmoother` | `0.55` | Higher = more responsive, lower = smoother |
| `radius` in `draw_led_dot` | `5` | Dot size in pixels |
| `alpha` in `draw_fiber` | `0.18` | Fiber line opacity |
| `display alpha` | `0.60` | Background darkness (0=black, 1=full bright) |
| Color shift speed | `18.0` | Higher = faster color cycling |
 
---
 
## 🆓 Cost
 
**LuminaHands is 100% free — forever.**
 
| Component | License | Cost |
|-----------|---------|------|
| Python | Open Source | Free |
| OpenCV | Apache 2.0 | Free |
| MediaPipe | Apache 2.0 | Free |
| NumPy | BSD | Free |
 
No subscriptions, no API keys, no cloud services, no expiry.
 
---
 
## 🐛 Troubleshooting
 
### Black/blank webcam window
- Check if your webcam has a **physical privacy shutter** — slide it open
- Go to **Windows Settings → Privacy → Camera** and enable camera access
- Make sure no other app (Teams, Zoom) is using the camera
### `mediapipe.solutions` error
You are using MediaPipe 0.10+. This script uses the new **Tasks API** — make sure you are using the latest `luminahands.py`
 
### Second hand not detected
- Ensure good lighting on both hands
- Keep both hands clearly visible in the frame
- Hold hands at roughly the same distance from the camera
### `pip` not recognized
Use `py -m pip install ...` instead of `pip install ...`
 
---
 
## 🙌 Credits
 
- Inspired by the **LG Elastic Stretchable Display** concept
- Hand tracking powered by **Google MediaPipe**
- Visual effect recreated by **Gomathy** using Claude AI (#vibecoding)
---
 
## 📄 License
 
MIT License — free to use, modify, and share.
 
---
 
<p align="center">Made with ❤️ using Python + OpenCV + MediaPipe</p>