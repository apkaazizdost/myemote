import cv2
import os
from deepface import DeepFace
import numpy as np

# Load emoji images once and store in dict
emotions = ['happy', 'sad', 'angry', 'neutral']
emoji_images = {}
for emo in emotions:
    path = os.path.join('emojis', f'{emo}.png')
    if os.path.exists(path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel if PNG has transparency
        emoji_images[emo] = img
    else:
        print(f"[!] Emoji image missing for '{emo}': {path}")

def overlay_emoji(frame, emoji_img, x=10, y=10, scale=0.2):
    # Resize emoji image
    h, w = emoji_img.shape[:2]
    new_w, new_h = int(w * scale), int(h * scale)
    emoji_resized = cv2.resize(emoji_img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Check if emoji has alpha channel
    if emoji_resized.shape[2] == 4:
        # Separate color and alpha channels
        emoji_rgb = emoji_resized[:, :, :3]
        alpha = emoji_resized[:, :, 3] / 255.0

        # Get region of interest on frame
        roi = frame[y:y+new_h, x:x+new_w]

        # Blend emoji with ROI using alpha mask
        for c in range(3):
            roi[:, :, c] = (alpha * emoji_rgb[:, :, c] + (1 - alpha) * roi[:, :, c])

        frame[y:y+new_h, x:x+new_w] = roi
    else:
        # No alpha channel, simple overlay
        frame[y:y+new_h, x:x+new_w] = emoji_resized

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[!] Could not open webcam.")
    exit()

print("[INFO] Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[!] Failed to grab frame.")
        break

    try:
        # Analyze emotion
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        print("Detected emotion:", dominant_emotion)

        # Overlay emoji if available
        emoji_img = emoji_images.get(dominant_emotion)
        if emoji_img is not None:
            overlay_emoji(frame, emoji_img, x=10, y=10, scale=0.3)  # Put emoji top-left, adjust scale if needed

    except Exception as e:
        print(f"[!] Error in emotion detection: {e}")

    # Show webcam with emoji overlay
    cv2.imshow("Emotion Detector", frame)

    # Quit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
