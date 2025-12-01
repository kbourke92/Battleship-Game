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

    # Placement Logic
    def preview_ship(self, row, col):
        self.clear_preview()
        grid = self.p1_grid if self.placement_stage == 1 else self.p2_grid

        ship_name = list(ships.keys())[self.placing_ship_index]
        length = ships[ship_name]
        emoji = ship_emojis[ship_name]

        coords = []
        for i in range(length):
            r, c = row, col
            if self.placing_orientation == "horizontal":
                c += i
            else:
                r += i

            if r >= GRID_SIZE or c >= GRID_SIZE or grid[r][c] != ".":
                return

            coords.append((r, c))

        for r, c in coords:
            self.buttons[r][c].config(text=emoji)

        self.drag_preview = coords

    def clear_preview(self):
        for r, c in self.drag_preview:
            grid = self.p1_grid if self.placement_stage == 1 else self.p2_grid
            val = grid[r][c]
            self.buttons[r][c].config(text=ship_emojis[val] if val in ships else ".")
        self.drag_preview = []

    def rotate_ship(self, event):
        self.placing_orientation = (
            "vertical" if self.placing_orientation == "horizontal" else "horizontal"
        )

    def place_ship(self, row, col):
        grid = self.p1_grid if self.placement_stage == 1 else self.p2_grid
        original = self.p1_original if self.placement_stage == 1 else self.p2_original

        ship_name = list(ships.keys())[self.placing_ship_index]
        length = ships[ship_name]

        coords = []
        for i in range(length):
            r, c = row, col
            if self.placing_orientation == "horizontal":
                c += i
            else:
                r += i

            if r >= GRID_SIZE or c >= GRID_SIZE or grid[r][c] != ".":
                self.status_var.set("Cannot place ship here!")
                return
            coords.append((r, c))

        for r, c in coords:
            grid[r][c] = ship_name
            original[r][c] = ship_name
            self.buttons[r][c].config(text=ship_emojis[ship_name])

        self.placing_ship_index += 1

        # Next ship or next player or battle
        if self.placing_ship_index >= len(ships):
            if self.placement_stage == 1:
                messagebox.showinfo("Player 1 Done", "Pass to Player 2 for placement.")
                self.placement_stage = 2
                self.placing_ship_index = 0
                self.status_var.set("Player 2: Place your Destroyer")
                self.build_placement_gui()
            else:
                messagebox.showinfo("Placement Complete", "Battle begins!")
                self.build_battle_gui()
        else:
            next_ship = list(ships.keys())[self.placing_ship_index]
            self.status_var.set(f"Player {self.placement_stage}: Place your {next_ship}")

    # Battle UI
    def build_battle_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.status_var.set("Player 1's turn — fire on Player 2")

        self.target_p2_buttons = []
        self.target_p1_buttons = []

        main = tk.Frame(self.root, bg=self.bg)
        main.pack(pady=10)

        tk.Label(main, text="Target Player 2", fg=self.text_color, bg=self.bg,
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=0)
        tk.Label(main, text="Target Player 1", fg=self.text_color, bg=self.bg,
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=1)

        frame1 = tk.Frame(main, bg=self.bg)
        frame1.grid(row=1, column=0, padx=10)

        for r in range(GRID_SIZE):
            row_buttons = []
            for c in range(GRID_SIZE):
                btn = tk.Button(frame1, text=".", width=3, height=2)
                self.style_button(btn)
                btn.config(command=lambda rr=r, cc=c: self.fire(1, rr, cc))
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_buttons.append(btn)
            self.target_p2_buttons.append(row_buttons)

        frame2 = tk.Frame(main, bg=self.bg)
        frame2.grid(row=1, column=1, padx=10)

        for r in range(GRID_SIZE):
            row_buttons = []
            for c in range(GRID_SIZE):
                btn = tk.Button(frame2, text=".", width=3, height=2)
                self.style_button(btn)
                btn.config(command=lambda rr=r, cc=c: self.fire(2, rr, cc))
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_buttons.append(btn)
            self.target_p1_buttons.append(row_buttons)

        tk.Label(self.root, textvariable=self.status_var,
                 fg=self.text_color, bg=self.bg,
                 font=("Segoe UI", 12)).pack(pady=5)

        self.score_label = tk.Label(self.root,
                                    text=f"P1 Wins: {self.p1_wins} | P2 Wins: {self.p2_wins}",
                                    fg=self.text_color, bg=self.bg,
                                    font=("Segoe UI", 14, "bold"))
        self.score_label.pack()

        restart = tk.Button(self.root, text="Restart Game",
                            command=self.start_new_game)
        self.style_button(restart)
        restart.pack(pady=10)

    # Game Logic
    def fire(self, player, row, col):

        if player != self.current_player:
            self.status_var.set(f"It's Player {self.current_player}'s turn!")
            return

        if player == 1:
            grid = self.p2_grid
            btn = self.target_p2_buttons[row][col]
            original = self.p2_original
            opponent = "Player 2"
        else:
            grid = self.p1_grid
            btn = self.target_p1_buttons[row][col]
            original = self.p1_original
            opponent = "Player 1"

        if btn["text"] in ("X", "O"):
            self.status_var.set("Already fired there!")
            return

        # Hit
        if grid[row][col] != ".":
            grid[row][col] = "X"
            btn.config(text="X", bg=self.hit_color)

            ship_name = original[row][col]

                        # Collect ship's full coordinate list
            ship_cells = [(r, c) for r in range(GRID_SIZE)
                          for c in range(GRID_SIZE)
                          if original[r][c] == ship_name]

            # Check if ship destroyed
            if all(grid[r][c] == "X" for r, c in ship_cells):

                self.status_var.set(
                    f"Player {player} destroyed {opponent}'s {ship_name}!"
                )

                # Popup message
                messagebox.showinfo(
                    "Ship Destroyed",
                    f"{opponent}'s {ship_name} has been sunk!"
                )

            else:
                self.status_var.set(f"Player {player} hits!")

        # Miss
        else:
            grid[row][col] = "O"
            btn.config(text="O", bg=self.miss_color)
            self.status_var.set(f"Player {player} misses!")

        # Check win
        remaining = any(
            grid[r][c] not in (".", "X")
            for r in range(GRID_SIZE) for c in range(GRID_SIZE)
        )

        if not remaining:
            if player == 1:
                self.p1_wins += 1
                winner = "Player 1"
            else:
                self.p2_wins += 1
                winner = "Player 2"

            messagebox.showinfo(
                "Game Over",
                f"{winner} wins!\nScore: P1 {self.p1_wins} | P2 {self.p2_wins}"
            )
            self.start_new_game()
            return

        # Switch turns
        self.current_player = 2 if self.current_player == 1 else 1
        self.status_var.set(
            f"Player {self.current_player}'s turn."
        )

# Run Game
if __name__ == "__main__":
    root = tk.Tk()
    BattleshipGUI(root)
    root.mainloop()