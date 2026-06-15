"""Optional helper to capture a README screenshot after launching the UI."""

from pathlib import Path

from tkinter import Tk

from ui import TicTacToeUI

OUTPUT = Path(__file__).resolve().parent.parent / "docs" / "screenshot.png"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    window = Tk()
    app = TicTacToeUI(window)
    app.game.make_move(0, 0)
    app.game.make_move(1, 1)
    app.game.make_move(0, 1)
    app.sync_ui()
    window.update_idletasks()
    window.update()

    try:
        from PIL import ImageGrab
    except ImportError as exc:
        raise SystemExit(
            "Install Pillow first: pip install Pillow"
        ) from exc

    x = window.winfo_rootx()
    y = window.winfo_rooty()
    width = window.winfo_width()
    height = window.winfo_height()
    image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    image.save(OUTPUT)
    print(f"Saved screenshot to {OUTPUT}")


if __name__ == "__main__":
    main()
