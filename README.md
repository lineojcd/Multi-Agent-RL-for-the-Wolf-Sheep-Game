# Multi-Agent-RL-for-the-Wolf-Sheep-Game
Multi-Agent RL for the Wolf-Sheep Game

## Game Description
In the figure below, you can see how the GUI of the game looks like.

Each game is played by two players (P1 and P2) that play against each other. A player has to operate two agents: the sheep and the wolf.

The wolf's objective is to sabotage the other player, by removing food items and trying to catch the opposite player's sheep. The sheep's objective is to score as many points as possible by eating food items.

![](https://github.com/lineojcd/Multi-Agent-RL-for-the-Wolf-Sheep-Game/blob/main/src/sheepgame.png)

## Rules and Objective of the Game

### Rules:
Both, the wolf and the sheep have 5 movement options for each call:
1. move = MOVE_DOWN;
2. move = MOVE_UP;
3. move = MOVE_LEFT;
4. move = MOVE_RIGHT;
5. move = MOVE_NONE;

The **wolf** is allowed to **make a step for every second step of the sheep**. In other words the sheep can move twice as fast as the wolf.

- Wolves cannot step on squares occupied by the opponent’s wolf (wolves block each other).
- Wolves cannot step on squares occupied by the sheep of the same player.
- Sheep cannot step on squares occupied by the wolf of the same player.
- Sheep cannot step on squares occupied by the opposite sheep.
- Neither the sheep nor the wolf can enter a square with a fence on.
- Neither the sheep nor the wolf can step on a square outside the map. Imagine the map is surrounded by fences.
- If the sheep steps on a food object the food object is consumed (removed from the map) and a score is awarded.
- If the wolf steps on a food object the food object gets removed but no score is awarded.

Each game lasts for a maximum of 100 turns or unless a sheep gets caught by the wolf, then the game ends immediately.

If the wolf of player1 catches the sheep of player2 the game ends immediately and player1 wins and is awarded ${\color{red}all &ensp; the&ensp; points}$ for the current run.

### Objectives:
**For the sheep**:
- Avoid the wolf of the opposite player.
- Maximize points, by consuming as many food objects as possible.
  - The rhubarb object gives you **five** score points
  - The grass object gives you **one** score point

**For the wolf**:
- Catch the other player's sheep.
- Remove food objects to sabotage the other player.
- Block the other wolf.

## Project Setup
### Getting started
The code provided to you is written using **Python version 3.7**. The instructions given here will be to simply run the game and your code in the terminal. Alternatively, you can use an IDE of your choosing, for example **PyCharm**.

Make sure the relevant packages are installed on your computer (like **arcade** to run the graphics); in case they are not, you can install them, e.g. using pip/Anaconda/Honeybrew.

The **arcade** version used in this project is 2.0.0.

### How to run the code
- Open the terminal and change the directory to the directory where the kingsheep.py file is:
```
cd Path_To_The_Code
```
- Call the game from the python file kingsheep.py. You have the following options:
  - **-d**: turns on debug mode, and prints the state of the game after each iteration in the terminal.
  - **-v** [int]: determines the verbosity level, i.e. how much information is printed: 1 prints the elapsed time, 2 adds the system messages, 3 adds the final game state of the game.
  - **-g**: turns on the graphics, so you can see the sheep and wolves walk around and follow the progress of the game visually.
  - **-s** [float]: slows down each iteration in seconds (fractions are allowed).
  - **-p1m** [string]: enter the name of the module of player 1 here.
  - **-p1n** [string]: enter the name of the class that defines player 1 here.
  - **-p2m** [string]: enter the name of the module of player 2 here.
  - **-p2n** [string]: enter the name of the class that defines player 2 here.
  - **-h**: prints the help option in the terminal, explaining all the arguments you can used when playing the game (like described in this list here).
  - **map** [filepath/to/map.map]: the file path to the map you want to run the game with. This is the **only mandatory** argument.

For example, if you want to run the map test.map which is in the folder resources, and you want the **Random player** (defined in the class RandomPlayer in the module random_player) to play against the **Greedy player** (defined in the class GreedyPlayer in the module greedy_player), and you want the debug information, you would call the game using the following line:
```
python kingsheep.py resources/test.map -p1m random_player -p1n RandomPlayer -p2m greedy_player -p2n GreedyPlayer -d
```
Note that the player modules need to be in the same folder as the kingsheep.py file in the current setup. Also note that when you create new maps to test your agents on, they need to have the file format .map (you can simply create them in a text editor, for example by editing the provided map). If for some reason your main Python version is not python 3, replace the python in the command line call to python3 to explicitly use this version.

### Various Wolf Sheep Maps
You can create different maps . To do this, copy test.map and edit the new file in a text editor.

The map consists of 15x19 squares and each square can contain one of four elements, represented by the following symbols:
1. Empty "."
2. Grass "g"
3. Rhubarb "r"
4. Fence "#"

The start position of the players are represented by the digits:
- **S** (Sheep player 1) 
- **W** (Wolf player 1) 
- **s** (Sheep player 2) 
- **w** (Wolf player 2)

Change the symbols as you wish. You can not change the size of the map. All maps should have symbols distributed symmetrically.

Change the name of your map argument in your run configuration, to run the agents on your custom map. 

### Write your first Wolf Sheep Agent
Open the example agent file. The main functions are move_sheep() and move_wolf(). Both these functions need to return one of the possible moves (MOVE_UP, MOVE_DOWN, MOVE_RIGHT, MOVE_LEFT, MOVE_NONE). It is up to you to figure out how to determine which moves your sheep and wolf should take. Possible choices could be search tree, A* star path planing, Reinforcement Learning and etc.

There is an optional requirement that is the thinklimit for your agents, which is set to 1 second. If your agent thinks too long, the game will stop and the opponent will have won. In other words, make sure your code is not too computationally heavy. This is important as onboard computing resources are limited if you deploy your algorithm onto real robot. 

## Credits
This project uses the GUI environment from the DDIS group (led by Prof. Abraham Bernstein) of the University of Zurich.
