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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        score = successorGameState.getScore()

        distanceGhost = float('Inf')
        for ghost in newGhostStates:
            g = util.manhattanDistance(newPos, ghost.getPosition())
            if g < distanceGhost:
                distanceGhost = g

        if distanceGhost < 2:
            return float('-Inf')

        distanceFood = float('Inf')
        for food in newFood.asList():
            f = util.manhattanDistance(newPos, food)
            if f < distanceFood:
                distanceFood = f

        score += distanceGhost/distanceFood

        return score

        "util.raiseNotDefined()"


def scoreEvaluationFunction(currentGameState):
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
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            v = float('-Inf')
            for action in gameState.getLegalActions(0):
                v = max(v, minValue(gameState.generateSuccessor(0, action), depth, 1))

            return v

        def minValue(gameState, depth, numAgents):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            v = float('Inf')
            for action in gameState.getLegalActions(numAgents):
                if numAgents == gameState.getNumAgents() - 1:
                    v = min(v, maxValue(gameState.generateSuccessor(numAgents, action), depth - 1))
                else:
                    v = min(v, minValue(gameState.generateSuccessor(numAgents, action), depth, numAgents + 1))

            return v

        def minimaxDecision(gameState):
            maxV = float('-Inf')
            for action in gameState.getLegalActions(0):
                v = minValue(gameState.generateSuccessor(0, action), self.depth, 1)
                if v > maxV:
                    maxV = v
                    move = action

            return move

        return minimaxDecision(gameState)

    "util.raiseNotDefined()"

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), ""

            v = (float('-Inf'), "")
            for action in gameState.getLegalActions(0):
                vMove = minValue(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)

                if vMove[0] > v[0]:
                    v = (vMove[0], action)

                if v[0] > beta:
                    return v
                alpha = max(v[0], alpha)

            return v

        def minValue(gameState, depth, numAgents, alpha, beta):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), ""

            v = (float('Inf'), "")
            for action in gameState.getLegalActions(numAgents):
                if numAgents == gameState.getNumAgents() - 1:
                    vMove = maxValue(gameState.generateSuccessor(numAgents, action), depth + 1, alpha, beta)
                else:
                    vMove = minValue(gameState.generateSuccessor(numAgents, action), depth, numAgents + 1, alpha, beta)

                if vMove[0] < v[0]:
                    v = (vMove[0], action)

                if v[0] < alpha:
                    return v
                beta = min(v[0], beta)

            return v

        result = maxValue(gameState, 0, float('-Inf'), float('Inf'))

        return result[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def maxvalue(gameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            v = float('-Inf')
            for action in gameState.getLegalActions(0):
                v = max(v, expectedValue(gameState.generateSuccessor(0, action), depth, 1))
            return v

        def expectedValue(gameState, depth, numAgents):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            v = 0
            for action in gameState.getLegalActions(numAgents):
                if numAgents == gameState.getNumAgents() - 1:
                    v += maxvalue(gameState.generateSuccessor(numAgents, action), depth - 1)/len(gameState.getLegalActions(numAgents))
                else:
                    v += expectedValue(gameState.generateSuccessor(numAgents, action), depth, numAgents + 1)/len(gameState.getLegalActions(numAgents))

            return v

        def expectiMax(gameState):
            maxV = float('-Inf')
            for action in gameState.getLegalActions(0):
                v = expectedValue(gameState.generateSuccessor(0, action), self.depth, 1)
                if v > maxV:
                    maxV = v
                    move = action

            return move

        return expectiMax(gameState)

        "util.raiseNotDefined()"


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation util.raiseNotDefined() function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"

    distanceGhost = float('Inf')
    for ghost in newGhostStates:
        g = util.manhattanDistance(newPos, ghost.getPosition())
        if g < distanceGhost:
            distanceGhost = g

    distanceFood = float('Inf')
    for food in newFood.asList():
        f = util.manhattanDistance(newPos, food)
        if f < distanceFood:
            distanceFood = f

    if newScaredTimes == 0:
        return currentGameState.getScore() + distanceGhost / distanceFood
    else:
        return currentGameState.getScore() + distanceGhost / distanceFood + sum(newScaredTimes)

    "util.raiseNotDefined()"

# Abbreviation
better = betterEvaluationFunction

