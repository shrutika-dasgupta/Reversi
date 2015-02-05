from engines import Engine
from copy import deepcopy
from board import moves_string, print_moves, move_string
import math


class StudentEngine(Engine):
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """

    MAX_SCORE = 10000

    def __init__(self):
        self.alpha_beta = False
        self.all_boards_states = dict()

    def get_move(self, board, color, move_num=None, time_remaining=None, time_opponent=None):
        """ Return a move for the given color that maximizes the difference in 
        number of pieces for that color. """
        #print "in GET-MOVE"
        # print "time-opponent: "+str(time_opponent)+" for: "+str(-1*color)+"\n"
        if self.alpha_beta == False:
            return self.minimax(board, color)
        else:
            return self.alpha_beta_minimax(board, color)
        
    def minimax(self, board, color):
        #print "in MINIMAX"
        all_moves = board.get_legal_moves(color)
        best_move = all_moves[0]
        heur_score = -StudentEngine.MAX_SCORE
        depth = 2

        for move in all_moves:
            newboard = deepcopy(board)
            newboard.execute_move(move, color)

            score = self.min_gameplay(newboard, color, depth-1)
            if score > heur_score:
                best_move = move
                heur_score = score

        return best_move


    def min_gameplay(self, board, color, depth):
        #print "In MIN_GAME"

        state_of_board = self.save_board_state(board, color)
        #print "In MIN_GAME"
        if state_of_board in self.all_boards_states:
            return self.all_boards_states[state_of_board]

        if depth == 0:
            return self.calculate_heuristics(board, color, depth)

        #stat = self.winner(board)
        #if stat[0] == color:
        #    return self.evaluate_board(board, color)
        #print "DEPTH=> "+str(depth)+" color => "+str(color)+"\n"
        all_moves = board.get_legal_moves(-color)

        if len(all_moves) == 0:
            return self.max_gameplay(board, color, depth-1)

        heur_score = StudentEngine.MAX_SCORE #positive
        
        
        for move in all_moves:
            newboard = deepcopy(board)
            newboard.execute_move(move, -color)
            score = self.max_gameplay(newboard, color, depth-1)
            if score < heur_score:
                best_move = move
                heur_score = score

        self.all_boards_states[state_of_board] = heur_score
        
        return heur_score

    def max_gameplay(self, board, color, depth):

        if depth == 0:
            return self.calculate_heuristics(board, color, depth)

        state_of_board = self.save_board_state(board, color)

        if state_of_board in self.all_boards_states:
            return self.all_boards_states[state_of_board]

        # stat = self.winner(board)
        # if stat[0] == color:
        #     return self.evaluate_board(board, color)
        all_moves = board.get_legal_moves(color)

        if len(all_moves) == 0:
            return self.min_gameplay(board, color, depth-1)

        heur_score = -StudentEngine.MAX_SCORE #negative
        

        for move in all_moves:
            newboard = deepcopy(board)
            newboard.execute_move(move, color)
            score = self.min_gameplay(newboard, color, depth-1)
            if score > heur_score:
                best_move = move
                heur_score = score
        
        self.all_boards_states[state_of_board] = heur_score

        return heur_score

    def alpha_beta_minimax(self, board, color):

        depth = 2

        all_moves = board.get_legal_moves(color)
        best_move = None
        
        alpha = -StudentEngine.MAX_SCORE
        beta = StudentEngine.MAX_SCORE

        for move in all_moves:
            newboard_ab = deepcopy(board)
            newboard_ab.execute_move(move, color)
            score = self.alpha_beta_minplay(newboard_ab, color, depth-1, alpha, beta)
            if score > alpha:
                alpha = score
                best_move = move

        return best_move

    def alpha_beta_minplay(self, board, color, depth, alpha, beta):
        if depth == 0:
            return self.calculate_heuristics(board, color, depth)

        all_moves = board.get_legal_moves(-color)
        if len(all_moves) == 0:
            return self.alpha_beta_maxplay(board, color, depth-1, alpha, beta)

        
        for move in all_moves:
            newboard_ab = deepcopy(board)
            newboard_ab.execute_move(newboard_ab, -color)
            score = self.alpha_beta_maxplay(newboard_ab, color, depth-1, alpha, beta)
            if score < alpha:
                return score
            if score < beta:
                beta = score
        return beta

    def alpha_beta_maxplay(self, board, color, depth, alpha, beta):
        if depth == 0:
            return self.calculate_heuristics(board, color, depth)

        all_moves = board.get_legal_moves(color)
        if len(all_moves) == 0:
            return self.alpha_beta_minplay(board, color, depth-1, alpha, beta)

        
        for move in all_moves:
            newboard_ab = deepcopy(board)
            newboard_ab.execute_move(newboard_ab, color)
            score = self.alpha_beta_minplay(newboard_ab, color, depth-1, alpha, beta)
            if score > beta:
                return score
            if score > alpha:
                alpha = score

        return alpha

    def evaluate_board(self, board, color):
        stat = self.winner(board)
        if stat[0] == color:
            return float('inf')
        else:
            return float('-inf')

    def winner(self, board):
        """ Determine the winner of a given board. Return the points of the two 
        players. """
        black_count = board.count(-1)
        white_count = board.count(1)
        if black_count > white_count:
            return (-1, black_count, white_count)
        elif white_count > black_count:
            return (1, black_count, white_count)
        else:
            return (0, black_count, white_count)

    def calculate_heuristics(self, board, color, depth):

        #print "IN calculate_heuristics"
        #calculating the heuristics based on the following 4 components:
        #1) mobility
        #2) stability
        #3) corners
        #4) coin parity
        
        #for mobility
        max_player_moves = board.get_legal_moves(color)
        
        #print_moves(max_player_moves)
        # print "init-board: \n"
        # self.display(board)
        max_player_mobility = len(max_player_moves)
        #print "len: max_mob: "+str(max_player_mobility)
        
        min_player_mobility = float('inf')
        num_min_player_moves = 0

        for move in max_player_moves:

            newboard_mob = deepcopy(board)
            newboard_mob.execute_move(move, color)
            
            min_player_moves = newboard_mob.get_legal_moves(-color)
            # print "Min-player-moves"
            # print_moves(min_player_moves)

            num_min_player_moves = len(min_player_moves)

            if(num_min_player_moves < min_player_mobility):
                min_player_mobility = num_min_player_moves

        # print "Min-Player_mob: "+str(min_player_mobility)
        # print "MAX-Player_mob: "+str(max_player_mobility)

        if(max_player_mobility + min_player_mobility != 0):
            actual_mobility = 10000*( max_player_mobility - min_player_mobility )/( max_player_mobility + min_player_mobility )
        else:
            actual_mobility = 0


        #corners captured

        newboard_corner = deepcopy(board)
        all_corners = [(0,0),(7,7), (0,7), (7,0)]
        potential_corners = [(0,2),(2,0),(5,0),(0,5),(5,7),(7,5),(2,7),(7,2)]
        tobe_potential_corners = [(5,5),(5,2),(2,5),(2,2)]
        unlikely_corners = [(6,1),(6,6),(1,1),(1,6),(1,7),(7,1),(0,6),(6,0),(6,7),(7,6),(1,0),(0,1)]
        max_corner_count = 0
        min_corner_count = 0
        max_potential_corners = 0
        min_potential_corners = 0
        max_tobe_potential_corners = 0
        min_tobe_potential_corners = 0

        min_unlikely_corners = 0
        max_unlikely_corners = 0

        cood_max_squares = newboard_corner.get_squares(color)
        cood_min_squares = newboard_corner.get_squares(-color)

        # print "min: "
        # print cood_min_squares
        # print "max: "
        # print cood_max_squares

        for cord_max in cood_max_squares:
            if cord_max in all_corners:   
                max_corner_count +=3
            if cord_max in potential_corners:
                max_potential_corners += 2
            if cord_max in tobe_potential_corners:
                max_tobe_potential_corners +=1

        for cord_min in cood_min_squares:
            if cord_min in all_corners:
                min_corner_count +=3
            if cord_min in potential_corners:
                min_potential_corners += 2
            if cord_min in tobe_potential_corners:
                min_tobe_potential_corners +=1

        total_max_corners = max_corner_count + max_potential_corners + max_tobe_potential_corners
        total_min_corners = min_corner_count + min_potential_corners + min_tobe_potential_corners

        # if (max_corner_count > 0):
        #     print "max: "+str(max_corner_count )

        # if(min_corner_count > 0):
        #     print "min: "+str(min_corner_count)

        # print "max-corners"+str(max_corner_count)
        # print "min-corners"+str(min_corner_count)
        
        if(total_max_corners + total_min_corners != 0):
            corner_heuristic = 10000*(( total_max_corners - total_max_corners )/( total_min_corners + total_max_corners ))
        else:
            corner_heuristic = 0

        #print "actual_mobility: "+str(actual_mobility)

        if(corner_heuristic != 0):
            return (actual_mobility + corner_heuristic)/2
        else: 
            return actual_mobility

    def save_board_state(self, board, color):
       # print "In SAVE"
        
        hash_board = hash(tuple(tuple(piece) for piece in board))
        #print hash_board
        return hash_board * color

engine = StudentEngine
