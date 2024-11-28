# Battle Tides: Python Battleship Game

## Description
**Battle Tides**  is a console-based Battleship game where you play against the computer. The objective is to sink all of the opponent's ships before they sink yours. Take turns shooting at each other's ships, and try to strategize your moves to avoid being hit while hitting your opponent's ships.

This game features:

- A player vs. computer mode
* Customizable board size (4x4 to 10x10)
+ Randomized ship placement
- Turn-based gameplay
* Score tracking for both the player and the computer

## Features

- Random Ship Placement: Ships are randomly placed on the board, and the opponent’s ships are hidden.
* Hit/Miss Feedback: After each shot, the game informs the player whether the shot was a hit or miss.
+ Score Tracking: Scores for both the player and the computer are tracked and displayed during gameplay.
- Replay Option: After the game ends, the player has the option to start a new game or exit.

## How to Play

1. **Starting the Game**:

    - When the game starts, you will be prompted to enter your name.<br>
    * Then, the game will display a welcome message and explain the basic rules.<br>
    + You will be asked to choose the size of the game board (between 4x4 and 10x10).<br>

2. **Taking Turns**:

    - The game alternates between the player and the computer.<br>
    * On your turn, you will be asked to select a column (A to X) and a row (1 to the board size).<br>
    + The computer will take a shot randomly at your board.<br>
    - The game will indicate whether each shot is a hit (H) or a miss (M) for both you and the computer.<br>

3. **Winning the Game**:

- The first player to sink all the opponent's ships wins.<br>
* The game ends when the player runs out of shots or one player sinks all the ships.<br>

4. **Play Again**:

- After the game finishes, you will be asked if you want to play again. Type 'y' for yes or 'n' for no.<br>


## Game Rules

- **Ships**:

    - There are 3 ships: a 3-cell ship, a 2-cell ship, and a 1-cell ship.
    * The ships are placed randomly on the board at the start of the game, and their locations are hidden from the player.

* **Gameplay**:

    - You will take turns with the computer shooting at each other's boards.
    * The goal is to hit all the opponent's ships before they hit yours.
    + Each hit earns 10 points for the player, and the game ends when all ships are sunk.

## Testing

    I have manually tested this project using the following methods:

- Passed the code through PEP8 to ensure compliance and confirmed there are no issues.
* Tested various invalid inputs, such as entering strings where numbers were expected, providing duplicate inputs, and inputting values that were out of bounds.
+ Conducted tests in both my local terminal and the Heroku terminal to verify functionality across environments.

### Validator Testing

- <a href="https://pep8ci.herokuapp.com/"></a>
    - No errors were returned, when trying it in CI python Linter


## Challenges Faced and Fixed Bugs
**Issue: Duplicate Shots Allowed Without Warning**

While developing the game, an issue occurred where the player could shoot at the same location multiple times without any warning or indication that the spot had already been targeted. This caused the game logic to behave incorrectly, as it would overwrite the board state without informing the player.

**Solution:**

To fix this, I implemented a validation system to track and check all shots fired by the player. This was done by introducing a shots_taken set to keep track of all previously targeted positions. Additionally, the shoot function was updated to verify if the chosen cell was already marked as hit (X) or miss (O) before processing the shot. If a duplicate shot was detected, the program now informs the player and prompts them to select a new target.


## Remaining Bugs
- No bugs remaining

## Tecnoligies Used
