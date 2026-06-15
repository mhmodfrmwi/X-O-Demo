# Tic-Tac-Toe Titans

A polished desktop tic-tac-toe game built with Python and Tkinter. The project demonstrates clean architecture, minimax AI with alpha-beta pruning, automated testing, and CI.

[![CI](https://github.com/mhmodfrmwi/X-O-Demo/actions/workflows/ci.yml/badge.svg)](https://github.com/mhmodfrmwi/X-O-Demo/actions/workflows/ci.yml)

> **Screenshot:** After running the game, capture one with `python scripts/capture_screenshot.py` (requires Pillow) and save it to `docs/screenshot.png`.

## Features

- **Two game modes**: Human vs Human and Human vs Computer
- **Three AI difficulty levels**:
  - **Easy** — random moves
  - **Medium** — blocks wins and takes immediate victories
  - **Hard** — unbeatable minimax with alpha-beta pruning
- **Persistent scoreboard** with wins and draws saved to `scores.json`
- **Undo move** support (undoes the last human move, or last human + AI pair in vs-computer mode)
- **Modern dark UI** with win highlighting and end-of-game board locking
- **Fully testable game engine** decoupled from the UI

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| UI | Tkinter |
| AI | Minimax + alpha-beta pruning |
| Testing | pytest |
| Linting | ruff |
| CI | GitHub Actions |

## Architecture

```
main.py          → Application entry point
ui.py            → Tkinter presentation layer
game_logic.py    → Game state, scoring, move orchestration
board.py         → Pure board model (no UI dependencies)
ai.py            → Computer opponent strategies
constants.py     → Configuration and theme
tests/           → Unit tests for board, AI, and game logic
```

The board model is UI-agnostic, which keeps game rules testable and makes the AI work against a copy of the board without touching widgets.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Tkinter (included with most Python installs; on Linux: `sudo apt install python3-tk`)

### Installation

```bash
git clone https://github.com/mhmodfrmwi/X-O-Demo.git
cd X-O-Demo
pip install -r requirements-dev.txt
```

### Run the game

```bash
python main.py
```

### Run tests

```bash
pytest -v
```

### Lint

```bash
ruff check .
```

## CI

Every push and pull request runs linting and the full pytest suite on Python 3.10, 3.11, and 3.12 via GitHub Actions.

## Project Highlights (for your CV)

- Separated **game engine** from **UI** for maintainability and testability
- Implemented **minimax AI** with difficulty tiers
- Added **pytest** coverage for board rules, AI behavior, and game flow
- Set up **GitHub Actions CI** for automated quality checks

## License

MIT
