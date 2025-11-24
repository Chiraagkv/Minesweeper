# Minesweeper

A feature-rich implementation of the classic Minesweeper game built using Python and Pygame. This project recreates the familiar puzzle experience with multiple difficulty levels, best time tracking, and polished visuals.

## Description

The objective of the game is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them. You are provided with clues about the number of neighboring mines in each field.

### Features
- **Three Difficulty Levels:** Easy (9x9), Medium (15x15), and Hard (20x20).
- **Timer & Best Score:** Tracks your current time and saves your best record for each difficulty.
- **Recursive Clearing:** Automatically reveals empty areas when a safe tile is clicked.
- **Flagging System:** Right-click to flag potential mines.
- **Sound Effects:** Audio cues for winning, losing, and flagging tiles.

## Project Structure

Here is an overview of the files in this repository and their specific roles:

- **`main.py`**: The entry point of the application. It initializes the game loop, handles user input (mouse clicks, keyboard events), and manages the overall flow of the game.
- **`game_logic.py`**: Contains the core algorithms and rules. It handles mine placement, calculating adjacent mine numbers, and the recursive logic for clearing empty areas.
- **`board.py`**: Manages the visual components. It is responsible for drawing the grid, tiles, UI elements (like the timer and mine counter), and the game-over popups.
- **`settings.py`**: A configuration file that stores constants such as colors, board dimensions, difficulty presets, and tile sizes.
- **`file_manager.py`**: Handles reading and writing data. It saves your best times to the `rec/` folder and logs game seeds for debugging or replayability.
- **`assets/`**: A directory containing game resources like images (icons) and sound files.
- **`rec/`**: A directory used to store local records, such as your best completion times.

## Prerequisites

Ensure you have the following installed:
- [Python 3.x](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/wiki/GettingStarted)

## Installation

1. Clone the repo
   ```bash
   git clone https://github.com/Chiraagkv/Minesweeper.git
   cd Minesweeper
   ```
2. Install dependecies
   ```bash
   pip install -r requirements.txt
   ```
3. Run `main.py`
   ```bash
   python3 main.py
   ```
