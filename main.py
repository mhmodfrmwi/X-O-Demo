"""Application entry point."""

from tkinter import Tk

from ui import TicTacToeUI


def main() -> None:
    window = Tk()
    TicTacToeUI(window)
    window.mainloop()


if __name__ == "__main__":
    main()
