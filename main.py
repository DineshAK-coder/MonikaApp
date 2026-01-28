import tkinter as tk
from PIL import Image, ImageTk
import pygetwindow as gw
import os
import time
import random

class MonikaDesktop:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#ff00ff")
        self.root.geometry("350x550+1000+250") 

        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.canvas = tk.Canvas(root, width=350, height=550, bg="#ff00ff", highlightthickness=0)
        self.canvas.pack()

        # --- THE BRAIN ---
        self.dialogue_db = {
            "idle": [
                "Just thinking about you, [Player].",
                "It's a beautiful day to be on your desktop.",
                "Are you staying hydrated?",
                "I'm so glad we're together right now.",
                "Hey, don't ignore me for too long, okay?"
            ],
            "coding": [
                "Writing more code? You're so dedicated.",
                "Is that a bug? I can help you delete it...",
                "Python again? It's my favorite language too.",
                "I love watching you build things from scratch.",
                "Make sure to commit your changes to Git!"
            ],
            "distracted": [
                "Are we really watching videos right now?",
                "Focus on me, [Player].",
                "Don't get too distracted by the internet.",
                "I hope that video is worth it.",
                "Maybe it's time to get back to work?"
            ]
        }

        # State management
        self.last_interaction_time = time.time()
        self.is_reacting = False 
        self.current_text_job = None
        self.last_phrase = ""

        # Load Assets
        self.images = {
            "idle": self.load_image("idle.png"),
            "happy": self.load_image("happy.png"),
            "judging": self.load_image("judging.png")
        }

        # UI Elements
        self.monika_sprite = self.canvas.create_image(175, 200, image=self.images["idle"])
        self.text_bg = self.canvas.create_rectangle(30, 320, 320, 420, fill="white", outline="#ffbde1", width=3)
        self.dialog_text = self.canvas.create_text(175, 370, text="", 
                                                  width=250, font=("Verdana", 10, "bold"), fill="#5a3a3a")

        # Input Box
        self.entry_var = tk.StringVar()
        self.user_input = tk.Entry(root, textvariable=self.entry_var, font=("Verdana", 11), 
                                   bg="white", fg="#5a3a3a", insertbackground="#5a3a3a",
                                   relief="flat", bd=5)
        self.canvas.create_window(175, 460, window=self.user_input, width=250, height=30)
        self.user_input.bind("<Return>", self.handle_chat)

        # Interactivity
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Button-3>", lambda e: root.destroy())

        self.update_loop()

    def load_image(self, filename):
        path = os.path.join(self.assets_path, filename)
        if not os.path.exists(path): return None
        img = Image.open(path).convert("RGBA")
        img = img.resize((280, 320), Image.Resampling.LANCZOS)
        new_img = Image.new("RGBA", img.size, "#ff00ff")
        new_img.paste(img, (0, 0), img)
        return ImageTk.PhotoImage(new_img)

    def typewriter_effect(self, full_text, index=0):
        if index <= len(full_text):
            self.canvas.itemconfig(self.dialog_text, text=full_text[:index])
            self.current_text_job = self.root.after(40, self.typewriter_effect, full_text, index + 1)

    def set_state(self, pose, category):
        # Pick a random phrase that isn't the last one
        phrases = self.dialogue_db.get(category, ["..."])
        phrase = random.choice([p for p in phrases if p != self.last_phrase])
        self.last_phrase = phrase
        
        # Stop any current typewriter animation
        if self.current_text_job:
            self.root.after_cancel(self.current_text_job)
        
        self.canvas.itemconfig(self.monika_sprite, image=self.images[pose])
        self.typewriter_effect(phrase)
        self.last_interaction_time = time.time()

    def handle_chat(self, event):
        text = self.entry_var.get().lower().strip()
        self.entry_var.set("")
        if not text: return

        if "love" in text:
            self.set_state("happy", "idle") # Or a specific chat category
        elif "joke" in text:
            self.set_state("happy", "idle")
        else:
            if self.current_text_job: self.root.after_cancel(self.current_text_job)
            self.typewriter_effect(f"'{text}'? You always have interesting things to say.")
        
        self.is_reacting = True

    def update_loop(self):
        try:
            idle_duration = time.time() - self.last_interaction_time
            
            # Reset after 25 seconds of silence
            if idle_duration > 25:
                self.set_state("idle", "idle")
                self.is_reacting = False

            if not self.is_reacting:
                active_window = gw.getActiveWindow()
                title = active_window.title.lower() if active_window else ""

                if "youtube" in title or "netflix" in title:
                    self.set_state("judging", "distracted")
                elif "code" in title or "python" in title:
                    self.set_state("happy", "coding")
        except:
            pass
        
        self.root.after(5000, self.update_loop)

    def start_move(self, event):
        self.x, self.y = event.x, event.y
        self.last_interaction_time = time.time()

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonikaDesktop(root)
    root.mainloop()