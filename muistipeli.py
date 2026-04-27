"""  Tämä ohjelma on suunniteltu muistin harjoittamiseen  """

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import time


class MemoryGame:
    """MemoryGame class."""
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Game")
        self.master.geometry("900x600")
        self.master.configure(bg="#1a1a2e")

        self.custom_font = ("Courgette", 14, "bold")

        self.colors = {
            'bg': "#061700",
            'sidebar_bg': "#061700",
            'card_bg': "#E7E7E7",
            'card_fg': "#1a4e0c",
            'text': "#ffffff",
            'button_bg': "#236e0e",
            'button_fg': "#ffffff",
            'combobox_bg': "#334b32",
            'combobox_fg': "#ffffff",
            'gameover_bg': "#0f3460"
        }

        self.difficulty_levels = {
            "Easy": {"grid": (4, 4), "symbols":
                      ["⟡", "♪", "☂", "✈", "☘︎", "𖢥", "✠", "☆"]},
            "Medium": {"grid": (4, 5), "symbols":
                        ["⟡", "♪", "☂", "✈", "☘︎", "𖢥", "✠", "☆", "↻", "@"]},
            "Hard": {"grid": (5, 6), "symbols":
                      ["⟡", "♪", "☂", "✈", "☘︎", "𖢥", "✠", "☆", "↻", "@", "♀", "♠", "✶", "©", "☎"]}
        }

        self.current_difficulty = "Easy"
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = None
        self.game_solved = False

        self.create_widgets()
        self.create_game_grid()

    def create_widgets(self):
        """create_widgets."""
        self.main_frame = tk.Frame(self.master, bg=self.colors['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_frame, bg=self.colors['sidebar_bg'],height=100, width=280)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.game_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=20)

        self.create_sidebar()

    def create_sidebar(self):
        """create_sidebar"""
        title_label = tk.Label(
            self.sidebar,
            text="Memory Game",
            font=("Courgette", 24, "bold"),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['text']
        )
        title_label.pack(pady=(80, 10))

        subtitle_label = tk.Label(
            self.sidebar,
            text="Test your memory",
            font=("Courgette", 16, "italic"),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['text']
        )
        subtitle_label.pack(pady=(0, 30))

        self.difficulty_label = tk.Label(
            self.sidebar,
            text="Difficulty:",
            font=self.custom_font,
            bg=self.colors['sidebar_bg'],
            fg=self.colors['text']
        )
        self.difficulty_label.pack(pady=(0, 5))

        self.style = ttk.Style()
        self.style.theme_create("modern", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": self.colors['combobox_bg'],
                    "fieldbackground": self.colors['combobox_bg'],
                    "background": self.colors['button_bg'],
                    "foreground": self.colors['combobox_fg']
                }
            }
        })
        self.style.theme_use("modern")

        self.difficulty_combobox = ttk.Combobox(
            self.sidebar,
            values=list(self.difficulty_levels.keys()),
            state="readonly",
            font=self.custom_font,
            width=10
        )
        self.difficulty_combobox.set(self.current_difficulty)
        self.difficulty_combobox.pack(pady=(0, 20))
        self.difficulty_combobox.bind("<<ComboboxSelected>>", self.change_difficulty)

        self.moves_label = tk.Label(
            self.sidebar,
            text="Moves: 0",
            font=self.custom_font,
            bg=self.colors['sidebar_bg'],
            fg=self.colors['text']
        )
        self.moves_label.pack(pady=10)

        self.time_label = tk.Label(
            self.sidebar,
            text="Time: 0:00",
            font=self.custom_font,
            bg=self.colors['sidebar_bg'],
            fg=self.colors['text']
        )
        self.time_label.pack(pady=10)

        self.new_game_button = tk.Button(
            self.sidebar,
            text="New Game",
            font=self.custom_font,
            bg=self.colors['button_bg'],
            relief=tk.FLAT,
            command=self.new_game
        )
        self.new_game_button.pack(pady=30)

        self.new_game_button.bind("<Enter>", lambda e: e.widget.config(bg="#5dbb3e"))
        self.new_game_button.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button_bg']))

    def create_game_grid(self):
        """create_game_grid"""
        self.cards_frame = tk.Frame(self.game_frame, bg=self.colors['bg'])
        self.cards_frame.pack(expand=True)

        self.cards = []
        rows, cols = self.difficulty_levels[self.current_difficulty]["grid"]
        symbols = self.difficulty_levels[self.current_difficulty]["symbols"] * 2
        random.shuffle(symbols)
        self.symbols = symbols

        for i in range(rows):
            for j in range(cols):
                card_idx = i * cols + j

                card = tk.Canvas(
                    self.cards_frame,
                    width=80,
                    height=100,
                    bg=self.colors['card_bg'],
                    highlightthickness=0
                )
                card.grid(row=i, column=j, padx=5, pady=5)

                card.bind("<Button-1>", lambda e, idx=card_idx: self.on_card_click(idx))

                card.create_rectangle(
                    5, 5, 75, 95,
                    fill=self.colors['card_bg'],
                    outline=self.colors['card_fg'],
                    width=2
                )

                card.create_text(
                    40, 50,
                    text="?",
                    font=("Courgette", 25, "bold"),
                    fill=self.colors['card_fg']
                )

                card.create_rectangle(
                    5, 5, 75, 95,
                    fill=self.colors['card_fg'],
                    outline=self.colors['card_bg'],
                    width=2,
                    state='hidden',
                    tags=('front',)
                )

                card.create_text(
                    40, 50,
                    text=self.symbols[card_idx],
                    font=("Courgette", 24, "bold"),
                    fill=self.colors['card_bg'],
                    state='hidden',
                    tags=('symbol',)
                )

                self.cards.append(card)

    def on_card_click(self, idx):
        """on_card_click"""
        if self.start_time is None:
            self.start_time = time.time()
            self.update_time()

        if idx in self.revealed or idx in self.matched_cards or len(self.revealed) == 2:
            return

        self.reveal_card(idx)
        self.revealed.append(idx)

        if len(self.revealed) == 2:
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.master.after(500, self.check_match)

    def reveal_card(self, idx):
        """reveal_card"""
        card = self.cards[idx]
        card.itemconfig('front', state='normal')
        card.itemconfig('symbol', state='normal')

    def hide_card(self, idx):
        """hide_card"""
        card = self.cards[idx]
        card.itemconfig('front', state='hidden')
        card.itemconfig('symbol', state='hidden')

    def check_match(self):
        """check_match"""
        idx1, idx2 = self.revealed
        if self.symbols[idx1] == self.symbols[idx2]:
            self.matched_pairs += 1
            self.matched_cards.extend([idx1, idx2])

            for idx in [idx1, idx2]:
                card = self.cards[idx]
                card.itemconfig('front', fill="#FFFFFF")

            if self.matched_pairs == len(self.symbols) // 2:
                self.master.after(500, self.game_over)
        else:
            self.hide_card(idx1)
            self.hide_card(idx2)

        self.revealed.clear()

    def update_time(self):
        """update_time"""
        if self.start_time and not self.game_solved:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.time_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.master.after(1000, self.update_time)

    def new_game(self):
        """new_game"""
        self.game_solved = False
        self.revealed.clear()
        self.matched_cards.clear()
        self.matched_pairs = 0
        self.moves = 0
        self.start_time = None

        self.moves_label.config(text="Moves: 0")
        self.time_label.config(text="Time: 0:00")

        self.cards_frame.destroy()
        self.create_game_grid()

    def change_difficulty(self, event):
        """change_difficulty"""
        new_difficulty = self.difficulty_combobox.get()
        if new_difficulty != self.current_difficulty:
            self.current_difficulty = new_difficulty
            self.new_game()

    def game_over(self):
        """game_over"""
        self.game_solved = True

        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)

        popup = tk.Toplevel(self.master)
        popup.title("Game Over")
        popup.geometry("300x200")
        popup.configure(bg=self.colors['gameover_bg'])
        self.master.update_idletasks()
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        popup_w = 300
        popup_h = 200
        pos_x = x + (w // 2) - (popup_w // 2)
        pos_y = y + (h // 2) - (popup_h // 2)

        popup.geometry(f"{popup_w}x{popup_h}+{pos_x}+{pos_y}")

        label = tk.Label(
            popup,
            text=f"You won!\nMoves: {self.moves}\nTime: {minutes}:{seconds:02d}",
            font=("Courgette", 14, "bold"),
            bg=self.colors['gameover_bg'],
            fg="white"
            )
        label.pack(expand=True)

        button = tk.Button(
        popup,
        text="OK",
        command=popup.destroy
        )
        button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
