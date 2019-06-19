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

    def manhattan(self, pacman, dot):
        "The Manhattan distance heuristic for a PositionSearchProblem"
        px, py = pacman
        dx, dy = dot
        return abs(px - dx) + abs(py - dy)

    def foodHeuristic(self, newPos, foodGrid):
        height = foodGrid.height
        width = foodGrid.width
        sum = 0
        m = 99999
        d = 0
        list = foodGrid.asList()
        if len(list) > 0:
            #print("food: ", list[0])
            #print("dist: ", self.manhattan(newPos, list[0]))
            return self.manhattan(newPos, list[0])
        return 0


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
        print(" ")
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currFood = currentGameState.getFood()
        currPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        for ghost in newGhostStates:
            gPos = ghost.configuration.getPosition()
            #print("ghostPos:", ghost.configuration.getPosition())
            if(self.manhattan(gPos, newPos) <= 1):
               return -1
            elif(self.manhattan(gPos, currPos) == 1
                 and action != Directions.STOP):
               return 1000
        if(action == Directions.STOP):
            return -1
        x,y = newPos

        if (currFood[x][y]):
            return 1000
        h = self.foodHeuristic(newPos, currFood)
        return (100 - h)

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
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

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
    Your minimax agent (question 7)
    """
    def DFS(self, state, depth):
        pActions = state.getLegalActions(0)
        #print("pActions: ", pActions)
        maxi = -999999
        maxAct = None
        for act in pActions:
            nextState = state.generateSuccessor(0, act)
            result = self.dfs(nextState, 1, nextState.getNumAgents(), depth)
            #print("result: ", result, "at depth: ", depth)
            if (maxi < result):
                maxi = result
                maxAct = act
        if(maxi == -999999):
            return self.evaluationFunction(state)
        if(depth == 1):
            return maxAct
        else:
            return maxi
    def dfs(self, state, num, agentNum, depth):
        #print("dfs:  depth: ", depth)
        #print("agentNum ", agentNum, "; num: ", num)
        gActions = state.getLegalActions(num)
        #print("gActions: ", gActions)
        m = 999999
        for gAct in gActions:
            gState = state.generateSuccessor(num, gAct)
            #print("act: ", gAct, "of num ", num, "at depth ", depth)
            if (num == agentNum - 1):
                if (depth == self.depth):
                    m = min(m, self.evaluationFunction(gState))
                    #print("returning from eval1, m:", m)
                else:
                    #print("going into DFS with depth", depth + 1)
                    m = min(m, self.DFS(gState, depth + 1))
            else :
                m = min(m, self.dfs(gState, num + 1, agentNum, depth))
        if (m == 999999):
            eval = self.evaluationFunction(state)
            #print("returning from eval2, eval: ", eval)
            return eval
        return m

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

        #print(self.depth)
        return self.DFS(gameState, 1)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 8)
    """
    def DFS(self, state, depth):
        pActions = state.getLegalActions(0)
        #print("pActions: ", pActions)
        maxi = -999999
        maxAct = None
        for act in pActions:
            nextState = state.generateSuccessor(0, act)
            result = self.dfs(nextState, 1, nextState.getNumAgents(), depth)
            #print("result: ", result, "at depth: ", depth)
            if (maxi < result):
                maxi = result
                maxAct = act
        if(maxi == -999999):
            return self.evaluationFunction(state)
        if(depth == 1):
            return maxAct
        else:
            return maxi

    def dfs(self, state, num, agentNum, depth):
        #print("dfs:  depth: ", depth)
        #print("agentNum ", agentNum, "; num: ", num)
        gActions = state.getLegalActions(num)
        #print("gActions: ", gActions)
        #m = 999999
        sum = 0
        for gAct in gActions:
            gState = state.generateSuccessor(num, gAct)
            #print("act: ", gAct, "of num ", num, "at depth ", depth)
            if (num == agentNum - 1):
                if (depth == self.depth):
                    #m = min(m, self.evaluationFunction(gState))
                    sum += self.evaluationFunction(gState)
                    #print("returning from eval1, m:", m)
                else:
                    #print("going into DFS with depth", depth + 1)
                    #m = min(m, self.DFS(gState, depth + 1))
                    sum += self.DFS(gState, depth + 1)
            else :
                #m = min(m, self.dfs(gState, num + 1, agentNum, depth))
                sum += self.dfs(gState, num + 1, agentNum, depth)
        if (sum == 0):
            eval = self.evaluationFunction(state)
            #print("returning from eval2, eval: ", eval)
            return eval
        return float(sum)/float(len(gActions))

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.DFS(gameState, 1)

def manhattan(pacman, dot):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    px, py = pacman
    dx, dy = dot
    return abs(px - dx) + abs(py - dy)

def foodHeuristic(newPos, foodGrid, capsules, score):
    height = foodGrid.height
    width = foodGrid.width
    sum = 0
    m = 99999
    d = 0
    list = foodGrid.asList()
    #print(capsules)
    if len(list) > 0:
        #print("food: ", list[0])
        #print("currPos: ", newPos)
        #print("dist: ", manhattan(newPos, list[0]))
        return manhattan(newPos, list[0])
    return 0

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 9).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currFood = currentGameState.getFood()
    currPos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    currGhostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    currScaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]
    #print(currScaredTimes)
    sum = 0
    #if(currPos == (3,3)):
        #print("at capsule (3,3)!!!", "if capsule", (3,3) in capsules)
    for g in range(len(currGhostStates)):
        if(currScaredTimes[g] > 0):
            sum += manhattan(currGhostStates[g].configuration.getPosition(), currPos)

    if(sum != 0):
        return (1000 - sum - 10*len(currFood.asList()))* 5
        + score + random.randint(1,5) - 10000*numCap
    for ghost in currGhostStates:
        gPos = ghost.configuration.getPosition()
        #print("ghostPos:", ghost.configuration.getPosition())
        if(manhattan(gPos, currPos) <= 1):
           return -1000000
    x,y = currPos
    numCap = len(capsules)
    h = foodHeuristic(currPos, currFood, capsules, score)
    return (1000 - h - 10*len(currFood.asList()))* 5 + score + random.randint(1,7) - 10000*numCap

# Abbreviation
better = betterEvaluationFunction
