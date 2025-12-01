import tkinter as tk
from tkinter import messagebox
import platform

GRID_SIZE = 10

# Ships and sizes
ships = {
    "Destroyer": 2,
    "Submarine": 3,
    "Battleship": 4
}

# Emoji representation
ship_emojis = {
    "Destroyer": "🚢",
    "Submarine": "🚤",
    "Battleship": "🛳"
}

# OS-based emoji fonts
system = platform.system()
if system == "Windows":
    EMOJI_FONT = "Segoe UI Emoji"
elif system == "Darwin":
    EMOJI_FONT = "Apple Color Emoji"
else:
    EMOJI_FONT = "Noto Color Emoji"


class BattleshipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Battleship PvP")

        # Aesthetic theme
        self.bg = "#1e1e1e"
        self.text_color = "#ffffff"
        self.hit_color = "#ff4d4d"
        self.miss_color = "#4da6ff"
        self.root.configure(bg=self.bg)

        self.p1_wins = 0
        self.p2_wins = 0

        self.status_var = tk.StringVar()

        self.start_new_game()