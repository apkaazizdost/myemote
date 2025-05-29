import cv2
from deepface import DeepFace
from PIL import Image, ImageTk
import tkinter as tk
import threading

def load_emoji(name):
    return ImageTk.PhotoImage(Image.open(f"emojis/{name}.png").resize((100,100)))

class Emojifloatwindow():
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.geometry("100x100+100+100")
        self.label = tk.Label(self.root)
        self.label.pack()


        self.emoji_images = {
            "happy" : load_emoji("happy"),
            "sad" : load_emoji("sad"),
            "angry" : load_emoji("angry"),
            "neutral" : load_emoji("neutral"),
        }

        self.current_emotion = "neutral"
        self.label.config(image=self.emoji_images[self.current_emotion])
        threading.Thread(target=self.detect_emotion_loop, daemon=True).start()
    
    def detect_emotion_loop(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            try:
                result = DeepFace.analyze(frame, actions=["emotion"],enforce_detection=False)
                dominant_emotion = result[0]["dominant_emotion"]
                if dominant_emotion in self.emoji_images:
                    self.current_emotion = dominant_emotion
                else:
                    self.current_emotion = "neutral"
            except:
                self.current_emotion = "neutral"
            
            self.label.config(image=self.emoji_images[self.current_emotion])
            self.label.image = self.emoji_images[self.current_emotion]


