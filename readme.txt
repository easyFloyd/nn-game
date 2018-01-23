# Usage:

 1. Training:
  - python main.py train
  - This command will collect training data from 10.000 random game,
    create the neural network (see the arhitecture below),
    and train it with tflearn, then save the results.
    In the end it will test the results on 100 game, and print the failed games's last observations, and the predicted move.
 2. Testing:
  - python main.py test
  - This command will run 100 test games, and print the failed games's last observations, and the predicted move.
    You should only use this command, if there are already saved results by training.
 3. Visualise:
  - python main.py visualise
  - This command will use the game's gui to watch a test game.
    You should only use this command, if there are already saved results by training.

# The game:

It's a very primitive game, where the starting situation is:
 - a board (board_width x board_height)
 - a player (O) start the game on the baseline
 - a goal area (4 unit) is on the finish line
 - some (opponents_number) random opponent (X) on the board
In every turn 
 - the player can take a step (Up, Down, Left or Right)
 - then the opponents take a random step (at the case, when the 'hard' option is True, not truly random)
The goal is:
 - the player have to reach the goal area in such a way, that it doesn't bump any opponent, and stay on the board

Options:
 - gui = True: Visualise the game on the screen (use the curses library)
 - hard = True: The opponents try to move in front of the player 
   (It shouldn't be used, because in most cases it could end in an infinite game)

# The neural network:

It has three layers:
 - Input layer: 6 neurons
  - 1. is there an obstacle in the UP direction
  - 2. is there an obstacle in the DOWN direction
  - 3. is there an obstacle in the LEFT direction
  - 4. is there an obstacle in the RIGHT direction
  - 5. is the goal on the right side (-1) of the player, or the left (+1), or front of it (0)
  - 6. the predicted direction (0: UP, 1: DOWN, 2: LEFT, 3: RIGHT)
 - Hidden layer: 36 neurons
  - It uses ReLU activation function
 - Output layer: 1 neuron
  - Should the player go to that direction or not (
    -1: the player bump an obstacle and the game is over, 
     0: the game is not over, but the goal area doesn't get closer,
    +1: the game is not over, and the goal area is getting closer)
    
    
