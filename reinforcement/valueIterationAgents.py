# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()

        for i in range(self.iterations):
            prevVal = self.values.copy()
            for s in states:
                maxval = -99999
                for act in self.mdp.getPossibleActions(s):
                    trans = self.mdp.getTransitionStatesAndProbs(s, act)
                    sum = 0
                    for (nxt, prob) in trans:
                        sum += prob * ((self.mdp.getReward(s, act, nxt))
                                       + self.discount * prevVal[nxt])

                    maxval = max(sum, maxval)
                if(maxval == -99999):
                    continue
                self.values.update({s: maxval})
                #print("s: ", s, "; maxval: ", maxval)



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        sum = 0
        trans = self.mdp.getTransitionStatesAndProbs(state, action)
        for (nxt, prob) in trans:
            sum += prob * (self.discount*self.values[nxt]
                           + self.mdp.getReward(state, action, nxt))
        return sum

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if (self.mdp.isTerminal(state)):
            return None
        actions = self.mdp.getPossibleActions(state)
        best = None
        max = -99999
        for act in actions:
            val = self.computeQValueFromValues(state, act)
            if max < val:
                best = act
                max = val
        return best

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        states = self.mdp.getStates()
        print(states)
        ct = 0
        while(ct < self.iterations):
            for s in states:
                if(ct >= self.iterations):
                    break
                ct += 1
                if (self.mdp.isTerminal(s)):
                    continue
                maxval = -99999
                for act in self.mdp.getPossibleActions(s):
                    trans = self.mdp.getTransitionStatesAndProbs(s, act)
                    sum = 0
                    for (nxt, prob) in trans:
                        sum += prob * ((self.mdp.getReward(s, act, nxt))
                                       + self.discount * self.values[nxt])

                    maxval = max(sum, maxval)

                if(maxval == -99999):
                    continue
                self.values.update({s: maxval})

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def predecessor(self, state):
        res = []
        for s in self.mdp.getStates():
            for a in self.mdp.getPossibleActions(s):
                for (nxt, prob) in self.mdp.getTransitionStatesAndProbs(s, a):
                    if nxt == state:
                        res.append(s)
        return res

    def update(self, state):
        maxval = -99999
        for act in self.mdp.getPossibleActions(state):
            trans = self.mdp.getTransitionStatesAndProbs(state, act)
            sum = 0
            for (nxt, prob) in trans:
                sum += prob * ((self.mdp.getReward(state, act, nxt))
                               + self.discount * self.values[nxt])

            maxval = max(sum, maxval)
        if(maxval == -99999):
            return
        self.values.update({state: maxval})

    def runValueIteration(self):
        states = self.mdp.getStates()
        pq = util.PriorityQueue()
        pred = dict()
        for st in states:
            pred.update({st: self.predecessor(st)})
        for s in states:
            if(self.mdp.isTerminal(s)):
                continue
            m = -999999
            for act in self.mdp.getPossibleActions(s):
                m = max(m, self.computeQValueFromValues(s, act))
            if m == -999999:
                continue
            pq.push(s, -abs(m-self.values[s]))
        for i in range(self.iterations):
            if (pq.isEmpty()):
                break
            curr = pq.pop()
            self.update(curr)
            for p in pred[curr]:
                m = -999999
                for act in self.mdp.getPossibleActions(p):
                    m = max(m, self.computeQValueFromValues(p, act))
                if m == -999999:
                    continue
                if abs(self.values[p] - m) > self.theta:
                    pq.update(p, -abs(self.values[p] - m))
