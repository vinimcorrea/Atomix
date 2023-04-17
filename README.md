# Atomix Game

This project is an implementation of the Atomix game, where the player moves atoms to form a target molecule. The game features human and computer modes, with various search algorithms available for the computer mode.

## Requirements

- Python 3.8 or higher
- Pygame 2.0.1 or higher

## Installation

1. Clone this repository or download it as a ZIP file and extract it to a folder.
2. Install the required libraries using the following command:

```
pip install -r requirements.txt
```

## Running the Game

To run the game, open a terminal/command prompt in the project folder, and run the following command:

```
python atomix.py
```

## How to Play

1. From the main menu, choose between Human mode or Computer mode.
2. In Human mode, use the arrow keys to move the cursor, and press Space to select/deselect an atom. Move the selected atom to its target position to form the molecule.
3. In Computer mode, select an algorithm (uniformed or heuristic) for the computer to solve the level. Watch as the computer finds the solution and forms the molecule.
4. When a level is completed, a message is displayed with the level completion status and relevant information for the computer mode.

## Controls

- Arrow keys: Move the cursor or the selected atom.
- Spacebar: Select/deselect an atom.
- ESC key: Go back to the main menu or quit the game.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.