import cv2
import time
 
print("=" * 50)
print("WEBCAM DIAGNOSTIC TEST")
print("=" * 50)
 
# Test all camera backends
backends = [
    (cv2.CAP_DSHOW,   "DirectShow (CAP_DSHOW)"),
    (cv2.CAP_MSMF,    "Media Foundation (CAP_MSMF)"),
    (cv2.CAP_ANY,     "Auto (CAP_ANY)"),
]
 
working = None
 
for index in [0, 1, 2]:
    for backend, name in backends:
        print(f"\nTrying camera index {index} with {name}...")
        cap = cv2.VideoCapture(index, backend)
        time.sleep(1)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None and frame.size > 0:
                print(f"  SUCCESS! Frame size: {frame.shape}")
                working = (index, backend, name)
                cap.release()
                break
            else:
                print(f"  Opened but no frame")
        else:
            print(f"  Failed to open")
        cap.release()
    if working:
        break
 
print("\n" + "=" * 50)
if working:
    idx, backend, name = working
    print(f"WORKING: index={idx}, backend={name}")
    print(f"\nOpening live window for 5 seconds...")
    cap = cv2.VideoCapture(idx, backend)
    time.sleep(0.5)
    start = time.time()
    while time.time() - start < 5:
        ret, frame = cap.read()
        if ret and frame is not None:
            cv2.imshow("Camera Test - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Done! Camera is working.")
else:
    print("NO WORKING CAMERA FOUND!")
    print("\nPossible reasons:")
    print("  1. Another app is using the webcam (Teams, Zoom, browser)")
    print("  2. Webcam driver not installed properly")
    print("  3. Windows camera privacy settings blocking access")
    print("\nFix: Go to Windows Settings > Privacy > Camera")
    print("     Make sure 'Allow apps to access your camera' is ON")
 
input("\nPress Enter to exit...")