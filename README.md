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

* Wolves cannot step on squares occupied by the opponent’s wolf (wolves block each other).

* Wolves cannot step on squares occupied by the sheep of the same player.

* Sheep cannot step on squares occupied by the wolf of the same player.

* Sheep cannot step on squares occupied by the opposite sheep.

* Neither the sheep nor the wolf can enter a square with a fence on.

* Neither the sheep nor the wolf can step on a square outside the map. Imagine the map is surrounded by fences.

* If the sheep steps on a food object the food object is consumed (removed from the map) and a score is awarded.

* If the wolf steps on a food object the food object gets removed but no score is awarded.
