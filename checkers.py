'''
@author: Peter Conant and Isabella Messina
We the undersigned promise that we have in good faith attempted to follow the principles of
pair programming. Although we were free to discuss ideas with others, the implementation is
our own. We have shared a common workspace and taken turns at the keyboard for the majority
of the work that we are submitting. Furthermore, any non programming portions of the assignment
were done independently. We recognize that should this not be the case, we will be subject
to penalties as outlined in the course syllabus.
'''

# Game representation and mechanics

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.
import statistics


# Python can load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
if True:
    import imp
    import sys
    major = sys.version_info[0]
    minor = sys.version_info[1]
    modpath = "lib/__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
    tonto = imp.load_compiled("tonto", modpath)


# human - human player, prompts for input    
from lib import human, checkerboard
import ai

from lib.timer import Timer


def Game(red=human.Strategy, black=tonto.Strategy,
         maxplies=6, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 

    Returns winning player 'r' or 'b'
    """

    current_board = checkerboard.CheckerBoard() # Initialize our board
    redplayer = red('r', current_board, maxplies) # Initilize our red & black player
    blackplayer = black('b', current_board, maxplies)

    print("Initial Board: ", current_board)

    # Main while loop: this loop commands each player to take a turn. Terminates loop when the end of the game
    # (a board that is in terminal state) is triggered
    while not current_board.is_terminal()[0]:
        # Red ply
        board_action = redplayer.play(current_board)
        current_board = board_action[0]  # Update current board
        # Print for readability
        print("redplayer: ", current_board.get_action_str(board_action[1]))
        print(current_board)
        # After red's turn check if game is over
        if current_board.is_terminal()[0]:  # Check if board is terminal after each ply
            break
        # Black ply
        board_action = blackplayer.play(current_board)
        current_board = board_action[0]  # Update current board
        # Print for readability
        print("blackplayer: ", current_board.get_action_str(board_action[1]))
        print(current_board)

    if current_board.is_terminal()[1] is None:
        print("Game ended in a draw.")
    else:
        print(current_board.is_terminal()[1], " WINS")  # Print the winner of the game


if __name__ == "__main__":
    # Examples
    # Starting from specific board with default strategy
    #Game(init=boardlibrary.boards["multihop"])
    #Game(init=boardlibrary.boards["StrategyTest1"])
    #Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)

    # Tonto vs Tonto
    Game(red=ai.Strategy, black=tonto.Strategy)

    #Play with default strategies...
    #Game()
        
        
        

        
                    
            
        

    
    
