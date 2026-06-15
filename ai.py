"""Computer opponent strategies from random play to minimax."""

from __future__ import annotations

import random
from enum import Enum

from board import Board, CellCoords


class Difficulty(str, Enum):
  EASY = "Easy"
  MEDIUM = "Medium"
  HARD = "Hard"


def get_computer_move(
  board: Board, player: str, difficulty: Difficulty
) -> CellCoords | None:
  empty_cells = board.get_empty_cells()
  if not empty_cells:
    return None

  if difficulty == Difficulty.EASY:
    return random.choice(empty_cells)

  if difficulty == Difficulty.MEDIUM:
    medium_move = _find_tactical_move(board, player)
    if medium_move:
      return medium_move
    return random.choice(empty_cells)

  return _minimax_move(board, player)


def _opponent(player: str) -> str:
  return "o" if player == "x" else "x"


def _find_tactical_move(board: Board, player: str) -> CellCoords | None:
  winning_move = _find_winning_move(board, player)
  if winning_move:
    return winning_move

  blocking_move = _find_winning_move(board, _opponent(player))
  if blocking_move:
    return blocking_move

  return None


def _find_winning_move(board: Board, player: str) -> CellCoords | None:
  for row, col in board.get_empty_cells():
    trial = board.copy()
    trial.set_cell(row, col, player)
    if trial.check_winner() == player:
      return row, col
  return None


def _minimax_move(board: Board, player: str) -> CellCoords:
  best_score = float("-inf")
  best_move = board.get_empty_cells()[0]

  for row, col in board.get_empty_cells():
    trial = board.copy()
    trial.set_cell(row, col, player)
    score = _minimax(trial, False, player, _opponent(player))
    if score > best_score:
      best_score = score
      best_move = (row, col)

  return best_move


def _minimax(
  board: Board,
  is_maximizing: bool,
  maximizing_player: str,
  minimizing_player: str,
  alpha: float = float("-inf"),
  beta: float = float("inf"),
) -> float:
  winner = board.check_winner()
  if winner == maximizing_player:
    return 1
  if winner == minimizing_player:
    return -1
  if board.is_full():
    return 0

  if is_maximizing:
    best_score = float("-inf")
    for row, col in board.get_empty_cells():
      trial = board.copy()
      trial.set_cell(row, col, maximizing_player)
      score = _minimax(
        trial, False, maximizing_player, minimizing_player, alpha, beta
      )
      best_score = max(best_score, score)
      alpha = max(alpha, score)
      if beta <= alpha:
        break
    return best_score

  best_score = float("inf")
  for row, col in board.get_empty_cells():
    trial = board.copy()
    trial.set_cell(row, col, minimizing_player)
    score = _minimax(
      trial, True, maximizing_player, minimizing_player, alpha, beta
    )
    best_score = min(best_score, score)
    beta = min(beta, score)
    if beta <= alpha:
      break
  return best_score
