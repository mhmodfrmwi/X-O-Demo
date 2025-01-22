
from tkinter import *
from tkinter import ttk
from game_logic import GameLogic
from constants import FONT_STYLE, BUTTON_BG_COLOR, GAME_MODES

class TicTacToeUI:
    def __init__(self, window):
        self.window = window
        self.window.title("X-O Game")
        self.game = GameLogic()

        self.game_mode_var = StringVar(value=GAME_MODES[0])
        self.game_mode_dropdown = ttk.Combobox(window, textvariable=self.game_mode_var, values=GAME_MODES, state="readonly")
        self.game_mode_dropdown.pack(side="top")
        self.game_mode_dropdown.bind("<<ComboboxSelected>>", self.change_game_mode)

        self.player_turn = Label(text=(self.game.player + " turn"), font=(FONT_STYLE, 40))
        self.player_turn.pack(side="top")

        self.restart_button = Button(text="Restart", font=(FONT_STYLE, 20), command=self.restart_game)
        self.restart_button.pack(side="top")

        self.reset_scores_button = Button(text="Reset Scores", font=(FONT_STYLE, 20), command=self.reset_scores)
        self.reset_scores_button.pack(side="top")

        self.buttons_frame = Frame(window)
        self.buttons_frame.pack()
        self.create_buttons()

        self.wins_label = Label(text="", font=(FONT_STYLE, 30))
        self.wins_label.pack(side='bottom')

        self.update_score()

    def create_buttons(self):
        for row in range(3):
            for col in range(3):
                button = Button(self.buttons_frame, text="", font=(FONT_STYLE, 50), width=4, height=1,
                                command=lambda row=row, col=col: self.on_button_click(row, col))
                button.grid(row=row, column=col)
                self.game.buttons[row][col] = button

    def on_button_click(self, row, col):
        self.game.next_turn(row, col)
        self.update_ui()

    def update_ui(self):
        self.player_turn.config(text=self.game.player + " turn")
        self.update_score()

    def update_score(self):
        self.wins_label.config(text=f'X = {self.game.x_wins} O = {self.game.o_wins}')

    def restart_game(self):
        self.game.start_new_turn()
        self.update_ui()

    def reset_scores(self):
        self.game.reset_scores()
        self.update_score()

    def change_game_mode(self, event):
        self.game.set_game_mode(self.game_mode_var.get())
        self.restart_game()