import tkinter as tk
from PIL import Image, ImageTk
import pygetwindow as gw
import os
import time

class MonikaDesktop:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#ff00ff")
        
        # Increased height to make room for the input on the canvas
        self.root.geometry("350x550+1000+250") 

        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.canvas = tk.Canvas(root, width=350, height=550, bg="#ff00ff", highlightthickness=0)
        self.canvas.pack()

        # State management
        self.last_interaction_time = time.time()
        self.is_reacting = False 

        # Load Assets
        self.images = {
            "idle": self.load_image("idle.png"),
            "happy": self.load_image("happy.png"),
            "judging": self.load_image("judging.png")
        }

        # 1. UI Elements on Canvas
        self.monika_sprite = self.canvas.create_image(175, 200, image=self.images["idle"])
        
        # Dialogue Box
        self.text_bg = self.canvas.create_rectangle(30, 320, 320, 420, fill="white", outline="#ffbde1", width=3)
        self.dialog_text = self.canvas.create_text(175, 370, text="Just Monika.", 
                                                  width=250, font=("Verdana", 10, "bold"), fill="#5a3a3a")

        # 2. THE INPUT BOX (Embedded in Canvas)
        self.entry_var = tk.StringVar()
        self.user_input = tk.Entry(root, textvariable=self.entry_var, font=("Verdana", 11), 
                                   bg="white", fg="#5a3a3a", insertbackground="#5a3a3a",
                                   relief="flat", bd=5)
        
        # This is the secret sauce: placing a widget inside the canvas coordinate system
        self.canvas.create_window(175, 460, window=self.user_input, width=250, height=30)
        
        self.user_input.bind("<Return>", self.handle_chat)

        # 3. Interactivity
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

    def set_state(self, pose, text):
        self.canvas.itemconfig(self.monika_sprite, image=self.images[pose])
        self.canvas.itemconfig(self.dialog_text, text=text)
        self.last_interaction_time = time.time()

    def handle_chat(self, event):
        text = self.entry_var.get().lower().strip()
        self.entry_var.set("") # Clear the box
        
        if not text: return

        if "love" in text:
            self.set_state("happy", "I love you too, [Player]! Forever.")
        elif "joke" in text:
            self.set_state("happy", "Why did the console cross the road? To get to the other IDE!")
        elif "reset" in text:
            self.set_state("idle", "Okay, I'm back to normal.")
        else:
            self.set_state("idle", f"You said: '{text}'? How sweet.")
        
        self.is_reacting = True

    def update_loop(self):
        try:
            # RESET LOGIC: Return to normal after 20 seconds of no typing/moving
            idle_duration = time.time() - self.last_interaction_time
            if idle_duration > 20 and (self.is_reacting or self.canvas.itemcget(self.monika_sprite, "image") != str(self.images["idle"])):
                self.set_state("idle", "Just resting my eyes... I'm still here.")
                self.is_reacting = False

            # WINDOW SENSING: Only if you aren't currently talking to her
            if not self.is_reacting:
                active_window = gw.getActiveWindow()
                title = active_window.title.lower() if active_window else ""

                if "youtube" in title or "netflix" in title:
                    self.set_state("judging", "Watching videos? Focus on me.")
                elif "code" in title or "python" in title:
                    self.set_state("happy", "I love watching you build things.")
        except:
            pass
        
        self.root.after(3000, self.update_loop)

    def start_move(self, event):
        self.x, self.y = event.x, event.y
        self.last_interaction_time = time.time() # Reset idle timer on click

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonikaDesktop(root)
    root.mainloop()