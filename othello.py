import argparse, copy, signal, sys, timeit, imp
from board import Board, move_string, print_moves

player = {-1 : "Black", 1 : "White"}

def game(white_engine, black_engine, game_time=300.0, verbose=False):
    """ Run a single game. Raise RuntimeError in the event of time expiration.
    Raise LookupError in the case of a bad move. The tournament engine must
    handle these exceptions. """

    # Initialize variables
    board = Board()
    time = { -1 : game_time, 1 : game_time }
    engine = { -1 : black_engine, 1 : white_engine }

    if verbose:
        print "INITIAL BOARD\n--\n"
        board.display(time)
    
    # Do rounds
    for move_num in range(60):
        moves = []
        for color in [-1, 1]:
            start_time = timeit.default_timer()
            move = get_move(board, engine[color], color, move_num, time)
            end_time = timeit.default_timer()
            # Update user time
            time[color] -= round(end_time - start_time, 1) 
            
            if time[color] < 0:
                raise RuntimeError(color)

            # Make a move, otherwise pass
            if move is not None:
                board.execute_move(move, color)
                moves.append(move)

                if verbose:
                    print "--\n"
                    print "Round " + str(move_num + 1) + ": " + player[color] + " plays in " + move_string(move) + '\n'
                    board.display(time)

        if not moves:
            # No more legal moves. Game is over.
            break

    print "FINAL BOARD\n--\n"
    board.display(time)

    return board

def winner(board):
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
            

def get_move(board, engine, color, move_num, time, **kwargs):
    """ Get the move for the given engine and color. Check validity of the 
    move. """
    legal_moves = board.get_legal_moves(color)

    if not legal_moves:
        return None
    elif len(legal_moves) == 1:
        return legal_moves[0]
    else:
	try:
            move = engine.get_move(copy.deepcopy(board), color, move_num, time[color], time[-color])
	except:
	    raise SystemError(color)

        if move not in legal_moves:
            raise LookupError(color)

        return move

def signal_handler(signal, frame):
    """ Capture SIGINT command. """
    print '\n\n- You quit the game!'
    sys.exit()  

result = (0, 0, 0)

def main(white_engine, black_engine, game_time, verbose):
    try:
    	board = game(white_engine, black_engine, game_time, verbose)
    	stats = winner(board)
    	bscore = str(stats[1])
    	wscore = str(stats[2])

    	if stats[0] == -1:
            print "- " + player[-1] + " wins the game! (" + bscore + "-" + wscore + ")"
	    return (-1, int(bscore), int(wscore))
    	elif stats[0] == 1:
            print "- " + player[1] + " wins the game! (" + wscore + "-" + bscore + ")"
            return (1, int(bscore), int(wscore))
	else:
            print "- " + player[-1] + " and " + player[1] + " are tied! (" + bscore + "-" + wscore + ")"
            return (0, int(bscore), int(wscore))

    except RuntimeError, e:
        if e[0] == -1:
            print "\n- " + player[-1] + " ran out of time!"
            print player[1] + " wins the game! (64-0)"
	    return (1, 0, 64)
        else:
            print "\n- " + player[1] + " ran out of time!"
            print player[-1] + " wins the game! (64-0)"
	    return (-1, 64, 0)

    except LookupError, e:
        if e[0] == -1:
            print "\n- " + player[-1] + " made an illegal move!"
            print player[1] + " wins the game! (64-0)"
	    return (1, 0, 64)
        else:
            print "\n- " + player[1] + " made an illegal move!"
            print player[-1] + " wins the game! (64-0)"
	    return (-1, 64, 0)
	
    except SystemError, e:
	if e[0] == -1:
            print "\n- " + player[-1] + " ended prematurely because of an error!"
            print player[1] + " wins the game! (64-0)"
            return (1, 0, 64)
        else:
            print "\n- " + player[1] + " ended prematurely because of an error!"
            print player[-1] + " wins the game! (64-0)"
            return (-1, 64, 0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    # Automatically generate help and usage messages. 
    # Issue errors when users gives the program invalid arguments.
    parser = argparse.ArgumentParser(description="Play the Othello game with different engines.")
    parser.add_argument("black_engine", type=str, nargs=1, help="black engine (human, oneply, random, student)")
    parser.add_argument("white_engine", type=str, nargs=1, help="white engine (human, oneply, random, student)")
    parser.add_argument("-aB", action="store_true", help="turn on alpha-beta pruning for the black player")
    parser.add_argument("-aW", action="store_true", help="turn on alpha-beta pruning for the white player")
    parser.add_argument("-t", type=int, action="store", help="adjust time limit", default=30)
    parser.add_argument("-v", action="store_true", help="display the board on each turn") 
    args = parser.parse_args();

    black_engine = args.black_engine[0]
    white_engine = args.white_engine[0]
    # Retrieve player names
    player[-1] = black_engine + " (black)"
    player[1] = white_engine + " (white)"

    try:
        engines_b = __import__('engines.' + black_engine)
        engines_w = __import__('engines.' + white_engine)
	engine_b = engines_b.__dict__[black_engine].__dict__['engine']()
        engine_w = engines_w.__dict__[white_engine].__dict__['engine']()
        
	if (args.aB and black_engine != "greedy" and black_engine != "human" and black_engine != "random"):
	    engine_b.alpha_beta = True
	if (args.aW and white_engine != "greedy" and white_engine != "human" and white_engine != "random"):
            engine_w.alpha_beta = True
	v = (args.v or white_engine == "human" or black_engine == "human")
        # Play game
	print player[-1] + " vs. " + player[1] + "\n"
        main(engine_w, engine_b, game_time=args.t, verbose=v)

    except ImportError, e:
        print 'Unknown engine -- ' + e[0].split()[-1]
        sys.exit()
