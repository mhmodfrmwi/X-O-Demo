"""Tests for the Board model."""

from board import Board


def test_empty_board_has_no_winner():
    board = Board()
    assert board.check_winner() is None
    assert board.winning_line is None


def test_row_win():
    board = Board()
    board.set_cell(0, 0, "x")
    board.set_cell(0, 1, "x")
    board.set_cell(0, 2, "x")

    assert board.check_winner() == "x"
    assert board.winning_line == [(0, 0), (0, 1), (0, 2)]


def test_column_win():
    board = Board()
    board.set_cell(0, 1, "o")
    board.set_cell(1, 1, "o")
    board.set_cell(2, 1, "o")

    assert board.check_winner() == "o"


def test_diagonal_win():
    board = Board()
    board.set_cell(0, 0, "x")
    board.set_cell(1, 1, "x")
    board.set_cell(2, 2, "x")

    assert board.check_winner() == "x"


def test_anti_diagonal_win():
    board = Board()
    board.set_cell(0, 2, "o")
    board.set_cell(1, 1, "o")
    board.set_cell(2, 0, "o")

    assert board.check_winner() == "o"


def test_cannot_overwrite_cell():
    board = Board()
    assert board.set_cell(1, 1, "x") is True
    assert board.set_cell(1, 1, "o") is False
    assert board.get_cell(1, 1) == "x"


def test_board_full():
    board = Board()
    moves = [
        (0, 0, "x"),
        (0, 1, "o"),
        (0, 2, "x"),
        (1, 0, "o"),
        (1, 1, "x"),
        (1, 2, "o"),
        (2, 0, "o"),
        (2, 1, "x"),
        (2, 2, "o"),
    ]
    for row, col, player in moves:
        board.set_cell(row, col, player)

    assert board.is_full() is True
    assert board.check_winner() is None


def test_reset_board():
    board = Board()
    board.set_cell(0, 0, "x")
    board.reset()

    assert board.get_cell(0, 0) == ""
    assert board.check_winner() is None


def test_copy_is_independent():
    board = Board()
    board.set_cell(0, 0, "x")
    duplicate = board.copy()
    duplicate.set_cell(1, 1, "o")

    assert board.get_cell(1, 1) == ""
    assert duplicate.get_cell(0, 0) == "x"
