# Multi-Agent-RL-for-the-Wolf-Sheep-Game
Multi-Agent RL for the Wolf-Sheep Game

## Game Description
In the figure below, you can see how the GUI of the game looks like.

Each game is played by two players (P1 and P2) that play against each other. A player has to operate two agents: the **sheep** and the **wolf**.

The wolf's objective is to sabotage the other player, by removing food items and trying to catch the opposite player's sheep. The sheep's objective is to score as many points as possible by eating food items.

![](https://github.com/lineojcd/Multi-Agent-RL-for-the-Wolf-Sheep-Game/blob/main/src/sheepgame.png)

## Rules and Objective of the Game

### Rules:
Both, the wolf and the sheep have 5 movement options for each call:
1. move = MOVE_DOWN, represented by 1
2. move = MOVE_UP, represented by -1
3. move = MOVE_LEFT, represented by -2
4. move = MOVE_RIGHT, represented by 2
5. move = MOVE_NONE, represented by 0

The **wolf** is allowed to **make a step for every second step of the sheep**. In other words the sheep can move twice as fast as the wolf.

- Wolves cannot step on squares occupied by the opponent’s wolf (wolves block each other).
- Wolves cannot step on squares occupied by the sheep of the same player.
- Sheep cannot step on squares occupied by the wolf of the same player.
- Sheep cannot step on squares occupied by the opposite sheep.
- Neither the sheep nor the wolf can enter a square with a fence on.
- Neither the sheep nor the wolf can step on a square outside the map. Imagine the map is surrounded by fences.
- If the sheep steps on a food object the food object is consumed (removed from the map) and a score is awarded.
- If the wolf steps on a food object the food object gets removed but no score is awarded.

Each game lasts for a **maximum of 100 turns** or unless a sheep gets caught by the wolf, then the game ends immediately.

If the wolf of player1 catches the sheep of player2 the game ends immediately and player1 wins and is awarded ${\color{red}all &ensp; the&ensp; points}$ for the current run.

This is a **fully observable environment** meaning that you can have all the information in each step including where the food is and the enemy sheep or wolf is.

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

The start position of the players are represented by these letters:
- **S** (Sheep player 1) 
- **W** (Wolf player 1) 
- **s** (Sheep player 2) 
- **w** (Wolf player 2)

Change the symbols as you wish. You can not change the size of the map. All maps should have symbols distributed symmetrically.

Change the name of your map argument in your run configuration, to run the agents on your custom map. 

### Write your first Wolf Sheep Agent
Open the example agent file. The main functions are **move_sheep()** and **move_wolf()**. Both these functions need to return one of the possible moves (MOVE_UP, MOVE_DOWN, MOVE_RIGHT, MOVE_LEFT, MOVE_NONE). It is up to you to figure out how to determine which moves your sheep and wolf should take. Possible choices could be search tree, A* star path planing, Reinforcement Learning and etc.

There is an **optional requirement** that is the thinklimit for your agents, which is set to 1 second. If your agent thinks too long, the game will stop and the opponent will have won. In other words, make sure your code is not too computationally heavy. This is important as onboard computing resources are limited if you deploy your algorithm onto real robot. 

### Running platform configuration
This program ran on a MacBook Pro with a 2.2 GHz i7 core and 16 GB memory.

### Code structure
The folder contains the following files:
- config.py: this file sets the global variables such as field height.
- kingsheep.py: this file runs the game and is the main file.
- ksgraphics.py: this files allows showing the game in its graphical representation
- resources: a folder containing the test map and images needed for the graphical representation
- Four preset players:
  - Greedy player: this agent uses a simply greedy approach
  - Keyboard player: use this agent to play with your keyboard rather than an algorithm
  - Passive player: this agent simply stays in place
  - Random player: this player makes a random move every turn
- One example agent (example_player.py) 

You are given the example agent to get started. You need to do the following within this file (this instruction is also included in the file, and will make more sense once you open the file):
- Change the name of your file to '[playername]_A1.py', where [playername] can be chosen by yourself.
- Change the name of the class to a name of your choosing.
- Change the def 'get_class_name()' to return the new name of your class
- Change the init of your class:
  - self.name can be an (anonymous) name of your choosing
  - self.playername needs to be your playername
- Update move_sheep() and move_wolf() function 

In addition to the preset agent, we developed others agents to play the Wolf sheep game. My new agents will be introduced under the **Agents** section below:

## Agents
The Agents are the key of this project as different agents have different capability to win the game.
### Random player
A preset agent that moves randomly every turn.
### Keyboard player
A preset agent that receives your keyboard command rather than controlled by an algorithm.
### Passive player
A preset agent that simply **stays** in place every turn.
### Greedy player
A preset agent that uses a simply greedy approach. It includes the following functions:
- get_player_position() gets the current position of the player's or enemy player's sheep or wolf.
- food_present() tells you if the food is still available in the map.
- valid_move() checks if the action you are going to take is valid or not.
- closest_goal() returns the nearest food position based on manhattan distance and ignore the obstables during the way.
- wolf_close() returns True/False is the enemy wolf is close to your sheep.
- run_from_wolf() takes action to run from enemy wolf.
- gather_closest_goal()：see pseudocode below
```
if the goal and my position are in the same column:
  if the goal right above me:
    if valid_move(above_grid):
      return MOVE_UP
    else:
      return MOVE_RIGHT
  else:
    if valid_move(below_grid):
      return MOVE_DOWN
    else:
      return MOVE_RIGHT
elif the goal and my position are in the same row:
  if the goal is on my left:
    if valid_move(left_grid);
      return MOVE_LEFT
    else:
      MOVE_UP
  else:
    if valid_move(right_grid);
      return MOVE_RIGHT
    else:
      MOVE_UP
else:
  #go left or up
  if the goal is on my left and above:
    if valid_move(left_grid):
      return MOVE_LEFT
    else:
      return MOVE_UP
  #go left or down
  elif the goal is on my left and below:
    if valid_move(left_grid):
        return MOVE_LEFT
    else:
        return MOVE_DOWN
  #go right or up
  elif the goal is on my right and above:    
    if valid_move(right_grid):
        return MOVE_RIGHT
    else:
        return MOVE_UP
  #go right or down
  elif the goal is on my right and below:
    if valid_move(right_grid):
        return MOVE_RIGHT
    else:
        return MOVE_DOWN
  else:
      print('fail')
      return MOVE_NONE
```
- move_wolf() takes enemy sheep as the goal and move towards it
- move_sheep() see pseudocode below
```
if wolf_close:
  return run_from_wolf()
elif food_present():
  return gather_closest_goal(closest_goal())
else:
  return MOVE_NON
```
The drawback of this strategy is shown in the gif below:
![](https://github.com/lineojcd/Multi-Agent-RL-for-the-Wolf-Sheep-Game/blob/main/src/greedyplayer_drawback_a.gif)
### A* player
[A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) is a graph traversal and path search algorithm. Through A star, the algorithm will guide the agent to move towards the goal.  This agent extends all the functions from Greedy player but replacing the gather_closest_goal() function by A* path finding algorithm and decreasing the conservative level in wolf_close() function.

In addition, it also adds the following functions:
- getManhDistance() computes manhattan distance between two spots on the map.
- huntSheep() takes enemy sheep as the goal and finds out the path for my wolf.
- getObjbyPosition() takes input position and returns what figure stays on this position.
- catchableSheep() computes manhattan distance between my wolf position and enemy sheep position, if the distance is 1, my wolf is nearby the enemy sheep and return enemy sheep's position.
- trapableSheep()computes manhattan distance between my wolf and enemy sheep, my sheep and enemy sheep, my sheep and my wolf, and then returns the wolf action position. Basically, it tells you if my sheep and wolf are trapping the enemy sheep together.
```
SW   W   sS  s     s    Ss    WS    W
s   sS    W  SW   WS    W      s    Ss
```
- stuckableSheep() returns a FLAG that tells you if the enemy sheep is stuck by my wolf at the fence or the boundry of the map. In this case, my sheep might need to come over instantly and help my wolf to trap the enemy sheep together.
```
|-------    ## 
| s     |   #s
|  W    |     W          
```
- my_move_validation() checks if my move is valid or not, similar to valid_move() function.
- moveParser() outputs an action to move my agent from the current position to the next position.
- move_wolf() see pseudocode below
```
finalMove = MOVE_NONE
suggested_action_position = huntSheep()
if catchableSheep():
  finalMove = moveParser()
if trapableSheep():
  finalMove = moveParser()
if stuckableSheep() 
  finalMove = MOVE_NONE
if my_move_validation()
  return finalMove 
return MOVE_NONE
```
- getFoodsPosition() returns a list of available food and its ABS location and relatively location to my current figure position or another position. The returned list is ordered by relatively distance to me. By default the relative distance is referring w.r.t my sheep. This function also take consideration of the award level of food and its relative distance. For example, if my relative distance towards grass and rhubarb are 1 and 4, the function will select the rhubarb prior to grass. 
- checkSafeFromWolf_by_Manh() returns True value when the Manh Dist from the given spot to enemy wolf is lower than 2 otherwise retuns False value
- move_far_from_wolf() is similar to run_from_wolf() function but improving its robustness.
- sheepfencing() is designed for my sheep. Basically, it tells the sheep don't move and work as a fence when my wolf and sheep are trapping the enemy sheep together.
- getMoveSearchforSheep() provides move suggestion for my sheep. see pseudocode below:
```
if sheepfencing():
  suggestedAction
if stuckableSheep():
  suggestedAction
if food_present():
  getFoodsPosition()
  suggestedAction
else:
  print("block enemy sheep, when no food available")
  suggestedAction
```
- move_sheep() see pseudocode below:
```
finalMove = MOVE_NONE
suggestedAction = getMoveSearchforSheep()
if checkSafeFromWolf_by_Manh():
  finalMove = moveParser()
  return finalMove
else:
  finalMove = move_far_from_wolf()
  return finalMove
```

A visualization of A star path finding algorithm is shown below:
![](https://github.com/lineojcd/Multi-Agent-RL-for-the-Wolf-Sheep-Game/blob/main/src/Astart.png)
### Learning player
Unlike the previous algorithm, in this approach, one needs to learn the strategy from the past experience aka. training data.

The training data will be stored in .csv files. It was gathered from previous game experience. Each file is a game that is run, where the following data is gathered for each move:
- field_before: this is the field before the move was made.
- field_axer: this is the field axer the move was made.
- turn_made_by: which player made the move (e.g. 'player1 sheep').
- move_made: the actual move the agent made (e.g. -1).
- score1: the score of player 1 axer the move.
- score2: the score of player 2 axer the move.
- reason: on the final line of the file, the reason will be given for the termination of the game, if it was not the maximum number of iterations

Some sample data is shown below:
![](https://github.com/lineojcd/Multi-Agent-RL-for-the-Wolf-Sheep-Game/blob/main/src/raw_train_data.png)
One can approach the game as a classification problem: based on the provided training data (or the data you create yourself), you can train a classification model that uses the field as input and classifies which move it predicts the player should do. This is the high-level idea of learning strategy. Possible algorithms include: Naive Bayes, Decision Tree, Support Vector Machine, Neural Network etc. 

For each of these algorithms, you need to determine features of the game state that you use to classify the game state. For example, these feature can include how close a piece of grass is for a sheep-move, or where the sheep is for a wolf-move. You parse the field into a feature vector your algorithm can use as input.

### Deep Reinforcement Learning player
Obviously, the input matrix can be seen as an image and it is the **state** of the game if talking in the context of Reinforcement Learning.
**One can also design the Convolutional Neural Networks to extract features from input images and output the action or action probability distrbution for the agent to chose**. In this case, the CNN is actually approximating a policy function that map the states to the action probability distrbution. The diagram is as follows:
![](https://github.com/lineojcd/Multi-Agent-RL-for-the-Wolf-Sheep-Game/blob/main/src/DQN_state_action.png)

However, this fashion of end-to-end is really time consuming and hence required a huge computing resources. Due to the limited computing power, we preprocess the input data (a 15x19 matrix) into a 1-D vector with the following features as elements below. Compared with the fashion of end-to-end learning, this method sacrifices generalization ability but it is a practical way to deal with our case. One can design one or many Convolutional Neural Networks to process the input image and output one or many features. 

For example, we can design a convolutional neural network to extract the position of the target from the input image and this prediction accuracy will be 100% in this context. The other features can be also extracted similarly. The figure below illustrate this approach:
![](https://github.com/lineojcd/Multi-Agent-RL-for-the-Wolf-Sheep-Game/blob/main/src/cnn_extractor.png)

Again, due to the limited computing power and time constraints, we hand-crafted the features from the input image and hence reduced the state space from high-dimension to relatively low-dimension.

**For Sheep**:
- sheepfencing: Is my sheep blocking the enemy sheep as the fence?
- stuckableSheep: Is my sheep stucking the enemy sheep to assit my wolf?
- stayable: Is my sheep better staying at current spot?
- food_present: Is the food still available in the map?
- mypos_2_new_tar_has_way: Is there a way towards the target?
- mypos_up_2_new_tar_real_dist_smaller: Is it starting from my up grid to the target better?
- mypos_down_2_new_tar_real_dist_smaller: Is it starting from my down grid to the target better?
- mypos_left_2_new_tar_real_dist_smaller: Is it starting from my left grid to the target better?
- mypos_right_2_new_tar_real_dist_smaller: Is it starting from my right grid to the target better?
- new_tar_neighboring: Is the target neighboring?
- my_pos_up_walkable: Is my up grid walkable?
- my_pos_down_walkable: Is my down grid walkable?
- my_pos_left_walkable: Is my left grid walkable?
- my_pos_right_walkable: Is my right grid walkable?
- my_pos_stay_safeable: Is it safe to stay on current grid?
- runfromwolf: Does my sheep need to run from wolf?

All of the above features only have value 1 or 0. 1 means True and 0 means False. A sample feature vector looks like: [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]. In the context of RL, this can be called a **state**.
Given this input, the sample **action** taken might be -1.

**For Wolf**:
- stuckableSheep: Is my agent stucking the enemy sheep to wait for assitence
- stayable: Is my agent better staying at current spot?
- mypos_2_new_tar_has_way: Is there a way towards the target?
- mypos_up_2_new_tar_real_dist_smaller: Is it starting from my up grid to the target better?
- mypos_down_2_new_tar_real_dist_smaller: Is it starting from my down grid to the target better?
- mypos_left_2_new_tar_real_dist_smaller: Is it starting from my left grid to the target better?
- mypos_right_2_new_tar_real_dist_smaller: Is it starting from my right grid to the target better?
- my_pos_up_walkable: Is my up grid walkable?
- my_pos_down_walkable: Is my down grid walkable?
- my_pos_left_walkable: Is my left grid walkable?
- my_pos_right_walkable: Is my right grid walkable?

In the context of RL, a sample **state** for Wolf maybe look like [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1] and the **action** taken might be 0.


## Credits
This project uses the GUI environment from the DDIS group (led by Prof. Abraham Bernstein) of the University of Zurich.
