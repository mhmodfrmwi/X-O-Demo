from tkinter import *
import random
x_wins = 0
o_wins = 0

# Function to handle the button click for the game
def next_turn(row, column):
    global player, x_wins, o_wins

    # Reset all button backgrounds to default
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(bg='#F0F0F0')

    # Check if the clicked button is empty and there is no winner yet
    if buttons[row][column]["text"] == "" and not check_winner():
        buttons[row][column]["text"] = player  # Set the player symbol

        # Check for a winner
        if check_winner():
            update_winner()
        elif not check_empty_spaces():
            # If no winner and no empty spaces, it's a tie
            player_turn.config(text="Tie!")
            
            # Highlight all buttons in red for emphasis
            for i in range(3):
                for j in range(3):
                    buttons[i][j].config(bg='red')
        else:
            # Switch to the next player's turn
            switch_player()

        # Update the score display
        update_score()

# Function to check if there is a winner
def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            highlight_winner(row, 0, row, 1, row, 2)
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            highlight_winner(0, column, 1, column, 2, column)
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        highlight_winner(0, 0, 1, 1, 2, 2)
        return True
    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        highlight_winner(0, 2, 1, 1, 2, 0)
        return True

    return False

# Function to highlight the winning combination
def highlight_winner(*coords):
    for i in range(0, len(coords), 2):
        row, col = coords[i], coords[i + 1]
        buttons[row][col].config(bg='cyan')

# Function to update the winner and scores
def update_winner():
    global player, x_wins, o_wins
    player_turn.config(text=player + " wins!")
    if player == 'x':
        x_wins += 1
    elif player == 'o':
        o_wins += 1

# Function to switch to the next player's turn
def switch_player():
    global player
    player = players[1] if player == players[0] else players[0]
    player_turn.config(text=player + " turn")

# Function to update the score display
def update_score():
    wins_label.config(text='X = ' + str(x_wins) + ' O = ' + str(o_wins))

# Function to check if there are empty spaces left on the board
def check_empty_spaces():
    return any(buttons[i][j]['text'] == "" for i in range(3) for j in range(3))

# Function to start a new turn
def start_new_turn():
    global player
    player = random.choice(players)
    player_turn.config(text=player + " turn")

    # Reset all button texts and backgrounds
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg='#F0F0F0')

# Main Tkinter window setup
window = Tk()
window.title("X-O Game")

players = ["x", "o"]
player = random.choice(players)

buttons = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

player_turn = Label(text=(player + " turn"), font=('consolas', 40))
player_turn.pack(side="top")

restart_button = Button(text="Restart", font=('consolas', 20), command=start_new_turn)
restart_button.pack(side="top")

buttons_frame = Frame(window)
buttons_frame.pack()

# Creating buttons for the game grid
for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(buttons_frame, text="",
                                      font=('consolas', 50),
                                      width=4, height=1,
                                      command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

wins_label = Label(text="", font=("consolas", 30))
wins_label.pack(side='bottom')

window.mainloop()
