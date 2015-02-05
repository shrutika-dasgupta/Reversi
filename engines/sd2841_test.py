from engines import Engine
from copy import deepcopy
import math
import time

class StudentEngine(Engine):
    
    MAXIMUM_SCORE = 10000

    POSITION_SCORES = [[25, 0, 6, 5, 5, 6, 0, 25],
                       [ 0, 0, 1, 1, 1, 1, 0,  0],
                       [ 6, 1, 4, 3, 3, 4, 1,  6],
                       [ 5, 1, 3, 2, 2, 3, 1,  5],
                       [ 5, 1, 3, 2, 2, 3, 1,  5],
                       [ 6, 1, 4, 3, 3, 4, 1,  6],
                       [ 0, 0, 1, 1, 1, 1, 0,  0],
                       [25, 0, 6, 5, 5, 6, 0, 25]]

    TIME_PROPORTIONS = [1, 1, 1.5, 2, 2, 3, 3, 7, 9, 11, 11, 11, 12, 15, 15, 15, 15, 15, 15, 15, 15, 12, 10, 8, 7, 6, 5, 4, 3, 2]

    BRANCHING_FACTORS = [3, 4, 4, 5, 6, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 9, 8, 8, 7, 7, 7, 6, 5, 5, 5, 5, 5]

    def __init__(self):
        self.alpha_beta = False
        self.known_boards = dict()

    # Return a move for the given color that maximizes the difference in number of pieces for that color.
    def get_move(self, board, color, move_num=None, time_remaining=None, time_opponent=None):
        if (self.alpha_beta == False):   
            return self.minimax(board, color, move_num, time_remaining, time_opponent)
        else:   
            return self.alphabeta(board, color, move_num, time_remaining, time_opponent)

    def minimax(self, board, max_color, move_num, time_remaining, time_opponent):
        # print(move_num)
        # record initial time; estimate time for each play and target cumulative time left
        if move_num == 0:
            self.initial_time_remaining = time_remaining
            proportions_sum = sum(StudentEngine.TIME_PROPORTIONS)
            self.time_per_turn = map(lambda porportion: (time_remaining)*float(porportion)/proportions_sum, StudentEngine.TIME_PROPORTIONS)

            self.cumulative_time_left = [0]*30
            for i in xrange(1, len(self.time_per_turn)):
                self.cumulative_time_left[-i-1] = self.cumulative_time_left[-i] + self.time_per_turn[-i-1]
            self.nodes_visited = 0
            self.nodes_per_sec = 0
        elif (move_num % 6) == 0:
            self.nodes_per_sec = self.nodes_visited / (self.initial_time_remaining - time_remaining)

        self.target_time = 1000     
        
        if move_num < 6 or self.nodes_per_sec < 0:
            self.minimax_depth = 4
        elif move_num < 30:
            # Compute how many nodes this play should explore
            self.current_diff_from_planned = time_remaining - self.cumulative_time_left[move_num]
            self.target_time = self.current_diff_from_planned + self.time_per_turn[move_num]
            target_node_count = self.nodes_per_sec * self.target_time

            if self.target_time < 0:
                self.target_time = 1000
                self.minimax_depth = 2
            else:
                b = StudentEngine.BRANCHING_FACTORS[move_num]
                self.minimax_depth = int(math.log(target_node_count*(b-1) + 1, b) - 1)
                if self.minimax_depth < 4:
                    self.minimax_depth = 4

            # print("Diff from cumulative planned: " + str(self.current_diff_from_planned))
            # print("Planned time for this turn:" + str(self.time_per_turn[move_num]))
            # print("Time for this turn:" + str(self.target_time))
            # print("Nodes per sec:" + str(self.nodes_per_sec))
            # print("Depth chosen:" + str(self.minimax_depth))
        else:
            if time_remaining < 2:
                self.minimax_depth = 3            
            else:
                self.minimax_depth = 4

        # First loop is done here to keep track of the best move (not only the score)
        moves = board.get_legal_moves(max_color)

        max_score = -StudentEngine.MAXIMUM_SCORE
        best_move = None
        newboard = deepcopy(board)
        start_time = time.time()
        for i in xrange(len(moves)):
            newboard.execute_move(moves[i], max_color)    
            score = self.minimax_min(newboard, max_color, self.minimax_depth-1)
            self.copy_board_state(board, newboard, moves[i])
            if score >= max_score:
                max_score = score
                best_move = moves[i]
            # emergency if running out of time
            if self.minimax_depth >= 4 and (time.time() - start_time) > self.target_time:
                self.minimax_depth -= 2

        return best_move

    def minimax_min(self, board, max_color, levels_deep_left):
        self.nodes_visited += 1

        state = self.state_to_i(board, max_color)
        if state in self.known_boards:
            return self.known_boards[state]

        if levels_deep_left == 0:
            return self.heuristic(board, max_color)

        moves = board.get_legal_moves(-max_color)
        if len(moves) == 0:
            return self.minimax_max(board, max_color, levels_deep_left-1)

        min_score = StudentEngine.MAXIMUM_SCORE
        newboard = deepcopy(board)
        for i in xrange(len(moves)):
            newboard.execute_move(moves[i], -max_color)    
            score = self.minimax_max(newboard, max_color, levels_deep_left-1)
            self.copy_board_state(board, newboard, moves[i])
            if score < min_score:
                min_score = score

        self.known_boards[state] = min_score
        return min_score
        
    def minimax_max(self, board, max_color, levels_deep_left):
        self.nodes_visited += 1

        state = self.state_to_i(board, max_color)
        if state in self.known_boards:
            return self.known_boards[state]

        if levels_deep_left == 0:
            return self.heuristic(board, max_color)

        moves = board.get_legal_moves(max_color)
        if len(moves) == 0:
            return self.minimax_min(board, max_color, levels_deep_left-1)

        max_score = -StudentEngine.MAXIMUM_SCORE
        newboard = deepcopy(board)
        for i in xrange(len(moves)):
            newboard.execute_move(moves[i], max_color)    
            score = self.minimax_min(newboard, max_color, levels_deep_left-1)
            self.copy_board_state(board, newboard, moves[i])
            if score > max_score:
                max_score = score

        self.known_boards[state] = max_score
        return max_score

    def alphabeta(self, board, max_color, move_num, time_remaining, time_opponent):
        #print(move_num)
        # record initial time; estimate time for each play and target cumulative time left
        if move_num == 0:
            self.initial_time_remaining = time_remaining
            proportions_sum = sum(StudentEngine.TIME_PROPORTIONS)
            self.time_per_turn = map(lambda porportion: (time_remaining)*float(porportion)/proportions_sum, StudentEngine.TIME_PROPORTIONS)

            self.cumulative_time_left = [0]*30
            for i in xrange(1, len(self.time_per_turn)):
                self.cumulative_time_left[-i-1] = self.cumulative_time_left[-i] + self.time_per_turn[-i-1]
            self.nodes_visited = 0
            self.nodes_per_sec = 0
        elif (move_num % 6) == 0:
            self.nodes_per_sec = self.nodes_visited / (self.initial_time_remaining - time_remaining)

        self.target_time = 1000     
        
        if move_num < 6 or self.nodes_per_sec < 0:
            self.minimax_depth = 4
        elif move_num < 30:
            # Compute how many nodes this play should explore
            self.current_diff_from_planned = time_remaining - self.cumulative_time_left[move_num]
            self.target_time = self.current_diff_from_planned + self.time_per_turn[move_num]
            target_node_count = self.nodes_per_sec * self.target_time

            if self.target_time < 0:
                self.target_time = 1000
                self.minimax_depth = 2
            else:
                b = StudentEngine.BRANCHING_FACTORS[move_num]
                self.minimax_depth = int(math.log(target_node_count*(b-1) + 1, b) - 1)
                if self.minimax_depth < 4:
                    self.minimax_depth = 4
            # print("Diff from cumulative planned: " + str(self.current_diff_from_planned))
            # print("Planned time for this turn:" + str(self.time_per_turn[move_num]))
            # print("Time for this turn:" + str(self.target_time))
            # print("Nodes per sec:" + str(self.nodes_per_sec))
            # print("Depth chosen:" + str(self.minimax_depth))
        else:
            if time_remaining < 2:
                self.minimax_depth = 3            
            else:
                self.minimax_depth = 4

        # First loop is done here to keep track of the best move (not only the score)
        moves = board.get_legal_moves(max_color)
        self.order_moves(moves)

        best_move = None
        newboard = deepcopy(board)
        alpha = -StudentEngine.MAXIMUM_SCORE
        beta = StudentEngine.MAXIMUM_SCORE
        start_time = time.time()
        for i in xrange(len(moves)):
            newboard.execute_move(moves[i], max_color)    
            score = self.alphabeta_min(newboard, max_color, self.minimax_depth-1, alpha, beta)
            self.copy_board_state(board, newboard, moves[i])
            if score > alpha:
                alpha = score
                best_move = moves[i]
            # emergency if running out of time
            if self.minimax_depth >= 4 and (time.time() - start_time) > (self.target_time - .5):
                self.minimax_depth -= 2
            elif self.target_time > 10 and i > 3 and self.minimax_depth >= 4 and (time.time() - start_time) > (self.target_time*(float(i) / len(moves))):
                self.minimax_depth -= 2
            elif i > 5 and i == StudentEngine.BRANCHING_FACTORS[move_num] and self.minimax_depth >= 4:
                self.minimax_depth -= 2

        return best_move

    def alphabeta_min(self, board, max_color, levels_deep_left, alpha, beta):
        self.nodes_visited += 1
        
        if levels_deep_left == 0:
            return self.heuristic(board, max_color)

        moves = board.get_legal_moves(-max_color)
        if len(moves) == 0:
            return self.alphabeta_max(board, max_color, levels_deep_left-1, alpha, beta)

        self.order_moves(moves)
        newboard = deepcopy(board)
        for i in xrange(len(moves)):
            newboard.execute_move(moves[i], -max_color)    
            score = self.alphabeta_max(newboard, max_color, levels_deep_left-1, alpha, beta)
            self.copy_board_state(board, newboard, moves[i])
            if score < alpha:
                return score
            if score < beta:
                beta = score

        return beta
        
    def alphabeta_max(self, board, max_color, levels_deep_left, alpha, beta):
        self.nodes_visited += 1

        if levels_deep_left == 0:
            return self.heuristic(board, max_color)

        moves = board.get_legal_moves(max_color)
        if len(moves) == 0:
            return self.alphabeta_min(board, max_color, levels_deep_left-1, alpha, beta)

        self.order_moves(moves)
        newboard = deepcopy(board)
        for i in xrange(len(moves)):
            newboard.execute_move(moves[i], max_color)    
            score = self.alphabeta_min(newboard, max_color, levels_deep_left-1, alpha, beta)
            self.copy_board_state(board, newboard, moves[i])
            if score > beta:
                return score
            if score > alpha:
                alpha = score

        return alpha
    
    def state_to_i(self, board, color):
        return color * hash(tuple(tuple(x) for x in board))

    def heuristic(self, board, color):
        score = 0
        for i in range(8):
            for j in range(8):
                score += board[i][j] * StudentEngine.POSITION_SCORES[i][j]

        for i in range(8):
            row_pieces = [board[i][0]]
            col_pieces = [board[0][i]]
            for j in range(1,8):
                if row_pieces[-1] * board[i][j] > 0:
                    row_pieces[-1] += board[i][j]
                else:
                    row_pieces.append(board[i][j])
                
                if col_pieces[-1] * board[j][i] > 0:
                    col_pieces[-1] += board[j][i]
                else:
                    col_pieces.append(board[j][i])

            if len(row_pieces) >= 3:
                for j in range(1, len(row_pieces)-1):
                    if row_pieces[j] != 0:
                        if row_pieces[j-1] * row_pieces[j+1] == 0 and row_pieces[j-1] + row_pieces[j+1] != 0:
                            score -= row_pieces[j] * 1

            if len(col_pieces) >= 3:
                for j in range(1, len(col_pieces)-1):
                    if col_pieces[j] != 0:
                        if col_pieces[j-1] * col_pieces[j+1] == 0 and col_pieces[j-1] + col_pieces[j+1] != 0:
                            score -= col_pieces[j] * 1

        if board[0][0] == 0:
            score -= (board[1][0] + board[0][1] + board[1][1])*3
        if board[0][7] == 0:
            score -= (board[1][7] + board[0][6] + board[1][6])*3
        if board[7][0] == 0:
            score -= (board[7][1] + board[6][0] + board[6][1])*3
        if board[7][7] == 0:
            score -= (board[6][7] + board[7][6] + board[6][6])*3

        return (score * color)# + 2*(len(board.get_legal_moves(color)) - len(board.get_legal_moves(-color)))

    def copy_board_state(self, from_board, to_board, move):
        move_line = move[0]
        move_col = move[1]

        for i in range(8):
            if i == move_line:
                for j in range(8):
                    to_board[i][j] = from_board[i][j]
            else:
                aux = move_line - i
                col = move_col - aux
                if col > 0 and col < 7:
                    to_board[i][col] = from_board[i][col]
                to_board[i][move_col] = from_board[i][move_col]
                col = move_col + aux
                if col > 0 and col < 7:
                    to_board[i][col] = from_board[i][col]

    def order_moves(self, moves):
        moves.sort(key=lambda move: StudentEngine.POSITION_SCORES[move[0]][move[1]])


engine = StudentEngine
