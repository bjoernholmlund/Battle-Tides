import os
import time
import random

# Default settings for the game
ships = [3, 2, 1] # Sizes of ships to place on the board
max_shots = 15 # Maximum number of shots the player has


def clear_screen():
    """
    Clears the screen for better user experience.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_welcome_message():
    """
    Prints a welcome message and returns the player's name.
    Asks the player if they are ready to start the game.
    """
    player_name = input("Enter your name to start: ")
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
            time.sleep(2) # Brief pause for dramatic effect
            return player_name  # Return the player's name
        elif ready_to_play == 'n':
            print("Okay, come back when you're ready!")
            return None
        else:
            print("Invalid input. "
                  "Please answer with 'y' for yes or 'n' for no.")


def get_board_size():
    """
    Asks the player to choose the size of the game board.
    Ensures the size is between 4x4 and 10x10.
    """
    while True:
        try:
            size = int(input(
                "Enter the size of the board (e.g., 4 for a 4x4 board): "))
            if 4 <= size <= 10:
                return size
            else:
                print("Please choose a size between 4 and 10.")
        except ValueError:
            print("Invalid input. Enter a number.")


def create_board(size):
    """
    Creates an empty game board with the given size.
    """
    return [["~"] * size for _ in range(size)]


def print_board(board, hide_ships=False):
    """Prints the board with row and column labels."""
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("    " + "   ".join(letters[:len(board)])) # Column labels
    for index, row in enumerate(board):
        row_display = f"{index + 1:>1} | " # Row numbers
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
        orientation = random.choice(["horizontal", "vertical"]) # Random orientation
        if orientation == "horizontal":
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - ship_size)
            if all(board[row][col + i] == "~" for i in range(ship_size)): # Check space
                for i in range(ship_size):
                    board[row][col + i] = "S"
                placed = True
        else:
            row = random.randint(0, len(board) - ship_size)
            col = random.randint(0, len(board[0]) - 1)
            if all(board[row + i][col] == "~" for i in range(ship_size)):
                for i in range(ship_size):
                    board[row + i][col] = "S" # Place ship
                placed = True


def shoot(board, row, col):
    """
    Executes a shot and returns if it was a hit or not.
    """
    if board[row][col] in ["X", "O"]:  # Already shot
        return False  # Invalid shot
    if board[row][col] == "S":
        board[row][col] = "X"
        return True  # Hit
    else:
        board[row][col] = "O"
        return False  # Miss


def get_player_shot(board_size, computer_board, shots_taken):
    """
    Asks for player's shot and ensures valid input.
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        try:
            prompt = f"Choose a column (A-{letters[board_size - 1]}): "
            col = input(prompt).upper()
            if col not in letters[:board_size]:
                print(
                    f"Invalid column. Please choose between A and "
                    f"{letters[board_size - 1]}."
                )
                continue  # Prompt for valid input
            col_index = letters.index(col)
            row = int(input(f"Choose a row (1-{board_size}): "))
            if 1 <= row <= board_size:
                row_index = row - 1
                if (row_index, col_index) in shots_taken:
                    print("\033[93mError: You already shot here!\033[0m")
                    print("Try again.")
                    continue  # Continue prompting until a valid shot is made
                else:
                    result = shoot(computer_board, row_index, col_index)
                    shots_taken.add((row_index, col_index))  # Register shot
                    if result:
                        return row_index, col_index, True  # Hit
                    else:
                        return row_index, col_index, False  # Miss
            else:
                print(
                    "Invalid row. Please choose between 1 and "
                    f"{board_size}."
                )
        except ValueError:
            print("Invalid input, try again.")


def play_game():
    """Main game loop where player and computer take turns shooting."""
    player_name = print_welcome_message()
    if not player_name:
        return

    board_size = get_board_size()  # Get the board size
    player_board = create_board(board_size)
    computer_board = create_board(board_size)
    hidden_computer_board = create_board(board_size)
    player_shots_left = max_shots
    player_score = 0
    computer_score = 0

    shots_taken = set()  # Keeps track of all shots taken by the player

    # Place ships
    for ship_size in ships:
        place_ship(player_board, ship_size)
        place_ship(computer_board, ship_size)

    while player_shots_left > 0:
        clear_screen()
        print(f"{player_name}, here is the computer's board:")
        print_board(hidden_computer_board, hide_ships=True)
        print(f"\nShots remaining: {player_shots_left}")
        print(f"Your score: {player_score} | "
              f"Computer's score: {computer_score}")

        # Player's turn
        row, col, hit = get_player_shot(
            board_size, computer_board, shots_taken
        )
        if hit:
            print("\033[91mHIT!\033[0m")
            hidden_computer_board[row][col] = "X"
            player_score += 10
        else:
            print("\033[94mMiss!\033[0m")
            hidden_computer_board[row][col] = "O"

        time.sleep(1)

        # Computer's turn
        comp_row = random.randint(0, board_size - 1)
        comp_col = random.randint(0, board_size - 1)

        # Keep trying random locations until an empty spot is found
        while player_board[comp_row][comp_col] in ["X", "O"]:
            comp_row = random.randint(0, board_size - 1)
            comp_col = random.randint(0, board_size - 1)

        # Check if the shot was a hit or miss
        if shoot(player_board, comp_row, comp_col):
            print(f"The computer \033[91mhits\033[0m at "
                  f"({comp_row + 1}, {comp_col + 1})!")
            computer_score += 10
        else:
            print(f"The computer \033[94mmisses\033[0m at "
                  f"({comp_row + 1}, {comp_col + 1})!")

        time.sleep(1)
        player_shots_left -= 1

        clear_screen()
        print(f"Game over, {player_name}! Your score: {player_score}, "
              f"Computer's score: {computer_score}")

    # Ask if the player wants to play again
    while True:
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == "y":
            print("Great! Starting a new game...\n")
            play_game()  # Restart the game
            return  # Prevents further execution after restarting
        elif play_again == "n":
            print("Thanks for playing! Goodbye!")
            return  # Ends the game and exits the loop
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

# Start the game


play_game()