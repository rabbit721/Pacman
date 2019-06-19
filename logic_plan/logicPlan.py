# logicPlan.py
# ------------
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


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()

    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    return logic.conjoin([(A | B), ((~A) % ((~B) | C)), ((~A) | (~B) | C)])


def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    return logic.conjoin([(C % (B | D)),(A >> ((~B) & (~D))),(~(B & (~C)) >> A),((~D) >> C)])

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    wAzero = logic.PropSymbolExpr('WumpusAlive', 0)
    wAone = logic.PropSymbolExpr('WumpusAlive', 1)
    wB = logic.PropSymbolExpr('WumpusBorn', 0)
    wK = logic.PropSymbolExpr('WumpusKilled', 0)
    return logic.conjoin([(wAone % ((wAzero & (~wK)) | ((~wAzero) & wB))),
                          (~(wAzero & wB)),wB])


def modelToString(model):
    """Converts the model to a string for printing purposes. The keys of a model are
    sorted before converting the model to a string.

    model: Either a boolean False or a dictionary of Expr symbols (keys)
    and a corresponding assignment of True or False (values). This model is the output of
    a call to logic.pycoSAT.
    """
    if model == False:
        return "False"
    else:
        # Dictionary
        modelList = sorted(model.items(), key=lambda item: str(item[0]))
        return str(modelList)

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    if logic.is_valid_cnf(sentence):
        return logic.pycoSAT(sentence)
    cnf = logic.to_cnf(sentence)
    return logic.pycoSAT(cnf)

def atLeastOne(literals):
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print(logic.pl_true(atleast1,model1))
    False
    >>> model2 = {A:False, B:True}
    >>> print(logic.pl_true(atleast1,model2))
    True
    >>> model3 = {A:True, B:True}
    >>> print(logic.pl_true(atleast1,model2))
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)

def atMostOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form) that represents the logic that at most one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    ls = []
    if len(literals) == 1:
        return literals
    noneTrue = []
    for i in range(len(literals)):
        for j in range(i+1,len(literals)):
            ls.append(((~literals[i]) | (~literals[j])))
    return (logic.conjoin(ls))

def exactlyOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form)that represents the logic that exactly one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    ls = []
    if len(literals) == 1:
        return literals[0]

    for i in range(len(literals)):
        for j in range(i+1,len(literals)):
            ls.append(((~literals[i]) | (~literals[j])))
    ls.append(logic.disjoin(literals))
    return logic.conjoin(ls)

def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[2]":True, "P[3,4,0]":True, "P[3,3,0]":False, "West[0]":True, "GhostScary":True, "West[2]":False, "South[1]":True, "East[0]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print(plan)
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    final = dict()
    for k in model:
        str,idx = logic.parseExpr(k)
        if model[k] and str in actions:
            final.update({idx : str})
    res = []
    for key in sorted(final.keys()):
        res.append(final[key])
    return res


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    ls = [(-1,0), (1,0), (0,-1), (0,1)]
    dir = ["East", "West", "North", "South"]
    acts = []
    for i in range(4):
        (mx, my) = ls[i]
        #print("xfs, yf", (mx + x, my + y))
        if (not walls_grid[mx + x][my + y]) :
            at = logic.PropSymbolExpr(pacman_str, mx + x, my + y, t-1)
            mv = logic.PropSymbolExpr(dir[i], t-1)
            acts.append((at & mv));
    res = (logic.PropSymbolExpr(pacman_str, x, y, t) % logic.disjoin(acts))
    return res

def possActs(x, y, t, walls_grid, problem):
    ls = [(-1,0), (1,0), (0,-1), (0,1)]
    dir = ["East", "West", "North", "South"]
    acts = []
    for i in range(4):
        (mx, my) = ls[i]
        #print("xfs, yf", (mx + x, my + y))
        if (validIdx(mx + x, my + y, problem) and not walls_grid[mx + x][my + y]) :
            at = logic.PropSymbolExpr(pacman_str, mx + x, my + y, t-1)
            mv = logic.PropSymbolExpr(dir[i], t-1)
            acts.append((at & mv));
    return acts

def nxtState(act):
    #return the next position
    model = findModel(act)
    #print(model)
    for st in model:
        if model[st] and logic.parseExpr(st)[0] == 'P':
            return (logic.parseExpr(st)[1])
    return None

def validIdx (x, y, problem):
    return not ( x <= 0 or x > problem.getWidth() or y <=0 or y > problem.getHeight())
def precond(problem, T):
    ls = None
    walls = problem.walls
    pos = [(1,0), (-1,0), (0,1), (0,-1)];
    dir = ["East", "West", "North", "South"]
    width, height = problem.getWidth(), problem.getHeight()

    for t in range(T, T + 1):
        tmp = []
        for act in ['North', 'East', 'South', 'West']:
            tmp.append(logic.PropSymbolExpr(act, 50 - t))
        if tmp != []:
            if ls == None:
                ls = exactlyOne(tmp)
            else:
                ls = ls & logic.to_cnf(exactlyOne(tmp))

        tmp = []
        for i in range(1, width + 1):
            for j in range(1, height + 1):
                if not walls[i][j]:
                    tmp.append(logic.PropSymbolExpr(pacman_str, i, j, 50-t))

                for m in range(4):
                    (a,b) = pos[m]
                    d = dir[m]
                    if not validIdx(i + a, j + b, problem) or walls[i + a][j + b]:
                        ls = ls & ((~logic.PropSymbolExpr(pacman_str, i, j, 50-t))
                                   | (~logic.PropSymbolExpr(d, 50-t)))


        if tmp == []:
            continue
        if ls == None:
            ls = exactlyOne(tmp)
        else:
            ls = ls & exactlyOne(tmp)
    #print("ls", ls)
    return ls

def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are ['North', 'East', 'South', 'West']
    Note that STOP is not an available action.
    """
    walls = problem.walls
    w, h = problem.getWidth(), problem.getHeight()
    walls_list = walls.asList()
    x0, y0 = problem.startState
    xg, yg = problem.goal
    print("x0, y0", x0, y0)
    cond = None

    for max in range(1, 50):
        lg = logic.PropSymbolExpr(pacman_str, x0, y0, 50 - max) & logic.PropSymbolExpr(pacman_str, xg, yg, 50)

        if cond == None:
            cond = logic.to_cnf(precond(problem, max))
            lg = lg & cond
        else:
            cond = cond & logic.to_cnf(precond(problem, max))
            lg = logic.conjoin([lg, cond])
        #print(lg)

        print(max)

        for t in range(50 - max + 1, 51):
            for x in range(1, w + 1):
                for y in range(1, h + 1):
                    if(not walls[x][y]):
                        axiom = pacmanSuccessorStateAxioms(x, y, t, walls)
                        lg = lg & logic.to_cnf(axiom)
        res = findModel(lg)
        #print("res: ", res, "\n")

        if res != False:
            print("actions:", extractActionSequence(res, ['North', 'East', 'South', 'West']))
            return extractActionSequence(res, ['North', 'East', 'South', 'West'])
        #print(lg)

def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are ['North', 'East', 'South', 'West']
    Note that STOP is not an available action.

    P[X,Y,Z,t] Z:food number
    """

    walls = problem.walls
    w, h = problem.getWidth(), problem.getHeight()
    (x0, y0), food = problem.start
    foodList = food.asList()

    print("foodList", foodList)
    cond = None

    for max in range(1, 50):
        if (len(foodList) == 0):
            return []
        lg = logic.PropSymbolExpr(pacman_str, x0, y0, 50 - max)

        if cond == None:
            cond = logic.to_cnf(precond(problem, max))
            lg = lg & cond
        else:
            cond = cond & logic.to_cnf(precond(problem, max))
            lg = logic.conjoin([lg, cond])
        #print(lg)

        print(max)

        for t in range(50 - max + 1, 51):
            for x in range(1, w + 1):
                for y in range(1, h + 1):
                    if(not walls[x][y]):
                        axiom = pacmanSuccessorStateAxioms(x, y, t, walls)
                        lg = lg & logic.to_cnf(axiom)
        #print(lg)
        for f in foodList:
            tmp = []
            for t in range(50 - max, 50):
                tmp.append(logic.PropSymbolExpr(pacman_str, f[0], f[1], t))
            if len(tmp) != 0:
                lg = lg & atLeastOne(tmp)

        res = findModel(lg)
        #print("res: ", res, "\n")

        if res != False:
            print("actions:", extractActionSequence(res, ['North', 'East', 'South', 'West']))
            return extractActionSequence(res, ['North', 'East', 'South', 'West'])

# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Sometimes the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
