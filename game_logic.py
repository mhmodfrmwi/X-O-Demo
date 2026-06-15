"""Game state management, scoring, and move orchestration."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional

from ai import Difficulty, get_computer_move
from board import Board, CellCoords, WinningLine
from constants import EMPTY_CELL, GAME_MODES, PLAYERS, SCORES_FILE


@dataclass
class MoveResult:
  success: bool
  game_over: bool = False
  winner: Optional[str] = None
  is_tie: bool = False
  winning_line: Optional[WinningLine] = None
  message: str = ""


@dataclass
class GameState:
  board: Board = field(default_factory=Board)
  current_player: str = PLAYERS[0]
  game_mode: str = GAME_MODES[0]
  difficulty: Difficulty = Difficulty.HARD
  game_over: bool = False
  winner: Optional[str] = None
  is_tie: bool = False
  x_wins: int = 0
  o_wins: int = 0
  ties: int = 0
  move_history: list[tuple[CellCoords, str]] = field(default_factory=list)


class GameLogic:
  """Coordinates board state, scoring, and computer moves."""

  def __init__(self) -> None:
    self.state = GameState()
    self._load_scores()

  @property
  def board(self) -> Board:
    return self.state.board

  @property
  def current_player(self) -> str:
    return self.state.current_player

  @property
  def game_mode(self) -> str:
    return self.state.game_mode

  @property
  def difficulty(self) -> Difficulty:
    return self.state.difficulty

  @property
  def game_over(self) -> bool:
    return self.state.game_over

  @property
  def winner(self) -> Optional[str]:
    return self.state.winner

  @property
  def is_tie(self) -> bool:
    return self.state.is_tie

  @property
  def winning_line(self) -> Optional[WinningLine]:
    return self.state.board.winning_line

  @property
  def x_wins(self) -> int:
    return self.state.x_wins

  @property
  def o_wins(self) -> int:
    return self.state.o_wins

  @property
  def ties(self) -> int:
    return self.state.ties

  @property
  def can_undo(self) -> bool:
    if self.state.game_over or not self.state.move_history:
      return False
    if self.state.game_mode == "Human vs Computer":
      return len(self.state.move_history) >= 2
    return len(self.state.move_history) >= 1

  def set_game_mode(self, mode: str) -> None:
    self.state.game_mode = mode

  def set_difficulty(self, difficulty: Difficulty) -> None:
    self.state.difficulty = difficulty

  def start_new_game(self) -> None:
    self.state.board.reset()
    self.state.current_player = PLAYERS[0]
    self.state.game_over = False
    self.state.winner = None
    self.state.is_tie = False
    self.state.move_history.clear()

    if (
      self.state.game_mode == "Human vs Computer"
      and self.state.current_player == "o"
    ):
      self._make_computer_move()

  def make_move(self, row: int, col: int) -> MoveResult:
    if self.state.game_over:
      return MoveResult(success=False, message="Game is already over.")

    if self.state.board.get_cell(row, col) != EMPTY_CELL:
      return MoveResult(success=False, message="Cell is already taken.")

    return self._apply_move(row, col, self.state.current_player)

  def undo_move(self) -> MoveResult:
    if not self.can_undo:
      return MoveResult(success=False, message="Nothing to undo.")

    moves_to_undo = 2 if self.state.game_mode == "Human vs Computer" else 1
    for _ in range(moves_to_undo):
      if not self.state.move_history:
        break
      coords, player = self.state.move_history.pop()
      row, col = coords
      self.state.board.clear_cell(row, col)
      self.state.current_player = player

    self.state.game_over = False
    self.state.winner = None
    self.state.is_tie = False
    return MoveResult(success=True, message="Move undone.")

  def _apply_move(self, row: int, col: int, player: str) -> MoveResult:
    self.state.board.set_cell(row, col, player)
    self.state.move_history.append(((row, col), player))

    winner = self.state.board.check_winner()
    if winner:
      self._finish_game(winner=winner)
      return MoveResult(
        success=True,
        game_over=True,
        winner=winner,
        winning_line=self.state.board.winning_line,
        message=f"{winner.upper()} wins!",
      )

    if self.state.board.is_full():
      self._finish_game(is_tie=True)
      return MoveResult(
        success=True,
        game_over=True,
        is_tie=True,
        message="It's a draw!",
      )

    self._switch_player()
    if (
      self.state.game_mode == "Human vs Computer"
      and self.state.current_player == "o"
      and not self.state.game_over
    ):
      self._make_computer_move()
      if self.state.game_over:
        if self.state.is_tie:
          return MoveResult(
            success=True,
            game_over=True,
            is_tie=True,
            message="It's a draw!",
          )
        return MoveResult(
          success=True,
          game_over=True,
          winner=self.state.winner,
          winning_line=self.state.board.winning_line,
          message=f"{self.state.winner.upper()} wins!",
        )

    return MoveResult(success=True, message=f"{self.state.current_player.upper()}'s turn.")

  def _make_computer_move(self) -> None:
    move = get_computer_move(
      self.state.board, "o", self.state.difficulty
    )
    if move is None:
      return
    row, col = move
    self._apply_move(row, col, "o")

  def _finish_game(
    self, winner: Optional[str] = None, is_tie: bool = False
  ) -> None:
    self.state.game_over = True
    self.state.winner = winner
    self.state.is_tie = is_tie

    if winner == "x":
      self.state.x_wins += 1
    elif winner == "o":
      self.state.o_wins += 1
    elif is_tie:
      self.state.ties += 1

    self._save_scores()

  def _switch_player(self) -> None:
    self.state.current_player = (
      PLAYERS[1] if self.state.current_player == PLAYERS[0] else PLAYERS[0]
    )

  def _load_scores(self) -> None:
    if not SCORES_FILE.exists():
      return
    with SCORES_FILE.open("r", encoding="utf-8") as file:
      scores = json.load(file)
      self.state.x_wins = scores.get("x_wins", 0)
      self.state.o_wins = scores.get("o_wins", 0)
      self.state.ties = scores.get("ties", 0)

  def _save_scores(self) -> None:
    with SCORES_FILE.open("w", encoding="utf-8") as file:
      json.dump(
        {
          "x_wins": self.state.x_wins,
          "o_wins": self.state.o_wins,
          "ties": self.state.ties,
        },
        file,
        indent=2,
      )

  def reset_scores(self) -> None:
    self.state.x_wins = 0
    self.state.o_wins = 0
    self.state.ties = 0
    self._save_scores()
