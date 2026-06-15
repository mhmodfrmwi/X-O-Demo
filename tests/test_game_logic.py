"""Tests for game orchestration and scoring."""

import json
from pathlib import Path

import pytest

from ai import Difficulty
from game_logic import GameLogic


@pytest.fixture
def game(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> GameLogic:
    scores_file = tmp_path / "scores.json"
    monkeypatch.setattr("game_logic.SCORES_FILE", scores_file)
    monkeypatch.setattr("constants.SCORES_FILE", scores_file)
    return GameLogic()


def test_human_win_updates_score(game: GameLogic):
    game.make_move(0, 0)
    game.make_move(1, 0)
    game.make_move(0, 1)
    game.make_move(1, 1)
    result = game.make_move(0, 2)

    assert result.game_over is True
    assert result.winner == "x"
    assert game.x_wins == 1


def test_draw_is_recorded(game: GameLogic):
    game.set_game_mode("Human vs Human")
    moves = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 0),
        (1, 2),
        (2, 1),
        (2, 0),
        (2, 2),
    ]
    for row, col in moves:
        game.make_move(row, col)

    assert game.is_tie is True
    assert game.ties == 1


def test_invalid_move_after_game_over(game: GameLogic):
    game.make_move(0, 0)
    game.make_move(1, 0)
    game.make_move(0, 1)
    game.make_move(1, 1)
    game.make_move(0, 2)

    result = game.make_move(2, 2)
    assert result.success is False


def test_undo_in_human_mode(game: GameLogic):
    game.set_game_mode("Human vs Human")
    game.make_move(0, 0)
    game.make_move(1, 1)

    result = game.undo_move()

    assert result.success is True
    assert game.board.get_cell(1, 1) == ""
    assert game.current_player == "o"


def test_scores_persist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    scores_file = tmp_path / "scores.json"
    monkeypatch.setattr("game_logic.SCORES_FILE", scores_file)
    monkeypatch.setattr("constants.SCORES_FILE", scores_file)

    first_session = GameLogic()
    first_session.make_move(0, 0)
    first_session.make_move(1, 0)
    first_session.make_move(0, 1)
    first_session.make_move(1, 1)
    first_session.make_move(0, 2)

    second_session = GameLogic()
    assert second_session.x_wins == 1

    payload = json.loads(scores_file.read_text(encoding="utf-8"))
    assert payload == {"x_wins": 1, "o_wins": 0, "ties": 0}


def test_reset_scores(game: GameLogic):
    game.state.x_wins = 2
    game.state.o_wins = 1
    game.state.ties = 3
    game.reset_scores()

    assert game.x_wins == 0
    assert game.o_wins == 0
    assert game.ties == 0


def test_computer_mode_uses_selected_difficulty(game: GameLogic):
    game.set_game_mode("Human vs Computer")
    game.set_difficulty(Difficulty.EASY)
    assert game.difficulty == Difficulty.EASY
