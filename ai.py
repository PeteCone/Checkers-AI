from lib import abstractstrategy, boardlibrary
import math


class AlphaBetaSearch:
    
    def __init__(self, strategy, maxplayer, minplayer, maxplies=3, 
                 verbose=False):
        """"alphabeta_search - Initialize a class capable of alphabeta search
        problem - problem representation
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the uitlity function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        self.strategy = strategy
        self.maxplies = maxplies
        self.maxplayer = maxplayer
        self.minplayer = minplayer

    def alphabeta(self, state):
        """
        Conduct an alpha beta pruning search from state
        :param state: Instance of the game representation
        :return: best action for maxplayer
        """
        return self.maxvalue(state=state, alpha=math.inf * -1, beta=math.inf, ply=0)[1]

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)
        """
        return state.is_terminal()[0] or ply == self.maxplies

    def maxvalue(self, state, alpha, beta, ply):
        """
        maxvalue - - alpha/beta search from a maximum node
        Find the best possible move knowing that the next move will try to
        minimize utility.
        :param state: current state
        :param alpha: lower bound of best move max player can make
        :param beta: upper bound of best move max player can make
        :param ply: current search depth
        :return: (value, maxaction)
        """
        # If the board is terminal or if the search has gone deep enough (recorded by ply) then return
        # the utility of that board. Otherwise we iterate through all possible actions for maxplayer
        # and compare their estimated utilities as given from minvalue. We return the largest utility
        # and the action associated with it. Alpha and beta track the max and min pruning in their search
        # and breaks out of the searching for loop to reduce unnecessary computation
        if self.cutoff(state=state, ply=ply):
            max_action = None
            utility = self.strategy.evaluate(state=state)
        else:
            max_action = state.get_actions(self.maxplayer)[0]
            utility = math.inf * -1
            for a in state.get_actions(self.maxplayer):
                temp = max(utility, self.minvalue(state=state.move(move=a), alpha=alpha, beta=beta, ply=ply+1)[0])
                if temp > utility:
                    utility = temp
                    max_action = a
                alpha = max(alpha, utility)
                if beta <= alpha:
                    break
        return utility, max_action

    def minvalue(self, state, alpha, beta, ply):
        """
        minvalue - alpha/beta search from a minimum node
        :param state: current state
        :param alpha:  lower bound on best move for min player
        :param beta:  upper bound on best move for max player
        :param ply: current depth
        :return: (v, minaction)  Value of min action and the action that
           produced it.
        """

        #Same function as maxvalue,
        if self.cutoff(state, ply):
            min_action = None
            utility = self.strategy.evaluate(state=state)
        else:
            min_action = state.get_actions(self.minplayer)[0]
            utility = math.inf
            for a in state.get_actions(self.minplayer):
                temp = min(utility, self.maxvalue(state.move(move=a), alpha=alpha, beta=beta, ply=ply+1)[0])
                if temp < utility:
                    utility = temp
                    min_action = a
                beta = min(beta,utility)
                if beta <= alpha:
                    break
        return utility, min_action

class Strategy(abstractstrategy.Strategy):
    """Your strategy, maybe you can beat Tamara Tansykkuzhina, 
       2019 World Women's Champion
    """

    def __init__(self, *args):
        """
        Strategy - Concrete implementation of abstractstrategy.Strategy
        See abstractstrategy.Strategy for parameters
       """

        super(Strategy, self).__init__(*args)
        
        self.search = \
            AlphaBetaSearch(self, self.maxplayer, self.minplayer,
                                   maxplies=self.maxplies, verbose=False)
     
    def play(self, board):
        """
        play(board) - Find best move on current board for the maxplayer
        Returns (newboard, action)
        """
        action = AlphaBetaSearch.alphabeta(self.search, state=board)
        newboard = board.move(action)
        return newboard, action
    
    def evaluate(self, state, turn = None):
        """
        evaluate - Determine utility of terminal state or estimated
        utility of a non-terminal state
        :param state: Game state
        :param turn: Optional turn (None to omit)
        :return:  utility or utility estimate based on strengh of board
                  (bigger numbers for max player, smaller numbers for
                   min player)
        """
        # Utility is determined by the number of pawns and kings on the board for each player.
        # Maxplayer pawns/kings increase the utility, Minplayer decreases the utility.
        score = state.get_pawnsN()[state.playeridx(self.maxplayer)] - \
            state.get_pawnsN()[state.playeridx(self.minplayer)]
        score += state.get_kingsN()[state.playeridx(self.maxplayer)] - \
            state.get_kingsN()[state.playeridx(self.minplayer)]

        return score
        

# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards["StrategyTest1"]
    redstrat = Strategy('r', b, 6)
    blackstrat = Strategy('b', b, 6)

    nb = b
    print(b)
    (nb, action) = redstrat.play(nb)
    print("Red would select ", action)
    print(nb)

    b = (nb, action)[0]
    
    (nb, action) = blackstrat.play(b)
    print("Black would select ", action)
    print(nb)
    
 

