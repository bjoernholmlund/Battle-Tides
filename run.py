import os
import time
import random

# Defaultvärden
ships = [3, 2, 1]
max_shots = 15

def clear_screen():
    """Clears the screen for better user experience."""
    os.system("cls" if os.name == "nt" else "clear")

def print_welcome_message(player_name):
    """Prints a welcome message to the player."""
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

def get_board_size():
    """Asks the player to input the board size."""
    while True:
        try:
            size = int(input("Enter the size of the board (e.g., 5 for a 5x5 board): "))
            if 3 <= size <= 10:
                return size
            else:
                print("Please choose a size between 3 and 10.")
        except ValueError:
            print("Invalid input. Enter a number.")

def create_board(size):
    """Creates an empty game board with the given size."""
    return [["~"] * size for _ in range(size)]

def print_board(board, hide_ships=False):
    """Prints the board with row and column labels."""
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("    " + "   ".join(letters[:len(board)]))
    for index, row in enumerate(board):
        row_display = f"{index + 1:>2} | "
        row_display += "   ".join(
            "\033[91mX\033[0m" if cell == "X" else  # Red for hit
            "\033[94mO\033[0m" if cell == "O" else  # Blue for miss
            "~" if hide_ships and cell == "S" else cell  # Hide ships if needed
            for cell in row
        )
        print(row_display)
        if index < len(board) - 1:
            print("   " + "-" * (len(row) * 4 - 1))

def place_ship(board, ship_size):
    """Places a ship randomly on the board."""
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
    """Executes a shot and returns if it was a hit."""
    if board[row][col] in ["X", "O"]:
        return None  # Already shot here
    if board[row][col] == "S":
        board[row][col] = "X"
        return True
    else:
        board[row][col] = "O"
        return False

def get_player_shot(board_size):
    """Asks for player's shot and ensures valid input."""
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        try:
            col = input(f"Choose a column (A-{letters[board_size - 1]}): ").upper()
            if col not in letters[:board_size]:
                print(f"Invalid column. Please choose between A and {letters[board_size - 1]}.")
                continue
            col_index = letters.index(col)
            row = int(input(f"Choose a row (1-{board_size}): "))
            if 1 <= row <= board_size:
                return row - 1, col_index
            else:
                print(f"Invalid row. Please choose between 1 and {board_size}.")
        except ValueError:
            print("Invalid input, try again.")

def ask_to_play_again():
    """Asks the player if they want to play again."""
    while True:
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'y':
            return True
        elif play_again == 'n':
            print("Thanks for playing! Goodbye.")
            return False
        else:
            print("Invalid input. Please answer with 'y' for yes or 'n' for no.")

def play_game():
    """Main game loop where player and computer take turns shooting."""
    player_name = input("Enter your name to start: ")
    
    while True:
        print_welcome_message(player_name)

        board_size = get_board_size()
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
            print(f"{player_name}, here is the computer's board:")
            print_board(hidden_computer_board, hide_ships=True)
            print(f"\nShots remaining: {player_shots_left}")
            print(f"Your score: {player_score} | Computer's score: {computer_score}")

            # Player's turn
            row, col = get_player_shot(board_size)
            if shoot(computer_board, row, col):
                print("\033[91mHIT!\033[0m")
                hidden_computer_board[row][col] = "X"
                player_score += 10
            else:
                print("\033[94mMiss!\033[0m")
                hidden_computer_board[row][col] = "O"

            time.sleep(1)

            # Computer's turn
            comp_row, comp_col = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
            while player_board[comp_row][comp_col] in ["X", "O"]:
                comp_row, comp_col = random.randint(0, board_size - 1), random.randint(0, board_size - 1)

            if shoot(player_board, comp_row, comp_col):
                print(f"The computer \033[91mhits\033[0m at ({comp_row + 1}, {comp_col + 1})!")
                computer_score += 10
            else:
                print(f"The computer \033[94mmisses\033[0m at ({comp_row + 1}, {comp_col + 1})!")

            time.sleep(1)
            player_shots_left -= 1

        clear_screen()
        print(f"Game over, {player_name}! Your score: {player_score}, Computer's score: {computer_score}")

        # Ask to play again
        if not ask_to_play_again():
            break

# Start the game
play_game()