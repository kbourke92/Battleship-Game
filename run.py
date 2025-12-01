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

    # Start New Game
    def start_new_game(self):
        self.p1_grid = [["."] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.p2_grid = [["."] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.p1_original = [["."] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.p2_original = [["."] * GRID_SIZE for _ in range(GRID_SIZE)]

        self.current_player = 1
        self.phase = "placement"
        self.placement_stage = 1
        self.placing_ship_index = 0
        self.placing_orientation = "horizontal"
        self.drag_preview = []

        self.status_var.set("Player 1: Place your Destroyer")
        self.build_placement_gui()

    # Button Style
    def style_button(self, btn):
        btn.config(
            bg=self.bg,
            fg=self.text_color,
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=(EMOJI_FONT, 14)
        )
    
    # Placement UI
    def build_placement_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=f"P1 Wins: {self.p1_wins} | P2 Wins: {self.p2_wins}",
            fg=self.text_color,
            bg=self.bg,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        board_frame = tk.Frame(self.root, bg=self.bg)
        board_frame.pack()

        self.buttons = []
        grid_data = self.p1_grid if self.placement_stage == 1 else self.p2_grid

        for r in range(GRID_SIZE):
            row_buttons = []
            for c in range(GRID_SIZE):
                btn = tk.Button(board_frame, text=".", width=3, height=2)
                self.style_button(btn)

                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind("<Enter>", lambda e, rr=r, cc=c: self.preview_ship(rr, cc))
                btn.bind("<Leave>", lambda e: self.clear_preview())
                btn.bind("<Button-1>", lambda e, rr=r, cc=c: self.place_ship(rr, cc))

                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        tk.Label(self.root, textvariable=self.status_var,
                 fg=self.text_color, bg=self.bg,
                 font=("Segoe UI", 12)).pack(pady=5)

        tk.Label(self.root,
                 text="Press 'R' to rotate ship",
                 fg=self.text_color, bg=self.bg).pack()

        self.root.bind("r", self.rotate_ship)