"""Game configuration and theme constants."""

from pathlib import Path

PLAYERS: list[str] = ["x", "o"]
BOARD_SIZE: int = 3
EMPTY_CELL: str = ""

GAME_MODES: list[str] = ["Human vs Human", "Human vs Computer"]

# Dark theme
BG_COLOR: str = "#1e1e2e"
PANEL_COLOR: str = "#313244"
BUTTON_BG_COLOR: str = "#45475a"
BUTTON_HOVER_COLOR: str = "#585b70"
BUTTON_DISABLED_COLOR: str = "#313244"
TEXT_COLOR: str = "#cdd6f4"
ACCENT_COLOR: str = "#89b4fa"
WINNER_BG_COLOR: str = "#a6e3a1"
TIE_BG_COLOR: str = "#f9e2af"
X_COLOR: str = "#f38ba8"
O_COLOR: str = "#89dceb"

FONT_STYLE: str = "Segoe UI"
FONT_MONO: str = "Consolas"

SCORES_FILE: Path = Path(__file__).resolve().parent / "scores.json"
