from tkinter import Tk
from ui import TicTacToeUI

if __name__ == "__main__":
    window = Tk()
    app = TicTacToeUI(window)
    window.mainloop()