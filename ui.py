"""Tkinter user interface for Tic-Tac-Toe Titans."""

from __future__ import annotations

from tkinter import Button, Frame, Label, StringVar, Tk
from tkinter import ttk

from ai import Difficulty
from constants import (
    ACCENT_COLOR,
    BG_COLOR,
    BUTTON_BG_COLOR,
    BUTTON_DISABLED_COLOR,
    FONT_MONO,
    FONT_STYLE,
    GAME_MODES,
    O_COLOR,
    PANEL_COLOR,
    TEXT_COLOR,
    TIE_BG_COLOR,
    WINNER_BG_COLOR,
    X_COLOR,
)
from game_logic import GameLogic


class TicTacToeUI:
    def __init__(self, window: Tk) -> None:
        self.window = window
        self.window.title("Tic-Tac-Toe Titans")
        self.window.configure(bg=BG_COLOR)
        self.window.resizable(False, False)

        self.game = GameLogic()
        self.buttons: list[list[Button]] = []

        self._build_header()
        self._build_board()
        self._build_footer()
        self.sync_ui()

    def _build_header(self) -> None:
        header = Frame(self.window, bg=BG_COLOR, padx=16, pady=12)
        header.pack(fill="x")

        controls = Frame(header, bg=PANEL_COLOR, padx=12, pady=10)
        controls.pack(fill="x")

        Label(
            controls,
            text="Game Mode",
            font=(FONT_STYLE, 11),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
        ).grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.game_mode_var = StringVar(value=self.game.game_mode)
        mode_dropdown = ttk.Combobox(
            controls,
            textvariable=self.game_mode_var,
            values=GAME_MODES,
            state="readonly",
            width=22,
        )
        mode_dropdown.grid(row=0, column=1, sticky="w")
        mode_dropdown.bind("<<ComboboxSelected>>", self._on_mode_change)

        Label(
            controls,
            text="AI Difficulty",
            font=(FONT_STYLE, 11),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        self.difficulty_var = StringVar(value=self.game.difficulty.value)
        self.difficulty_dropdown = ttk.Combobox(
            controls,
            textvariable=self.difficulty_var,
            values=[level.value for level in Difficulty],
            state="readonly",
            width=22,
        )
        self.difficulty_dropdown.grid(row=1, column=1, sticky="w", pady=(8, 0))
        self.difficulty_dropdown.bind(
            "<<ComboboxSelected>>", self._on_difficulty_change
        )

        self.status_label = Label(
            header,
            text="",
            font=(FONT_STYLE, 28, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
            pady=8,
        )
        self.status_label.pack(fill="x")

        action_bar = Frame(header, bg=BG_COLOR)
        action_bar.pack(fill="x", pady=(4, 0))

        for text, command in (
            ("New Game", self.restart_game),
            ("Undo", self.undo_move),
            ("Reset Scores", self.reset_scores),
        ):
            Button(
                action_bar,
                text=text,
                font=(FONT_STYLE, 12),
                bg=BUTTON_BG_COLOR,
                fg=TEXT_COLOR,
                activebackground=ACCENT_COLOR,
                activeforeground=BG_COLOR,
                relief="flat",
                padx=12,
                pady=6,
                command=command,
            ).pack(side="left", padx=4)

    def _build_board(self) -> None:
        board_frame = Frame(self.window, bg=BG_COLOR, padx=16, pady=8)
        board_frame.pack()

        grid = Frame(board_frame, bg=PANEL_COLOR, padx=8, pady=8)
        grid.pack()

        for row in range(3):
            row_buttons: list[Button] = []
            for col in range(3):
                button = Button(
                    grid,
                    text="",
                    font=(FONT_MONO, 42, "bold"),
                    width=3,
                    height=1,
                    bg=BUTTON_BG_COLOR,
                    fg=TEXT_COLOR,
                    activebackground=ACCENT_COLOR,
                    relief="flat",
                    command=lambda r=row, c=col: self.on_button_click(r, c),
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def _build_footer(self) -> None:
        self.score_label = Label(
            self.window,
            text="",
            font=(FONT_STYLE, 16),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            pady=12,
        )
        self.score_label.pack(fill="x")

    def on_button_click(self, row: int, col: int) -> None:
        if self.game.game_over:
            return

        result = self.game.make_move(row, col)
        if result.message:
            self.status_label.config(text=result.message)
        self.sync_ui()

    def sync_ui(self) -> None:
        winning_cells = {
            (row, col)
            for row, col in (self.game.winning_line or [])
        }

        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                value = self.game.board.get_cell(row, col)
                button.config(text=value.upper(), state="normal")

                if self.game.game_over:
                    button.config(state="disabled")
                    if self.game.is_tie:
                        button.config(bg=TIE_BG_COLOR, fg=BG_COLOR)
                    elif (row, col) in winning_cells:
                        button.config(bg=WINNER_BG_COLOR, fg=BG_COLOR)
                    else:
                        button.config(bg=BUTTON_DISABLED_COLOR, fg=TEXT_COLOR)
                else:
                    button.config(bg=BUTTON_BG_COLOR)
                    if value == "x":
                        button.config(fg=X_COLOR)
                    elif value == "o":
                        button.config(fg=O_COLOR)
                    else:
                        button.config(fg=TEXT_COLOR)

        if not self.game.game_over:
            self.status_label.config(
                text=f"{self.game.current_player.upper()}'s turn"
            )

        self._update_difficulty_state()
        self.update_score()

    def _update_difficulty_state(self) -> None:
        state = (
            "readonly"
            if self.game.game_mode == "Human vs Computer"
            else "disabled"
        )
        self.difficulty_dropdown.config(state=state)

    def update_score(self) -> None:
        self.score_label.config(
            text=(
                f"Score — X: {self.game.x_wins}  |  "
                f"O: {self.game.o_wins}  |  Draws: {self.game.ties}"
            )
        )

    def restart_game(self) -> None:
        self.game.start_new_game()
        self.sync_ui()

    def undo_move(self) -> None:
        result = self.game.undo_move()
        if result.success:
            self.status_label.config(text=result.message)
        self.sync_ui()

    def reset_scores(self) -> None:
        self.game.reset_scores()
        self.update_score()

    def _on_mode_change(self, _event: object) -> None:
        self.game.set_game_mode(self.game_mode_var.get())
        self.restart_game()

    def _on_difficulty_change(self, _event: object) -> None:
        self.game.set_difficulty(Difficulty(self.difficulty_var.get()))
        self.restart_game()
