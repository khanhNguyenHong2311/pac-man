# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):

        def minimax(state, high, char):
            if high  == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if char == 0:
                return maximize(state, high)
            return minimize(state, high, char)




        def maximize(state, high):
            bestVal = float('-inf')
            bestAction = None

            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                val = minimax(successor, high , 1)

                if val > bestVal:
                    bestVal = val
                    bestAction = action

            
            if high== 0:
                return bestAction

            return bestVal





        def minimize(state, high, char):
            bestVal = float('inf')

            for action in state.getLegalActions(char):
                successor = state.generateSuccessor(char, action)

                nextChar = char + 1
                nextHigh = high

                if nextChar == state.getNumAgents():
                    nextChar = 0
                    nextHigh += 1

                val = minimax(successor, nextHigh, nextChar)
                bestVal = min(bestVal, val)

            return bestVal


        return maximize(gameState, 0)

        util.raiseNotDefined()
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        

        def minimax(state, char, high, a, b):

            
            if high == self.depth  or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            
            if char == 0:
                return maximize(state, char, high, a, b)
            else:
                return minimize(state, char, high, a, b)




        def maximize(state, char, high, a, b):
            bestVal = float('-inf')
            bestAction = None

            actions = state.getLegalActions(char)

            for action in actions:
                next_state = state.generateSuccessor(char, action)

                val = minimax(next_state, char + 1, high, a,  b)

                if val > bestVal:
                    bestVal = val
                    bestAction= action

                
                if bestVal > b:
                    return bestVal

                a = max(a, bestVal)

            #root cần action
            if high == 0:
                return bestAction

            return bestVal


        def minimize(state, char, high, a, b):
            bestVal = float('inf')

            actions = state.getLegalActions(char)

            for action in actions:
                nextState = state.generateSuccessor(char, action)

            
                nextChar = char+ 1
                nextHigh = high

                if char == state.getNumAgents() - 1:
                    nextChar = 0
                    nextHigh = high + 1

                val = minimax(nextState, nextChar, nextHigh, a, b)

                if val < bestVal:
                    bestVal = val

                
                if bestVal < a:
                    return bestVal

                b = min(b, bestVal)

            return bestVal


       
        return maximize(gameState, 0, 0, float('-inf'), float('inf'))
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        

        def expectimax(state, high, char):

            if high == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            
            if char == 0:
                return maximize(state, high)

            return expectValue(state, high, char)





        def maximize(state, high):

            bestVal = float('-inf')

            for action in state.getLegalActions(0):

                successor = state.generateSuccessor(0, action)

                val = expectimax(successor, high, 1)

                if val > bestVal:
                    bestVal = val

            return bestVal





        def expectValue(state, high, char):

            actions = state.getLegalActions(char)

            if len(actions) == 0:
                return self.evaluationFunction(state)

            total = 0

            for action in actions:

                successor = state.generateSuccessor(char, action)

                nextChar = char + 1
                nextHigh = high

                if nextChar == state.getNumAgents():
                    nextChar = 0
                    nextHigh += 1

                val = expectimax(successor, nextHigh, nextChar)

                total += val

            return total / len(actions)





        bestVal = float('-inf')
        bestAction = None

        for action in gameState.getLegalActions(0):

            successor = gameState.generateSuccessor(0, action)

            val = expectimax(successor, 0, 1)

            if val > bestVal:
                bestVal = val
                bestAction = action


        return bestAction

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
