import os
import time
import random

# Minskat bräde
board_size = 5
ships = [3, 2, 1]
max_shots = 15

def clear_screen():
    """
    Clears the screen for better user experience.
    """
    os.system("cls" if os.name == "nt" else "clear")

def print_welcome_message():
    """
    Prints a welcome message to the player, including their name.
    """
    player_name = input("Enter your name to start: ")
    # Clear the screen after getting the player's name
    clear_screen()

    welcome_message = r"""
    ***********************************************
        Welcome {player_name} to BATTLE TIDES!         
        Prepare for battle!                     

    ***********************************************
     ____        _   _   _        _____ _     _           
    | __ )  __ _| |_| |_| | ___  |_   _(_) __| | ___  ___ 
    |  _ \ / _` | __| __| |/ _ \   | | | |/ _` |/ _ \/ __|
    | |_) | (_| | |_| |_| |  __/   | | | | (_| |  __/\__ \
    |____/ \__,_|\__|\__|_|\___|   |_| |_|\__,_|\___||___/

    You will be playing against the computer.
    Try to sink all their ships before they sink yours!
    
    Game rules:
    - Take turns shooting at each other's ships.
    - The first to sink all ships wins!
    
    Let the battle begin...!
    """
    print(welcome_message.format(player_name=player_name))

    while True:
        ready_to_play = input("Are you ready to play? (y/n): ").lower()
        if ready_to_play == 'y':
            print("Great! Let's start the game!")
            time.sleep(2)
            return True
        elif ready_to_play == 'n':
            print("Okay, come back when you're ready!")
            return False
        else:
            print("Invalid input. Please answer with 'y' for yes or 'n' for no.")

def create_board(size):
    """
    Creates an empty game board with the given size.
    """
    return [["~"] * size for _ in range(size)]

def print_board(board, hide_ships=False):
    """
    Prints the board in a simplified format with row and column labels.
    """
    letters = "ABCDE"  # Column letters
    print("    " + "   ".join(letters))  # Column headers
    for index, row in enumerate(board):
        row_display = f"{index + 1} | "  # Row numbers (1-indexed)
        row_display += "   ".join("~" if hide_ships and cell == "S" else cell for cell in row)
        print(row_display)
        if index < len(board) - 1:
            print("   " + "-" * (len(row) * 4 - 1))  # Simple line between rows

def place_ship(board, ship_size):
    """
    Places a ship randomly on the board.
    """
    placed = False
    while not placed:
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - ship_size)
            if all(board[row][col + i] == "~" for i in range(ship_size)):
                for i in range(ship_size):
                    board[row][col + i] = "S"
                placed = True
        else:
            row = random.randint(0, len(board) - ship_size)
            col = random.randint(0, len(board[0]) - 1)
            if all(board[row + i][col] == "~" for i in range(ship_size)):
                for i in range(ship_size):
                    board[row + i][col] = "S"
                placed = True

def shoot(board, row, col):
    """
    Executes a shot and returns if it was a hit.
    """
    if board[row][col] in ["X", "O"]:
        return None  # If you've already shot here, do nothing
    if board[row][col] == "S":
        board[row][col] = "X"
        return True
    else:
        board[row][col] = "O"
        return False

def get_player_shot():
    """Asks for player's shot and ensures valid input."""
    letters = "ABCDE"
    while True:
        try:
            col = input("Choose a column (A-E): ").upper()
            if col not in letters:
                print("Invalid column. Please choose between A and E.")
                continue
            col_index = letters.index(col)
            row = int(input("Choose a row (1-5): "))
            if 1 <= row <= 5:
                return row - 1, col_index  # Return 0-indexed positions
            else:
                print("Invalid row. Please choose between 1 and 5.")
        except ValueError:
            print("Invalid input, try again.")

def play_game():
    """
    Main game loop where player and computer take turns shooting.
    """
    player_board = create_board(board_size)
    computer_board = create_board(board_size)
    hidden_computer_board = create_board(board_size)
    player_shots_left = max_shots
    player_score = 0
    computer_score = 0

    # Place ships
    for ship_size in ships:
        place_ship(player_board, ship_size)
        place_ship(computer_board, ship_size)

    while player_shots_left > 0:
        clear_screen()

        # Print only the computer's board
        print("Computer's board:")
        print_board(hidden_computer_board, hide_ships=True)

        print(f"\nShots remaining: {player_shots_left}")
        print(f"Your score: {player_score} | Computer's score: {computer_score}")

        # Get player's shot
        row, col = get_player_shot()
        if shoot(computer_board, row, col):
            print("HIT!")
            hidden_computer_board[row][col] = "X"
            player_score += 10
        else:
            print("Miss!")
            hidden_computer_board[row][col] = "O"

        # Pause for 1 second to show hit/miss message
        time.sleep(1)

        # Check if all computer's ships are sunk
        if all(cell != "S" for row in computer_board for cell in row):
            clear_screen()
            print("Congratulations, you've sunk all the computer's ships!")
            break

        # Computer's turn
        comp_row, comp_col = random.randint(0, 4), random.randint(0, 4)
        while player_board[comp_row][comp_col] in ["X", "O"]:
            comp_row, comp_col = random.randint(0, 4), random.randint(0, 4)

        if shoot(player_board, comp_row, comp_col):
            print(f"The computer hit at ({comp_row + 1}, {comp_col + 1})!")
            computer_score += 10
        else:
            print(f"The computer missed at ({comp_row + 1}, {comp_col + 1})!")

        # Pause for 1 second for computer's action
        time.sleep(1)

        # Check if all player's ships are sunk
        if all(cell != "S" for row in player_board for cell in row):
            clear_screen()
            print("Sorry, the computer has sunk all your ships!")
            break

        player_shots_left -= 1

    clear_screen()
    print(f"Game over! Your score: {player_score}, Computer's score: {computer_score}")

# Start the game
print_welcome_message()
play_game()