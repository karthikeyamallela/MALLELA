# AI MINIPROJECT
## Siddharth Agarwal 
### Single player AI based game of Chess using minimax and alpha-beta pruning

---------------------

[![AIChess Game Screenshot](http://img.youtube.com/vi/B0Nvw8D6xk8/0.jpg)](https://www.youtube.com/watch?v=B0Nvw8D6xk8 "AI Chess Project - Minmax with Alpha-Beta Pruning")

Introduction
This mini project is an GUI based AI powered single player game of chess written in python using pygame(cross-platform set of python modules designed for writing video games/ https://www.pygame.org/ ). The basic search engine comprises of alpha-beta pruning. This is to decrease the number of nodes generate and evaluated by minimax algorithm. The depth of search ahead steps is set to 3 under board configuration in board.py.
Initial planning flowchart of how the game should work.
   
    Dependencies 1. Pygame
Alpha-beta pruning Worst case performance: (b^d) Best case performance: (b^d/2)
The minimax algorithm chooses the best move out of the possible moves from the search tree. Our search ahead depth for future steps is set to 3. For depths more than 3 we need a better search engine and heuristic as the number of possibilities will increase and thus take exponentially more time. The algorithm allows us to filter out the nodes which are not the best option without even traversing the tree. This is done by keeping track of two values called alpha and beta as you are searching through the tree.
Alpha is our maximum lower bound (lowest score acceptable)
  
Beta is our minimum upper bound (highest score acceptable to opponent)
Heuristics Applied
For solving this problem, I have used 3 core heuristics for the evaluation function.
These are Fruit values. Fruit uses a 16x12 vector attack board representation which is essentially a square centric board representation.
The attack value or the safety rating of a piece controlling a square might be considered as inversely proportional to its point value. The more valuable a piece becomes in the game, the lower it’s safety rating becomes. Each piece also has a certain position rating or mobility rating which is the determined by the depth of the search tree. These 3 evaluation functions make up the final evaluation function and this value is then used to compare and perform moves.
Evaluation Function used
       Fruit point values
  
   Pawn
      Knight
      Bishop
      Rook
      Queen
    100
   400
   400
   600
   1200
     Safety Rating/attack values
    Pawn
   Knight
   Bishop
   Rook
   Queen
    50
      150
      150
      300
      450
  Using point values blindly can lead to bad play and bad AI decisions.
The 3 heuristics together form an evaluation function where the value of each piece is updates as a move is made. It is given by the sum of material value, piece squared value and mobility value.
How to install
pip install –user pygame python main.py
Scope of improvement
1. Better evaluation function and more accurate values
2. Useatrainedconvolutionalnetasanevaluationfunctiontoevaluatefuture
states from the search tree
3. Add pawn promotion
4. Add castling
5. Add en passant
6. Going to more depth for better search results
Reference:
http://web.cs.ucla.edu/~rosen/161/notes/alphabeta.html
    
https://github.com/Open-Source-Project-Collaboration/board-game-playing-ai
https://github.com/devinalvaro/yachess
https://www.chessprogramming.org/Neural_MoveMap_Heuristic
https://www.chessprogramming.org/Move_Ordering#Using_Neural_Networks
https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
https://www.pygame.org/wiki/GettingStarted
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
https://www.chessprogramming.org/Point_Value https://www.chessprogramming.org/Material https://www.chess.com/learn-how-to-play-chess https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha- beta-pruning/
https://www.chessprogramming.org/Mobility https://www.chessprogramming.org/Engines#F https://github.com/hwuebben/Chess https://github.com/itay121/Chess_AI
                 
