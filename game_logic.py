
import random
import json
import os
from constants import PLAYERS, BOARD_SIZE, WINNER_BG_COLOR, BUTTON_BG_COLOR, TIE_BG_COLOR

class GameLogic:
    def __init__(self):
        self.x_wins = 0
        self.o_wins = 0
        self.player = None
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.game_mode = "Human vs Human"  
        self.load_scores()
        self.start_new_turn()

    def set_game_mode(self, mode):
        self.game_mode = mode

    def start_new_turn(self):
        self.player = PLAYERS[0]  
        self.reset_board()
        if self.game_mode == "Human vs Computer" and self.player == 'o':
            self.computer_move()

    def computer_move(self):
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.buttons[i][j]["text"] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.next_turn(row, col)

    def reset_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.buttons[row][col]:
                    self.buttons[row][col]["text"] = ""
                    self.buttons[row][col].config(bg=BUTTON_BG_COLOR)

    def next_turn(self, row, column):
        if self.buttons[row][column]["text"] == "" and not self.check_winner():
            self.buttons[row][column]["text"] = self.player

            if self.check_winner():
                self.update_winner()
            elif not self.check_empty_spaces():
                self.handle_tie()
            else:
                self.switch_player()
                if self.game_mode == "Human vs Computer" and self.player == 'o':
                    self.computer_move()

    def check_winner(self):
        for row in range(BOARD_SIZE):
            if self.buttons[row][0]['text'] == self.buttons[row][1]['text'] == self.buttons[row][2]['text'] != "":
                self.highlight_winner(row, 0, row, 1, row, 2)
                return True

        for column in range(BOARD_SIZE):
            if self.buttons[0][column]['text'] == self.buttons[1][column]['text'] == self.buttons[2][column]['text'] != "":
                self.highlight_winner(0, column, 1, column, 2, column)
                return True

        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != "":
            self.highlight_winner(0, 0, 1, 1, 2, 2)
            return True
        elif self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != "":
            self.highlight_winner(0, 2, 1, 1, 2, 0)
            return True

        return False

    def highlight_winner(self, *coords):
        for i in range(0, len(coords), 2):
            row, col = coords[i], coords[i + 1]
            self.buttons[row][col].config(bg=WINNER_BG_COLOR)

    def update_winner(self):
        if self.player == 'x':
            self.x_wins += 1
        elif self.player == 'o':
            self.o_wins += 1
        self.save_scores()

    def switch_player(self):
        self.player = PLAYERS[1] if self.player == PLAYERS[0] else PLAYERS[0]

    def check_empty_spaces(self):
        return any(self.buttons[i][j]['text'] == "" for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

    def handle_tie(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.buttons[row][col].config(bg=TIE_BG_COLOR)

    def load_scores(self):
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as file:
                scores = json.load(file)
                self.x_wins = scores.get("x_wins", 0)
                self.o_wins = scores.get("o_wins", 0)

    def save_scores(self):
        with open("scores.json", "w") as file:
            json.dump({"x_wins": self.x_wins, "o_wins": self.o_wins}, file)

    def reset_scores(self):
        self.x_wins = 0
        self.o_wins = 0
        self.save_scores()