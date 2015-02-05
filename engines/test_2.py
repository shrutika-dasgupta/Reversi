from engines import Engine
from copy import deepcopy

class StudentEngine(Engine):
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """

    Max_Score = 1000

    def __init__(self):
        self.alpha_beta = False

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Return a move for the given color that maximizes the difference in 
        number of pieces for that color. """
        # Get a list of all legal moves.
        

        return self.minimax(board, 3, color)

        # Return the best move according to our simple utility function:h
        # which move yields the largest different in number of pieces for the
        # given color vs. the opponent?
	   #return max(moves, key=lambda move: self._get_cost(board, color, move))

    def _get_cost(self, board, color, move):
        """ Return the difference in number of pieces after the given move 
        is executed. """
        
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board
        num_pieces_op = len(newboard.get_squares(color))
        num_pieces_me = len(newboard.get_squares(color))

        # Return the difference in number of pieces
        return num_pieces_me - num_pieces_op

    def minimax(self, board, depth, color):
        moves = board.get_legal_moves(color)
        best_move = moves[0]
        best_score = -self.Max_Score
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.min_play(newboard, depth-1, color)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def min_play(self, board, depth, color):
        if depth == 0:
            return
        moves = board.get_legal_moves(-color)
        best_score = self.Max_Score
        for move in moves:
            newboard = deepcopy(board) 
            newboard.execute_move(move,-color)
            score = self.max_play(newboard, depth-1, color)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self, board, depth, color):
        if depth == 0:
            return
        moves = board.get_legal_moves(color)
        best_score = -self.Max_Score
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.min_play(newboard, depth-1,color)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score
engine = StudentEngine

