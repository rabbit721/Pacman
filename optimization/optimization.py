# optimization.py
# ---------------
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


import numpy as np
import itertools
import math

import pacmanPlot
import graphicsUtils
import util

# You may add any helper functions you would like here:
# def somethingUseful():
#     return True

def is_solv(a):
    return np.linalg.matrix_rank(a) == a.shape[0]


def lines(depth, cursor, dim, constraints, intersections, input, output):
    if(depth > dim and is_solv(np.array(input))):
        sol = tuple(np.linalg.solve(np.array(input), np.array(output)))
        #print(sol)
        intersections.append(sol)
        return
    for i in range(cursor, len(constraints)):
        ipt = list.copy(input);
        opt = list.copy(output);
        ipt.append(np.asarray(constraints[i][0]))
        opt.append(np.asarray(constraints[i][1]))
        #print("input: ", ipt)
        #print("output: ", opt)
        lines(depth + 1, i + 1, dim, constraints, intersections, ipt, opt);
    return


def findIntersections(constraints):
    """
    Given a list of linear inequality constraints, return a list of all
    intersection points.

    Input: A list of constraints. Each constraint has the form:
        ((a1, a2, ..., aN), b)
        where the N-dimensional point (x1, x2, ..., xN) is feasible
        if a1*x1 + a2*x2 + ... + aN*xN <= b for all constraints.
    Output: A list of N-dimensional points. Each point has the form:
        (x1, x2, ..., xN).
        If none of the constraint boundaries intersect with each other, return [].

    An intersection point is an N-dimensional point that satisfies the
    strict equality of N of the input constraints.
    This method must return the intersection points for all possible
    combinations of N constraints.

    """
    "*** YOUR CODE HERE ***"
    dim = len(constraints[0][0])
    intersections = []
    lines(1,0,dim,constraints,intersections,[],[])
    return intersections

def findFeasibleIntersections(constraints):
    """
    Given a list of linear inequality constraints, return a list all
    feasible intersection points.

    Input: A list of constraints. Each constraint has the form:
        ((a1, a2, ..., aN), b).
        where the N-dimensional point (x1, x2, ..., xN) is feasible
        if a1*x1 + a2*x2 + ... + aN*xN <= b for all constraints.

    Output: A list of N-dimensional points. Each point has the form:
        (x1, x2, ..., xN).

        If none of the lines intersect with each other, return [].
        If none of the intersections are feasible, return [].

    You will want to take advantage of your findIntersections function.

    """
    allIntersects = findIntersections(constraints)
    feasible = []
    for its in allIntersects:
        fs = True
        for cont in constraints:
            if np.dot(cont[0], its) > (cont[1] + 1e-12):
                fs = False
                break;
        if (fs):
            feasible.append(its)
    #print("feasible: ", feasible)
    return feasible

def solveLP(constraints, cost):
    """
    Given a list of linear inequality constraints and a cost vector,
    find a feasible point that minimizes the objective.

    Input: A list of constraints. Each constraint has the form:
        ((a1, a2, ..., aN), b).
        where the N-dimensional point (x1, x2, ..., xN) is feasible
        if a1*x1 + a2*x2 + ... + aN*xN <= b for all constraints.

        A tuple of cost coefficients: (c1, c2, ..., cN) where
        [c1, c2, ..., cN]^T is the cost vector that helps the
        objective function as cost^T*x.

    Output: A tuple of an N-dimensional optimal point and the
        corresponding objective value at that point.
        One N-demensional point (x1, x2, ..., xN) which yields
        minimum value for the objective function.

        Return None if there is no feasible solution.
        You may assume that if a solution exists, it will be bounded,
        i.e. not infinity.

    You can take advantage of your findFeasibleIntersections function.

    """
    fsIntersects = findFeasibleIntersections(constraints)
    minCost = 999999
    cVector = np.transpose(cost)
    minIntersect = None
    for its in fsIntersects:
        cost = np.dot(cVector,its)
        if cost < minCost:
            minCost = cost
            minIntersect = its

    if minIntersect == None:
        return None
    return (minIntersect, minCost)

def wordProblemLP():
    """
    Formulate the work problem in the write-up as a linear program.
    Use your implementation of solveLP to find the optimal point and
    objective function.

    Output: A tuple of optimal point and the corresponding objective
        value at that point.
        Specifically return:
            ((sunscreen_amount, tantrum_amount), maximal_utility)

        Return None if there is no feasible solution.
        You may assume that if a solution exists, it will be bounded,
        i.e. not infinity.

    """
    """
    at least 20 fluid ounces of suncreen and at least 15.5 fluid ounces of Tantrum.
    Pat's suitcase can fit 100 units of stuff.
    2 variables
    """
    "*** YOUR CODE HERE ***"
    consts = [((2.5,2.5),100.0),
              ((0.5,0.25),50.0),
              ((-1,0),-20.0),
              ((0,-1),-15.5)]
    cost = (-7, -4)
    (result, utility) = solveLP(consts, cost)
    print("result: ", result)
    print("maxutil: ", -utility)
    return (result, -utility)

def solveIP(constraints, cost):
    """
    Given a list of linear inequality constraints and a cost vector,
    use the branch and bound algorithm to find a feasible point with
    interger values that minimizes the objective.

    Input: A list of constraints. Each constraint has the form:
        ((a1, a2, ..., aN), b).
        where the N-dimensional point (x1, x2, ..., xN) is feasible
        if a1*x1 + a2*x2 + ... + aN*xN <= b for all constraints.

        A tuple of cost coefficients: (c1, c2, ..., cN) where
        [c1, c2, ..., cN]^T is the cost vector that helps the
        objective function as cost^T*x.

    Output: A tuple of an N-dimensional optimal point and the
        corresponding objective value at that point.
        One N-demensional point (x1, x2, ..., xN) which yields
        minimum value for the objective function.

        Return None if there is no feasible solution.
        You may assume that if a solution exists, it will be bounded,
        i.e. not infinity.

    You can take advantage of your solveLP function.

    """
    queue = util.Queue()
    bestIPRes, best = None, None
    queue.push(constraints)
    explored = []
    while(not queue.isEmpty()):
        currConst = queue.pop()

        res = solveLP(currConst, cost)
        #print(res)
        explored.append(currConst)

        if (res == None):
            continue

        (currRes, currBest) = res

        if (best != None and currBest > best):
            continue

        floor = [r for r in currRes]
        ceil = [r for r in currRes]
        intRes = True

        for i in range(len(currRes)):
            r = currRes[i]
            floor[i] = math.floor(r)
            ceil[i] = math.ceil(r)
            if (not np.isclose(floor[i], r, atol = 1e-12)
                and not np.isclose(ceil[i], r, atol = 1e-12)):
                intRes = False
        floor = tuple(floor)
        ceil = tuple(ceil)

        if(intRes):
            if(best == None or currBest < best):
                best = currBest
                bestIPRes = currRes
            continue


        for i in range(len(currRes)):
            tmp = [0 for x in range(len(currRes))]
            tmp[i] = 1
            ctsF = tuple(tmp)
            tmp[i] = -1
            ctsC = tuple(tmp)
            if(floor[i] == ceil[i]):
                continue
            leftConst = list.copy(currConst)
            rightConst = list.copy(currConst)

            if((ctsF, floor[i]) not in leftConst):
                leftConst.append((ctsF, floor[i]))
                queue.push(leftConst)

            if((ctsC, ceil[i]) not in rightConst):
                rightConst.append((ctsC, -ceil[i]))
                queue.push(rightConst)

    if (bestIPRes == None):
        return None
    return (bestIPRes, best)


def wordProblemIP():
    """
    Formulate the work problem in the write-up as a linear program.
    Use your implementation of solveIP to find the optimal point and
    objective function.

    Output: A tuple of optimal point and the corresponding objective
        value at that point.
        Specifically return:
        ((f_DtoG, f_DtoS, f_EtoG, f_EtoS, f_UtoG, f_UtoS), minimal_cost)

        Return None if there is no feasible solution.
        You may assume that if a solution exists, it will be bounded,
        i.e. not infinity.

    """
    consts = [((1.2,0,0,0,0,0),30),
              ((0,1.2,0,0,0,0),30),
              ((0,0,1.3,0,0,0),30),
              ((0,0,0,1.3,0,0),30),
              ((0,0,0,0,1.1,0),30),
              ((0,0,0,0,0,1.1),30),
              ((-1,0,-1,0,-1,0),-15),
              ((0,-1,0,-1,0,-1),-30),
              ((-1,0,0,0,0,0),0),
              ((0,-1,0,0,0,0),0),
              ((0,0,-1,0,0,0),0),
              ((0,0,0,-1,0,0),0),
              ((0,0,0,0,-1,0),0),
              ((0,0,0,0,0,-1),0)]
    cost = (12,20,4,5,2,1)
    res = solveIP(consts, cost)
    if(res == None):
        return None
    (result, utility) = res
    print("result: ", result)
    return (result, utility)


def foodDistribution(truck_limit, W, C, T):
    """
    Given M food providers and N communities, return the integer
    number of units that each provider should send to each community
    to satisfy the constraints and minimize transportation cost.

    Input:
        truck_limit: Scalar value representing the weight limit for each truck
        W: A tuple of M values representing the weight of food per unit for each
            provider, (w1, w2, ..., wM)
        C: A tuple of N values representing the minimal amount of food units each
            community needs, (c1, c2, ..., cN)
        T: A list of M tuples, where each tuple has N values, representing the
            transportation cost to move each unit of food from provider m to
            community n:
            [ (t1,1, t1,2, ..., t1,n, ..., t1N),
              (t2,1, t2,2, ..., t2,n, ..., t2N),
              ...
              (tm,1, tm,2, ..., tm,n, ..., tmN),
              ...
              (tM,1, tM,2, ..., tM,n, ..., tMN) ]

    Output: A list of M tuples, where each tuple has N values, representing the
            integer number of food units to move from provider m to community n:
            [ (f1,1, f1,2, ..., f1,n, ..., f1N),
              (f2,1, f2,2, ..., f2,n, ..., f2N),
              ...
              (fm,1, fm,2, ..., fm,n, ..., fmN),
              ...
              (fM,1, fM,2, ..., fM,n, ..., fMN) ]

        Return None if there is no feasible solution.
        You may assume that if a solution exists, it will be bounded,
        i.e. not infinity.

    You can take advantage of your solveIP function.

    """
    M = len(W)
    N = len(C)
    truckConst = []
    res = [() for x in range(len(C))]
    reordCost = np.transpose(T)
    for i in range(len(W)):
        tmp = [0 for x in range(len(W))]
        tmp[i] = W[i]
        truckConst.append((tuple(tmp), truck_limit))
    for i in range(len(C)):
        const = []
        tmp = [-1 for x in range(len(W))]
        minFood = ((tmp, -C[i]))
        const += truckConst
        const.append(minFood)
        for j in range(len(W)):
            tmp = [0 for x in range(len(W))]
            tmp[j] = -1
            const.append((tuple(tmp), 0))
        res[i] = solveIP(const, reordCost[i])
    final = [0 for x in range(len(W)*len(C))]
    total = 0
    for i in range(len(W)):
        for j in range(len(C)):
            #print(res[j][0][i])
            #print(i*len(C)+j)
            final[i*len(C)+j] = res[j][0][i]
        total+= res[i][1]
    return (tuple(final),total)
    return res




if __name__ == "__main__":
    constraints = [((3, 2), 10),((1, -9), 8),((-3, 2), 40),((-3, -1), 20)]
    inter = findIntersections(constraints)
    print(inter)
    print()
    valid = findFeasibleIntersections(constraints)
    print(valid)
    print()
    print(solveLP(constraints, (3,5)))
    print()
    print(solveIP(constraints, (3,5)))
    print()
    print(wordProblemIP())
