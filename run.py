import random

def print_welcome_message():
    """
    Prints a welcome message to the player, including their name.
    """
    player_name = input("Enter your name to start: ")

    # Use a multi-line raw string for better formatting
    welcome_message = r"""
    ***********************************************
    *     Welcome {player_name} to BATTLE TIDES!          *
    *     Prepare for battle!                     *
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

        # Ask the player if they are ready to play
    while True:
        ready_to_play = input("Are you ready to play? (y/n): ").lower()
        if ready_to_play == 'y':
            print("Great! Let's start the game!")
            break
        elif ready_to_play == 'n':
            print("Okay, come back when you're ready!")
            return  # Exit the function, game won't start
        else:
            print("Invalid input. Please answer with 'y' for yes or 'n' for no.")

# Global variables
board_size = 8  # Size of the game board (8x8)
player_board = []  # Player's board
computer_board = []  # Computer's board
hidden_computer_board = []  # Computer's board with only hits/misses visible to the player
player_score = 0  # Player's score
computer_score = 0  # Computer's score
ships = [3, 3, 2, 2, 1, 1]  # Ship sizes (2 large, 2 medium, 2 small)
max_shots = 30  # Maximum number of shots
player_shots_left = max_shots  # Tracks remaining shots for the player

def create_board(size):
    """
    Creates a game board of the given size (size is defined by 'size').
    Fills the board with "~", which means an empty space.
    """
    return [["~"] * size for _ in range(size)]  # Creates a list of lists, each cell filled with "~"

def print_board(board, hide_ships=False):
    """
    Prints the board in a user-friendly way.
    Displays row and column numbers to make it easier to target shots.
    If 'hide_ships' is True, the ships on the board will not be shown.
    """
    print("  " + " ".join(str(i) for i in range(len(board[0]))))  # Print column numbers
    for index, row in enumerate(board):  # Loop through each row and print it
        if hide_ships:
            row = ['~' if cell == 'S' else cell for cell in row]  # Hide ships for the player
        print(f"{index} " + " ".join(row))  # Print row number and its content
    print("\n")

def place_ship(board, ship_size):
    """
    Places a ship on the game board. The ship is placed either horizontally or vertically.
    For each placement, it checks that there is enough space for the ship.
    """
    placed = False  # Variable to check if the ship has been placed
    while not placed:
        # Randomly choose the orientation (horizontal or vertical)
        orientation = random.choice(["horizontal", "vertical"])
        
        if orientation == "horizontal":
            # Randomly select a row and column where the ship will be placed
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - ship_size)

            # Check if all cells are empty (~)
            if all(board[row][col + i] == "~" for i in range(ship_size)):
                for i in range(ship_size):
                    board[row][col + i] = "S"  # Place the ship ("S" stands for ship)
                placed = True

        else:
            # Randomly select a row and column where the ship will be placed
            row = random.randint(0, len(board) - ship_size)
            col = random.randint(0, len(board[0]) - 1)
            
            # Check if all cells are empty (~)
            if all(board[row + i][col] == "~" for i in range(ship_size)):
                for i in range(ship_size):
                    board[row + i][col] = "S"  # Place the ship ("S" stands for ship)
                placed = True

def shoot(board, row, col):
    """
    Executes a shot at the specified location on the board.
    If the location has already been shot at (X or O), the player is informed to pick a new spot.
    If the shot hits a ship ("S"), it is marked with "X", otherwise it is marked with "O".
    """
    if board[row][col] in ["X", "O"]:
        print("You have already shot here! Choose another spot.")
        return None
    if board[row][col] == "S":
        board[row][col] = "X"  # "X" means hit
        return True
    elif board[row][col] == "~":
        board[row][col] = "O"  # "O" means miss
        return False
    return None

def get_player_shot():
    """
    Asks for the player's shot. Ensures the entered row and column are within valid limits (0-7).
    If the input is invalid, the prompt will repeat until a valid value is entered.
    """
    while True:
        try:
            row = int(input("Select a row between (0-7): "))
            col = int(input("Select a column (0-7): "))
            if 0 <= row < 8 and 0 <= col < 8:
                return row, col
            else:
                print("Please choose values between 0 and 7.")
        except ValueError:
            print("Invalid input, try again.")

def ask_play_again():
    """
    Asks the player if they want to play again after the game is over.
    Accepts 'y' or 'n' as responses. If the answer is invalid, the prompt repeats.
    """
    while True:
        replay = input("Do you want to play again? (y/n):\n ").lower()
        if replay == 'y':
            return True
        elif replay == 'n':
            return False
        else:
            print("Invalid input, please enter 'y' or 'n'.")

def play_game():
    """
    The main game logic. The player and the computer take turns shooting at each other's boards.
    The game continues until one party has sunk all of the opponent's ships or the player runs out of shots.
    """
    global player_score, computer_score, player_board, computer_board, hidden_computer_board, player_shots_left
    while True:
        # Display the player's board and the computer's board with hits/misses
        print("Player's board:")
        print_board(player_board)

        print("Computer's board with hits/misses:")
        print_board(hidden_computer_board, hide_ships=True)

        if player_shots_left == 0:
            print("You're out of shots! Game over.")
            break

        # Ask for the player's shot and check the result
        print(f"Shots remaining: {player_shots_left}")
        row, col = get_player_shot()
        player_shots_left -= 1  # Decrease shots left after each shot

        if shoot(computer_board, row, col):
            print("HIT!")
            hidden_computer_board[row][col] = "X"
            player_score += 10
        else:
            print("Miss!")
            hidden_computer_board[row][col] = "O"    

        # Check if the player has sunk all of the computer's ships
        if all(cell != "S" for row in computer_board for cell in row):
            print("Congratulations, you have sunk all of the computer's ships!")
            player_score += 50
            break

        # Computer's turn to shoot
        print("The computer shoots at your board…")
        computer_row, computer_col = random.randint(0, 7), random.randint(0, 7)
        if shoot(player_board, computer_row, computer_col):
            print(f"The computer hit on ({computer_row}, {computer_col})!")
            computer_score += 10
        else:
            print(f"The computer missed on ({computer_row}, {computer_col})!")

        # Check if the computer has sunk all of the player's ships
        if all(cell != "S" for row in player_board for cell in row):
            print("The computer has sunk all of your ships! You lost.")
            break

    # Display the final scores and ask if the player wants to play again
    print(f"\nFinal Scores:\nPlayer: {player_score}\nComputer: {computer_score}")
    if ask_play_again():
        # Reset game state for a new round
        player_board = create_board(board_size)
        computer_board = create_board(board_size)
        hidden_computer_board = create_board(board_size)
        player_shots_left = max_shots
        player_score = 0
        computer_score = 0

        # Place ships on the boards
        for ship_size in ships:
            place_ship(player_board, ship_size)
            place_ship(computer_board, ship_size)

        play_game()  # Restart the game

# Main script to initialize the game
print_welcome_message()
player_board = create_board(board_size)
computer_board = create_board(board_size)
hidden_computer_board = create_board(board_size)

# Place ships on the boards
for ship_size in ships:
    place_ship(player_board, ship_size)
    place_ship(computer_board, ship_size)

print("Player's board with ships:")
print_board(player_board, hide_ships=True)

# Start the game
play_game()

     



"""
import random

def create_board(size):
    return [["~"] * size for _ in range(size)]

def print_board(board):
    print("  " + " ".join(str(i) for i in range(len(board[0]))))
    for index, row in enumerate(board):
        print(f"{index} " + " ".join(row))
    print("\n")


def place_ship(board, ship_size):
    placed = False
    while not placed:

        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            row = random.randint(0, len(board) -1)
            col = random.randint(0, len(board[0]) - ship_size)

            if all(board[row][col + i] == "~" for i in range(ship_size)):
                for i in range(ship_size):
                    board[row][col + i] = "S"
                    placed = True

            else:
                row = random.randint(0, len(board) - ship_size)
                col = random.randint(0, len(board[0]) -1)
                if all(board[row + i][col] == "~" for i in range(ship_size)):
                    for i in range(ship_size):
                        board[row + i][col] = "S"
                    placed = True       


def shoot(board, row, col):
    if board[row][col] in ["X", "O"]:
        print("You already shot here! Choose another spot.")
        return None
    if board[row][col] == "S":
        board[row][col] = "X" # X Means hit!
        return True
    elif board[row][col] == "~":
        board[row][col] = "O" # O Means miss!
        return False
    return None

def get_player_shot():
    while True:
        try:
            row = int(input("Select a row between (0-7)"))
            col = int(input("Select a column (0-7): "))
            if 0 <= row < 8 and 0 <= col < 8:
                return row, col
            else:
                print("Please choose values ​​between 0 and 7.")
        except ValueError:
            print("Invalid input, Try again.")

board_size = 8
player_board = create_board(board_size)
computer_board = create_board(board_size)

ships = [3, 3, 2, 2, 1, 1] #Sizes of the ships, Two bigger ships (3), two medium ships(2) and 2 small ships(1)

for ship_size in ships:
    place_ship(player_board, ship_size)
    place_ship(computer_board, ship_size)

hidden_computer_board = create_board(board_size)

player_score = 0
computer_score = 0

def play_game():
    global player_score, computer_score
    while True:
        print("Players board")
        print_board(player_board)

        print("Computers board with hits/misses:")
        print_board(hidden_computer_board)

        row, col = get_player_shot()

        if shoot(computer_board, row, col):
            print("HIT!")
            hidden_computer_board[row][col] = "X"
            player_score +=10

        else:
            print("Miss!")
            hidden_computer_board[row][col] = "O"    


        if all(cell != "S" for row in computer_board for cell in row):
            print("Congratulations, you have sunk all of the computer's ships!")
            player_score += 50
            break

        print("The computer shoots at your board…")
        computer_row, computer_col = random.randint(0, 7), random.randint(0, 7)
        if shoot(player_board, computer_row, computer_col):
            print(f"The computer hit on({computer_row}, {computer_col})!")
            computer_score += 10
        else:
            print(f"The computer missed on ({computer_row}, {computer_col})!")

        if all(cell != "S" for row in player_board for cell in row):
            print("Sorry, the computer has sunk all your ships!")
            computer_score += 50
            break

        print(f"Scores: Player - {player_score}, Computer - {computer_score}\n")

print("Players board with ship:")
print_board(player_board)

play_game()
"""



"""
#board_size = 8
player_board = create_board(board_size)
computer_board = create_board(board_size)

print("Players board:")
print(player_board)

print("Computers board:")
print(player_board)

def place_ship(board):
    row = random.randint(0, len(board) -1)
    col = random.randint(0, len(board) -1)

    while board[row][col] == "S":
        row = random.randint(0, len(board) -1)
        col = random.randint(0, len(board[0]) -1)
    board[row][col] = "S"

place_ship(player_board)
place_ship(computer_board)

print("Players board with ship:")
print_board(player_board)

print("Computers board with ship (invisible for the player):")
hidden_computer_board = create_board(board_size)
print_board(hidden_computer_board)

def shoot(board, row, col):
    if board[row][col] == "S":
        board[row][col] = "X" # X means hit
        return True
    elif board[row][col] == "~":
        board[row][col] = "0" # 0 means miss
        return False
    return None

def get_player_shot():
    while True:
        try:
            row = int(input("Choose a row between (0-4): "))
            col = int(input ("Choose a column between (0-4): "))
            if 0 <= row < 5 and 0 <= col < 5:
               return row, col
            else:
                print("Please choose a value between 0 and 4.")     
        except ValueError:
            print("Unvalid input, try again.")

def play_game():

    while True:
        print("Players board:")
        print_board(player_board)

        print("Computers board with hits/misses")
        print_board(hidden_computer_board)

        row, col = get_player_shot()

        if shoot(computer_board, row, col):
            print("HIT!")
            hidden_computer_board[row][col] = "X"

        else:
            print("MISS!")
            hidden_computer_board[row][col] = "0"

        if all(cell != "S" for row in computer_board for cell in row):
            print("Congratulations, you have shoot down all the computers ship!")
            break 

        print("Computer is shooting on your board...")
        computer_row, computer_col = random.randint(0, 7), random.randint(0, 7)
        if shoot(player_board, computer_row, computer_col):
            print(f"Computer hit on ({computer_row}, {computer_col})!")
        else:
            print(f"Computer missed on ({computer_row}, {computer_col})!")

        if all(cell != "S" for row in player_board for cell in row):
            print("Sorry, computer have sunken all your ships comrat!")
            break

board_size = 8
player_board = create_board(board_size)
computer_board = create_board(board_size)

ships = [3, 3, 2, 2, 1, 1] #Two bigger ships, two medium ships and two small ships

for ship_size in ships:
    place_ship(player_board, ship_size)
    place_ship(computer_board, ship_size)

hidden_computer_board = create_board(board_size)

print("Players board with ship:")
print_board(player_board)

#play_game()
"""