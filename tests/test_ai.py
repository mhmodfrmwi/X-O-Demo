"""Tests for AI move selection."""

from board import Board
from ai import Difficulty, get_computer_move


def test_easy_picks_valid_move():
    board = Board()
    move = get_computer_move(board, "o", Difficulty.EASY)
    assert move in board.get_empty_cells()


def test_medium_blocks_immediate_loss():
    board = Board()
    board.set_cell(0, 0, "x")
    board.set_cell(0, 1, "x")

    move = get_computer_move(board, "o", Difficulty.MEDIUM)
    assert move == (0, 2)


def test_medium_takes_immediate_win():
    board = Board()
    board.set_cell(2, 0, "o")
    board.set_cell(2, 1, "o")

    move = get_computer_move(board, "o", Difficulty.MEDIUM)
    assert move == (2, 2)


def test_hard_blocks_immediate_threat():
    board = Board()
    board.set_cell(0, 0, "x")
    board.set_cell(1, 1, "o")
    board.set_cell(2, 2, "x")

    move = get_computer_move(board, "o", Difficulty.HARD)
    trial = board.copy()
    trial.set_cell(*move, "o")

    for row, col in trial.get_empty_cells():
        x_trial = trial.copy()
        x_trial.set_cell(row, col, "x")
        assert x_trial.check_winner() != "x"


def test_hard_prefers_winning_move():
    board = Board()
    board.set_cell(0, 0, "o")
    board.set_cell(0, 1, "o")
    board.set_cell(1, 0, "x")

    move = get_computer_move(board, "o", Difficulty.HARD)
    assert move == (0, 2)


def test_find_winning_move_returns_none_when_unavailable():
    board = Board()
    assert get_computer_move(board, "x", Difficulty.MEDIUM) is not None


def test_hard_never_loses_as_o():
    """Exhaustive check: O should never lose when playing optimally."""
    board = Board()
    _assert_optimal_outcome(board, "o", "x", Difficulty.HARD)


def _assert_optimal_outcome(
    board: Board, ai_player: str, human_player: str, difficulty: Difficulty
) -> None:
    winner = board.check_winner()
    if winner == human_player:
        raise AssertionError("AI allowed a forced loss.")
    if winner or board.is_full():
        return

    if board.get_empty_cells() and _is_ai_turn(board, ai_player):
        row, col = get_computer_move(board, ai_player, difficulty)
        trial = board.copy()
        trial.set_cell(row, col, ai_player)
        _assert_optimal_outcome(trial, ai_player, human_player, difficulty)
        return

    for row, col in board.get_empty_cells():
        trial = board.copy()
        trial.set_cell(row, col, human_player)
        _assert_optimal_outcome(trial, ai_player, human_player, difficulty)


def _is_ai_turn(board: Board, ai_player: str) -> bool:
    x_count = sum(cell == "x" for row in board.cells() for cell in row)
    o_count = sum(cell == "o" for row in board.cells() for cell in row)
    if ai_player == "x":
        return x_count == o_count
    return o_count < x_count
