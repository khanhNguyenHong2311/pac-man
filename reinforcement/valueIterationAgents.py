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
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)



class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
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
        # tạo dsach các set tiền nhiệm
        predecessors = self.computeAllPredecessors()

        pq = util.PriorityQueue()

        # thêm tất cả các trạng thái kèm diff vào pq
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                diff = self.computeDiff(s)
                # min heap
                pq.push(s, -diff)

        # vòng lặp cập nhật maxQvalue
        for i in range(self.iterations):

            if pq.isEmpty():
                break

            s = pq.pop()
            # cập nhật V(s)=Q max(s,a)
            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                self.values[s] = max([self.getQValue(s, a) for a in actions])

            # duyệt tiền nhiệm của s để cập nhật tiếp
            for p in predecessors[s]:
                if not self.mdp.isTerminal(p):
                    diff = self.computeDiff(p)
                    if diff > self.theta:
                        # cập nhật ưu tiên nếu p có sẵn trong pq
                        pq.update(p, -diff)

    def computeAllPredecessors(self):
        #Mỗi state s 1 set tiền nhiệm
        predecessors = {s: set() for s in self.mdp.getStates()}
        for s in self.mdp.getStates():
            if self.mdp.isTerminal(s):
                continue
            for action in self.mdp.getPossibleActions(s):
                for next_state, prob in self.mdp.getTransitionStatesAndProbs(s, action):
                    if prob > 0:
                        predecessors[next_state].add(s)
        return predecessors

    def computeDiff(self, state):
        #Tính toán sai số: |V(s) - max Q(s,a)|
        actions = self.mdp.getPossibleActions(state)

        if not actions:
            return 0
        
        max_q = max([self.getQValue(state, action) for action in actions])
        return abs(self.values[state] - max_q)

