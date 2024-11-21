import os
import time
import random

# Kartstorlek och skeppsstorlekar
board_size = 6  # Mindre spelplan (6x6)
ships = [3, 3, 2, 2, 1, 1]  # Skeppsstorlekar
max_shots = 20

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
    Skapar en tom spelplan med givna dimensioner.
    """
    return [["~"] * size for _ in range(size)]

def print_board(board, hide_ships=False):
    """
    Skriver ut spelplanen på ett användarvänligt sätt med tydliga gränser, bokstäver och nummer.
    """
    letters = "ABCDEF"  # Kolumnbokstäver för en mindre spelplan (6x6)
    print("    " + "   ".join(letters))  # Kolumnrubriker
    print("  +---+---+---+---+---+---+")  # Översta gräns
    for index, row in enumerate(board):
        row_display = f"{index} | "  # Radnummer
        for cell in row:
            # Om vi ska dölja skeppen, visa bara "~" för tomma områden
            if hide_ships and cell == "S":
                row_display += "~   "
            else:
                row_display += f"{cell}   "  # Träff eller miss
        print(row_display + "|")  # Radutskrift
        print("  +---+---+---+---+---+---+")  # Gräns för varje rad
    print("\n")

def place_ship(board, ship_size):
    """
    Placerar ett skepp på brädet i slumpmässig riktning.
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
    Utför ett skott och returnerar om det är en träff.
    """
    if board[row][col] in ["X", "O"]:
        return None  # Om du redan har skjutit här så gör ingenting
    if board[row][col] == "S":
        board[row][col] = "X"
        return True
    else:
        board[row][col] = "O"
        return False

def get_player_shot():
    """Frågar efter spelarens skott och säkerställer giltig inmatning med bokstäver."""
    letters = "ABCDEF"  # För en 6x6 bräda
    while True:
        try:
            col = input("Välj en kolumn (A-F): ").upper()
            if col not in letters:
                print("Ogiltig kolumn. Vänligen välj mellan A-F.")
                continue
            col_index = letters.index(col)
            row = int(input("Välj en rad (0-5): "))  # Anpassat för 6 rader
            if 0 <= row < 6:
                return row, col_index
            else:
                print("Ogiltig rad. Vänligen välj mellan 0-5.")
        except ValueError:
            print("Ogiltig inmatning, försök igen.")

def play_game():
    """
    Huvudspel där spelare och dator turas om att skjuta.
    """
    player_board = create_board(board_size)
    computer_board = create_board(board_size)
    hidden_computer_board = create_board(board_size)
    player_shots_left = max_shots
    player_score = 0
    computer_score = 0

    # Placera skepp
    for ship_size in ships:
        place_ship(player_board, ship_size)
        place_ship(computer_board, ship_size)

    while player_shots_left > 0:
        clear_screen()

        print("Ditt bräde:")
        print_board(player_board)

        print("Datorns bräde:")
        print_board(hidden_computer_board, hide_ships=True)

        print(f"Skott kvar: {player_shots_left}")
        print(f"Din poäng: {player_score} | Datorns poäng: {computer_score}")

        row, col = get_player_shot()

        # Spelarens tur
        if shoot(computer_board, row, col):
            print("TRÄFF!")
            hidden_computer_board[row][col] = "X"
            player_score += 10
        else:
            print("Miss!")
            hidden_computer_board[row][col] = "O"

        # Vänta 1 sekund innan skärmen uppdateras
        time.sleep(1)

        # Uppdatera endast den specifika positionen på brädet
        print("Uppdaterad spelplan efter ditt skott:")
        print_board(hidden_computer_board, hide_ships=True)

        # Kontrollera om alla datorns skepp är sänkta
        if all(cell != "S" for row in computer_board for cell in row):
            print("Grattis, du har sänkt alla datorns skepp!")
            break

        # Datorns tur
        comp_row, comp_col = random.randint(0, 5), random.randint(0, 5)  # Anpassat för 6x6
        while player_board[comp_row][comp_col] in ["X", "O"]:
            comp_row, comp_col = random.randint(0, 5), random.randint(0, 5)  # Anpassat för 6x6

        if shoot(player_board, comp_row, comp_col):
            print(f"Datorn träffade på ({comp_row}, {comp_col})!")
            computer_score += 10
        else:
            print(f"Datorn missade på ({comp_row}, {comp_col})!")

        # Vänta 1 sekund innan skärmen uppdateras
        time.sleep(1)

        # Uppdatera endast den specifika positionen på brädet
        print("Uppdaterad spelplan efter datorns skott:")
        print_board(player_board)

        # Kontrollera om alla spelarens skepp är sänkta
        if all(cell != "S" for row in player_board for cell in row):
            print("Tyvärr, datorn har sänkt alla dina skepp!")
            break

        player_shots_left -= 1

    print(f"Spelet är slut! Din poäng: {player_score}, Datorns poäng: {computer_score}")

# Starta spelet
print_welcome_message()
play_game()