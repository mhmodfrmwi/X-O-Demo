"""Pure tic-tac-toe board model with no UI dependencies."""

from __future__ import annotations

from copy import deepcopy

from constants import BOARD_SIZE, EMPTY_CELL

CellCoords = tuple[int, int]
WinningLine = list[CellCoords]


class Board:
  """Represents the game board and win/tie detection logic."""

  def __init__(self) -> None:
    self._cells: list[list[str]] = [
      [EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
    ]
    self._winning_line: WinningLine | None = None

  @property
  def winning_line(self) -> WinningLine | None:
    return self._winning_line

  def reset(self) -> None:
    self._cells = [
      [EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
    ]
    self._winning_line = None

  def get_cell(self, row: int, col: int) -> str:
    return self._cells[row][col]

  def set_cell(self, row: int, col: int, player: str) -> bool:
    if self._cells[row][col] != EMPTY_CELL:
      return False
    self._cells[row][col] = player
    return True

  def is_full(self) -> bool:
    return all(cell != EMPTY_CELL for row in self._cells for cell in row)

  def get_empty_cells(self) -> list[CellCoords]:
    return [
      (row, col)
      for row in range(BOARD_SIZE)
      for col in range(BOARD_SIZE)
      if self._cells[row][col] == EMPTY_CELL
    ]

  def check_winner(self) -> str | None:
    self._winning_line = None

    for row in range(BOARD_SIZE):
      winner = self._line_winner(
        [(row, col) for col in range(BOARD_SIZE)]
      )
      if winner:
        return winner

    for col in range(BOARD_SIZE):
      winner = self._line_winner(
        [(row, col) for row in range(BOARD_SIZE)]
      )
      if winner:
        return winner

    winner = self._line_winner([(0, 0), (1, 1), (2, 2)])
    if winner:
      return winner

    winner = self._line_winner([(0, 2), (1, 1), (2, 0)])
    if winner:
      return winner

    return None

  def _line_winner(self, coords: WinningLine) -> str | None:
    values = [self._cells[row][col] for row, col in coords]
    if values[0] != EMPTY_CELL and len(set(values)) == 1:
      self._winning_line = coords
      return values[0]
    return None

  def cells(self) -> list[list[str]]:
    return deepcopy(self._cells)

  def copy(self) -> Board:
    duplicate = Board()
    duplicate._cells = deepcopy(self._cells)
    duplicate._winning_line = (
      list(self._winning_line) if self._winning_line else None
    )
    return duplicate

  def clear_cell(self, row: int, col: int) -> None:
    self._cells[row][col] = EMPTY_CELL
    self._winning_line = None
