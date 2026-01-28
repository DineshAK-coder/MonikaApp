import tkinter as tk
from PIL import Image, ImageTk
import pygetwindow as gw
import os

class MonikaDesktop:
    def __init__(self, root):
        self.root = root
        
        # 1. Window Setup
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        # We use a rare color like 'magenta' as the transparency key 
        # because Monika doesn't have much magenta in her design.
        self.root.attributes("-transparentcolor", "#ff00ff") 
        self.root.geometry("300x400+1000+400") 

        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        
        # 2. Canvas for better rendering
        # We set the highlightthickness to 0 to remove the border
        self.canvas = tk.Canvas(root, width=300, height=400, bg="#ff00ff", highlightthickness=0)
        self.canvas.pack()

        self.images = {
            "idle": self.load_image("idle.png"),
            "happy": self.load_image("happy.png"),
            "judging": self.load_image("judging.png")
        }

        # Create image and text on canvas
        self.monika_sprite = self.canvas.create_image(150, 200, image=self.images["idle"])
        
        # Text with a slight background for readability
        self.text_bg = self.canvas.create_rectangle(50, 320, 250, 380, fill="white", outline="black")
        self.dialogue_text = self.canvas.create_text(150, 350, text="Just Monika.", 
                                                    width=180, font=("Verdana", 10, "bold"), fill="black")

        # 3. Interactivity
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Button-3>", lambda e: root.destroy()) # Right click to close

        self.update_behavior()

    def load_image(self, filename):
        path = os.path.join(self.assets_path, filename)
        if not os.path.exists(path):
            # Create a placeholder if image is missing
            return None
        img = Image.open(path).convert("RGBA")
        img = img.resize((250, 300), Image.Resampling.LANCZOS)
        
        # This replaces the transparent background with our key color #ff00ff
        new_img = Image.new("RGBA", img.size, "#ff00ff")
        new_img.paste(img, (0, 0), img)
        return ImageTk.PhotoImage(new_img)

    def update_behavior(self):
        try:
            active_window = gw.getActiveWindow()
            title = active_window.title.lower() if active_window else ""

            if "youtube" in title or "netflix" in title:
                msg, img = "Watching videos? Focus on me.", self.images["judging"]
            elif "code" in title or "python" in title:
                msg, img = "I love it when you code!", self.images["happy"]
            else:
                msg, img = "I'm just happy to be here.", self.images["idle"]

            self.canvas.itemconfig(self.dialogue_text, text=msg)
            self.canvas.itemconfig(self.monika_sprite, image=img)
        except:
            pass
        
        self.root.after(3000, self.update_behavior)

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