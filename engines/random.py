from __future__ import absolute_import
import random 

from engines import Engine

class RandomEngine(Engine):
    """ Game engine that plays completely randomly. """
    def get_move(self, board, color, move_num=None, 
		 time_remaining=None, time_opponent=None):
        """ Select a random move from the list of legal moves. """
        moves = board.get_legal_moves(color)
        return random.choice(moves)

engine = RandomEngine

