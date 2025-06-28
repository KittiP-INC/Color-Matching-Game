import tkinter as tk
from PIL import Image, ImageTk
import random
import time

# ==== CONFIG ====
NUM_ROWS = 4
NUM_COLS = 4
CARD_BACK = "images/back.png"
IMAGE_PATHS = [
    "images/img1.png", "images/img2.png", "images/img3.png", "images/img4.png",
    "images/img5.png", "images/img6.png", "images/img7.png", "images/img8.png"
]

# ==== MAIN GAME ====
class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matching Game")
        self.root.resizable(False, False)

        self.start_time = time.time()
        self.timer_running = True
        self.clicks = 0  # ⬅️ นับจำนวนครั้งที่จับคู่

        self.load_images()
        self.create_widgets()
        self.shuffle_cards()
        self.update_timer()

        self.first_card = None
        self.second_card = None
        self.lock = False
        self.matches_found = 0

    def load_images(self):
        self.card_images = {}
        self.card_back = ImageTk.PhotoImage(Image.open(CARD_BACK).resize((100, 100)))
        for i, path in enumerate(IMAGE_PATHS):
            img = Image.open(path).resize((100, 100))
            self.card_images[i] = ImageTk.PhotoImage(img)

    def shuffle_cards(self):
        self.card_values = list(range(8)) * 2
        random.shuffle(self.card_values)

    def create_widgets(self):
        self.buttons = []
        for r in range(NUM_ROWS):
            row = []
            for c in range(NUM_COLS):
                btn = tk.Button(self.root, image=self.card_back, command=lambda r=r, c=c: self.reveal_card(r, c))
                btn.grid(row=r, column=c, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Arial", 14))
        self.timer_label.grid(row=NUM_ROWS, column=0, columnspan=2)

        self.click_label = tk.Label(self.root, text="Clicks: 0", font=("Arial", 14))  # ⬅️ แสดงจำนวนคลิก
        self.click_label.grid(row=NUM_ROWS, column=2, columnspan=2)

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def reveal_card(self, r, c):
        if self.lock or self.buttons[r][c]['state'] == 'disabled':
            return

        index = r * NUM_COLS + c
        value = self.card_values[index]
        self.buttons[r][c].config(image=self.card_images[value])
        self.buttons[r][c]['state'] = 'disabled'

        if not self.first_card:
            self.first_card = (r, c, value)
        else:
            self.second_card = (r, c, value)
            self.lock = True
            self.root.after(1000, self.check_match)

    def check_match(self):
        r1, c1, val1 = self.first_card
        r2, c2, val2 = self.second_card

        self.clicks += 1  # ⬅️ เพิ่มคลิกเมื่อจับคู่
        self.click_label.config(text=f"Clicks: {self.clicks}")

        if val1 == val2:
            self.matches_found += 1
        else:
            self.buttons[r1][c1].config(image=self.card_back, state='normal')
            self.buttons[r2][c2].config(image=self.card_back, state='normal')

        self.first_card = None
        self.second_card = None
        self.lock = False

        if self.matches_found == 8:
            self.timer_running = False  # ⬅️ หยุดนับเวลา
            total_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"🎉 You win! Time: {total_time}s")
            self.click_label.config(text=f"Total Clicks: {self.clicks}")

# ==== RUN GAME ====
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
