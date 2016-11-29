# 2048_AI_Solver
A simple AI solver for the game 2048 written in Python

## The Game
The puzzle game 2048 is a fun and addicting game involving the combination of instances of the same number to form 2048.
The original game can be found here: https://gabrielecirulli.github.io/2048/

## Search Algorithm
The file PlayerAI.py contains the main logic for the AI solver.
The AI uses a minimax algorithm with alpha-beta pruning. The default search depth is 4 layers.

## Heuristics
For heuristics, two are currently used, this part can still be improved greatly.
#### Snake Score
The first heuristic uses a snake score. That is the number in the corner is assigned the biggest weight.
The weighting descends as it moves along each cell in a snake-like manner.
A bonus score is awarded if the highest value cell is in the corner.
The total sum of (cellValue*weight) is the snakeScore.
#### Empty Tile Score
Another heuristic is an empty tiles heuristic. The system awards higher points to board states with more empty cells.
#### Gradient Score (not used)
The gradient score is similar to the snake score, but instead of weighting based on a snake-like manner, weighting is
determined strictly by the distance from the corner.
In practice, this heuristic performed a lot worse than the snake score.
I have kept the code here as it has room for improvement.
#### Total Score
The total score is the sum of the snake score and empty tile score.

## HOW TO RUN
To run, type the command:
$ python GameManager.py
