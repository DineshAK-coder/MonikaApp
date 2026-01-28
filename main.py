import tkinter as tk
from PIL import Image, ImageTk
import pygetwindow as gw
import os
import random

class MonikaDesktop:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#ff00ff")
        self.root.geometry("350x450+1000+400") 

        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.canvas = tk.Canvas(root, width=350, height=450, bg="#ff00ff", highlightthickness=0)
        self.canvas.pack()

        # Load Assets
        self.images = {
            "idle": self.load_image("idle.png"),
            "happy": self.load_image("happy.png"),
            "judging": self.load_image("judging.png")
        }

        # Dialogue Database
        self.idle_quotes = [
            "Are you having a good day, [Player]?",
            "I was just thinking about you.",
            "Hey, don't forget to stretch a bit!",
            "It's nice just spending time with you like this."
        ]

        # UI Setup
        self.monika_sprite = self.canvas.create_image(175, 200, image=self.images["idle"])
        
        # Stylized Text Box (White with Rounded-style feel)
        self.text_bg = self.canvas.create_rectangle(30, 320, 320, 420, fill="white", outline="#ffbde1", width=3)
        self.dialog_text = self.canvas.create_text(175, 370, text="Just Monika.", 
                                                  width=250, font=("Verdana", 10, "bold"), fill="#5a3a3a")

        # Interactivity
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        
        # Right-Click Menu
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Force Happy", command=lambda: self.set_state("happy", "Yay!"))
        self.menu.add_command(label="Force Judging", command=lambda: self.set_state("judging", "..."))
        self.menu.add_separator()
        self.menu.add_command(label="Goodbye", command=root.destroy)
        self.canvas.bind("<Button-3>", self.show_menu)

        self.last_window = ""
        self.update_behavior()

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

    def update_behavior(self):
        try:
            active_window = gw.getActiveWindow()
            current_title = active_window.title.lower() if active_window else ""

            # Only change if the window actually switched
            if current_title != self.last_window:
                if "youtube" in current_title:
                    self.set_state("judging", "Watching videos? Focus on me.")
                elif "code" in current_title or "python" in current_title:
                    self.set_state("happy", "Coding something for us?")
                elif current_title == "":
                    self.set_state("idle", random.choice(self.idle_quotes))
                
                self.last_window = current_title
            
            # 10% chance to say something random every 10 seconds if idle
            elif random.random() < 0.1:
                self.canvas.itemconfig(self.dialog_text, text=random.choice(self.idle_quotes))

        except:
            pass
        
        self.root.after(10000, self.update_behavior) # Check every 10 seconds

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def start_move(self, event):
        self.x, self.y = event.x, event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonikaDesktop(root)
    root.mainloop()