BeeHave

Final project for beginners' Python programming course
This is an endless runner game implemented in Python using the Pygame library. The player controls a bee who continuously flies in a sky, avoiding polluted rain drops and collecting lives to achieve a high score.

Made using PyCharm Community Edition 2022.3.2

To use project:

## Installation
1. Clone the repository
2. Navigate to the project directory
3. Create virtual enviroment
4. Install the required dependencies

## How to Play
1. Run the game script: main.py
2. Use left and right arrow keys to control the character's movements.
3. Avoid rain drops by going from one side to another.
4. Collect hearts to get more lives
5. The game ends if the player looses all lives

## Features
- Endless gameplay with increasing difficulty.
- Smooth character movement.
- Randomly generated obstacles and lives.
- Score tracking and high score display.

## File Structure
- `main.py`: The main script to run the game.
- `player.py`: Contains the player class and related functionality.
- `obstacle.py`: Defines the obstacle class and its behavior.
- `life.py`: Manages player lives
- `heart.py`: Creates hearts to get back lost lives when collected
- `button.py`: Handles menu actions like play button or quit button
- `highscore.py`: Manages highscore and last score
- `images/`: Directory containing images
- `fonts/`: Directory containing custom fonts used in the game.
- `score.db`:Database for storing score
- `README.md`: This file.
