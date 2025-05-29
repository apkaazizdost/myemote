from emoji_float import Emojifloatwindow
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

#creating the main window

window = tk.Tk()
window.title("myemote chat")
window.geometry("400x600")

#chat display area
chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, width = 40, height = 20 , font = ("Arial",12))
chat_display.pack(pady=10)
chat_display.config(state="disabled")

#message box
entry_box=tk.Entry(window,font=("Arial",12))
entry_box.pack(fill="x", padx=10, pady=10)

#emoji display inside chat window
emoji_window = Emojifloatwindow()       #instantiate the emoji window
emoji_window.root.withdraw()            #hiding the floating emoji window

emoji_label = tk.Label(window)
emoji_label.pack(anchor="e", padx=10)

#udpdating emoji every 1 second
def update_chat_emoji():
    current_emoji = emoji_window.emoji_images[emoji_window.current_emotion]
    emoji_label.config(image=current_emoji)
    emoji_label.image = current_emoji
    window.after(1000, update_chat_emoji)

update_chat_emoji()

#sending emoji fuction
def send_emoji():
    emoji_text = f"[{emoji_window.current_emotion}emoji]"
    chat_display.config(state="normal")
    chat_display.insert(tk.END,f"you : {emoji_text}\n")
    chat_display.config(state="disabled")
    chat_display.see(tk.END)


#function to send message
def send_message():
    message = entry_box.get()
    if message.strip()!="":
        chat_display.config(state="normal")
        chat_display.insert(tk.END, f"you: {message}\n")
        chat_display.config(state="disabled")
        entry_box.delete(0,tk.END)

#send button
send_button = tk.Button(window, text="send", command=send_message, font=("Arial",12))
send_button.pack(pady=10)

entry_box.bind("<Return>", lambda event: send_message())
emoji_label.bind("<Button-1>", lambda e: send_emoji())



#strats the gui
window.mainloop()

 

