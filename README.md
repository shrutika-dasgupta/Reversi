Course: CS4701 - Artificial Intelligence
Assignment No. :2
------------------------------------------
Name	: Shrutika Dasgupta

Aim 	: To optimize the game of Othello using Minimax Algorithm with Alpha-Beta Prunning. 
-----------------------------------------------------------------------
For the purpose of implementing the Minimax Algorithm for the program to fair well against an opponent in the gam of 
Othello the follow functions have been implemented and they are run with the following heuristics to improve the chances 
of my agent to win against the random agent.

**The functions in the file**
-------------------------------------------
1) get_move
	--> This functions calls the various function in the tree so that it can construct the minimax tree.
	--> Also to make it work faster and more effectively, we are implementing the call to the function so that depth is 
		passed as the parameter and depending
		on how much time is remaning for the user to finish the game and make a move, the depth various is varied between '2 and 3'
	--> the game is run in two modes that is alpabeta mode and minimax mode

2) minimax
	--> This method like naturally applies the minimaxtree implementation of the booard state.
	-->this method makes a call to the min_gameply() min value for the opporent player to minimze its chance to choose from random.

3) min_gameplay
	--> This method checks if the depth is reached to zero
	--> this method also calls the max_gameplay() when a turn is missed as the opponent has no places to move.
	--> If the depth is zero it calcultes the heuristic of that leaf board in the minimax tree.
	--> The depth is not reached then the function in turn calls the max_gameplay()

4) max_gameplay
	--> This method checks if the depth is reached to zero
	--> this method also calls the min_gameplay() when a turn is missed as the opponent has no places to move.
	--> If the depth is zero it calcultes the heuristic of that leaf board in the minimax tree.
	--> The depth is not reached then the function in turn calls the min_gameplay()

5) alpha_beta_minimax
	--> This method applies that Alpha-Beta prunning tool to the Minimax Tree, to element branches that need not be 
	included and thus preventing them from exploring the nodes that are not promising.

6) alpha_beta_minplay
	--> Works same as "min_gameplay()" with Alpha-Beta Prunning

7) alpha_beta_maxplay
	--> Works same as "max_gameplay()" with Alpha-Beta Prunning

8) winner
	--> Checks if the color has won or not

9) calculate_heuristics
	--> This method is called from the following methods for the respective conditions mentioned below:
		1. min_gameplay when the depth is 0
		2. max_gameplay when the depth is 0
		3. alpha_beta_minplay when the depth is 0
		4. alpha_beta_maxplay when the depth is 0
	--> This funtions calls the following functions to generate the heuristics:
		1. calc_mobility_heurictics
		2. calc_corner_edge_heuristics
		3. calc_stability_heuristics
		4. calc_coin_parity_heuristics

10) calc_mobility_heurictics
	--> This heuristic takes into consideration 2 main types of mobilities:
		1. Actual_mobility: 
			This is heuristic calculates the the difference between the available legal moves for the player and 
			the opponent for that particular board state.
		2. Potetial_mobility:
			This is the heuristic value that determines the number of potential moves that open up around one 
			legal move for the player, that means the number of opponent coins around a legal move empty space for the player. 

11) calc_corner_edge_heuristics
	--> This heuristics calcultes the number of edges that are occupied by the player and its opponent.
	--> The way this is works is by assigning positive weighted to the corners of the board that are [(0,0),(7,7),(0,7),(7,0)] 
		and negative weightage to the board pieces that are potentially harmful for the player when the corner is yet to be captured. 
		These peices are [(1,0),(0,1),(1,1),(1,7),(0,6),(1,6),(7,1),(6,0),(6,1),(6,7),(7,6),(6,6)]
	--> So when the player captures these harmful pieces before he can capture before the corners, the score of the player decreases, 
		but for the opponent doing the same thing, proves beneficial for the player.
	--> It also provides the heuristics for the corner 4 triangles. So that maximum heuristic value can be obtained:
		1. (7,0)(7,1)(7,2)(6,0)(6,1)(5,0)
		2. (2,0)(1,0)(1,1)(0,0)(0,1)(0,2)
		3. (7,5)(7,6)(7,7)(6,6)(6,7)(5,7)
		4. (2,7)(1,6)(1,7)(0,5)(0,6)(0,7)

12) calc_stability_heuristics
	--> The stability heuristic determines how many pieces on the board for the player are flippable as compared to the pieces for the opponent.
	--> This determines the degree of stability.

13) calc_coin_parity_heuristics:
	--> This heuristic determines that number of coins on the board for a particular state for the player in comparison to the opponent.

14) display:
	--> displayes that state of the board.

15) save_board_state:
	--> Saves the hash of the board state when the depth is 0 for keeping a tab leaf nodes in the tree that have already been visited.


**The Various Research Papers refered for this purpose are:**
-----------------------------------------------------------------

1) Sannidhanam, V., & Annamalai, M. (n.d.). An Analysis of Heuristics in Othello.
2) Korf, E. (1994). Minimax Search: Othello Results, 1365–1370.
3) Buro, M. (2002). Improving heuristic mini-max search by supervised learning, 134, 85–99.
4) http://www.giocc.com/concise-implementation-of-minimax-through-higher-order-functions.html#show-last-Point
5) Roy, A., Supervisor, S., & Schalk, A. (n.d.). Final Project Report - Othello Master.
6) Rosenbloom, P. S. (1981). A world-championship-level Othello program.
