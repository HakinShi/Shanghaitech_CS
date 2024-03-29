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
        for i in range(self.iterations):
            newvalue = util.Counter()
            for state in self.mdp.getStates():
                if len(self.mdp.getPossibleActions(state)) == 0:
                    newvalue[state] = 0
                    continue

                q = util.Counter()

                for action in self.mdp.getPossibleActions(state):
                    q[action] = self.computeQValueFromValues(state, action)
                maxi = -1e10
                for prob in q:
                    if q[prob] > maxi:
                        maxi = q[prob]
                newvalue[state] = maxi
            #newvalue {'TERMINAL_STATE': 0, (0, 0): -10.0, (0, 1): -10.0, (0, 2): -10.0, (0, 3): -10.0, (0, 4): -10.0,
            #(1, 0): 2.9289102300077094}
            self.values = newvalue

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

        ans = 0
        if action!= 0 :
            for nextstate, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                reward = self.mdp.getReward(state,action, nextstate)
                disc = self.discount * self.values[nextstate]
                ans += prob * (reward +disc)
        else:
            return 0
        return ans


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        possibleaction = self.mdp.getPossibleActions(state)
        ans = None
        maxi = -1e10
        if self.mdp.isTerminal(state) is None or len(possibleaction)==0:
            return None
        for act in possibleaction:
            q = self.computeQValueFromValues(state, act)
            if q > maxi:
                maxi = q
                ans = act
        return ans

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
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        for i in range(0, self.iterations):
            current = self.mdp.getStates()[i % len(self.mdp.getStates())]
            act = self.getAction(current)
            if act is not None:
                q = self.computeQValueFromValues(current, act)
                self.values[current] = q

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

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        pd = {}
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for nextstate, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    if prob > self.theta or nextstate in pd.keys():
                        if nextstate not in pd :
                            pd[nextstate] = [state]
                        else:
                            pd[nextstate].append(state)

        priq = util.PriorityQueue()
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                diff = abs(self.values[state] - self.computeQValueFromValues(state, self.computeActionFromValues(state)))
                priq.push(state, -diff)
        i = 0
        while i < self.iterations:
            we = priq.isEmpty()
            e = not we
            if  e:
                state = priq.pop()
                if not self.mdp.isTerminal(state):
                    maxi = -1e5
                    for action in self.mdp.getPossibleActions(state):
                        if self.computeQValueFromValues(state, action) > maxi:
                            maxi = self.computeQValueFromValues(state, action)
                    self.values[state] = maxi

                    for p in pd[state]:
                        if not self.mdp.isTerminal(p):
                            diff = abs(self.values[p] - self.computeQValueFromValues(p, self.computeActionFromValues(p)))
                            if diff > self.theta:
                                priq.update(p, -diff)
            i +=1

