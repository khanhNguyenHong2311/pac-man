# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.q_values = util.Counter()

    # Hàm này trả về giá trị Q value.
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if (state, action) in self.q_values:
            return self.q_values[(state, action)]
        else:
            return 0.0
        util.raiseNotDefined()

    # Hàm này tính toán Vk dựa trên các Q_value có sẵn (Tính V từ Q)
    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # Lấy các hành động hợp lệ tại trạng thái này
        legalActions = self.getLegalActions(state)

        # Nếu là trạng thái kết thúc, tức là không có hành động hợp lệ nào nữa, thì trả về 0.0
        if not legalActions:
            return 0.0

        # Tìm giá trị Q lớn nhất trong số các hành động hợp lệ
        # Công thức: V = Qmax(s, a)
        max_q = max([self.getQValue(state, action) for action in legalActions])
        
        return max_q
        util.raiseNotDefined()

    # computeActionFromQValues trả về hành động tốt nhất của trạng thái này. Ví dụ ở ô 1 đi sang Nam 
    # là tốt nhất ==> Hàm trả về hướng Nam  
    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Lấy các hành động khả thi, nếu không có hành động nào (trạng thái kết thúc), trả về None
        legalActions = self.getLegalActions(state)
        if not legalActions:
            return None

        # Tìm giá trị Q lớn nhất hiện tại (V)
        bestValue = self.computeValueFromQValues(state)
        
        # Tìm tất cả các hành động có giá trị Q bằng với giá trị tốt nhất này
        bestActions = [action for action in legalActions if self.getQValue(state, action) == bestValue]

        # Chọn ngẫu nhiên một trong các hành động tốt nhất đó
        return random.choice(bestActions)
        util.raiseNotDefined()

    # Mỗi khi đến lượt đi, sẽ có xác suất epsilon% AI chọn bừa 1 hướng đi linh tinh mặc
    # kệ cái Q value , mục đích để tìm đường mới (Khám phá).
    # Và AI sẽ có xác suất (1 - epsilon)% đi đúng theo Q_value, tức là đi theo Qmax (Khai thác)
    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        # Hàm này trả về hành động có thể thực hiện ở ô hiện tại
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            # Hàm này trả về hành động có Q value max ( hành động tốt nhất của trạng thái này)
            action = self.getPolicy(state)

        return action
        
        util.raiseNotDefined()

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # Lấy giá trị Q hiện tại: Q(s, a) trong công thức Bellman Q-Learning
        current_q = self.getQValue(state, action)
        
        # Tính toán "Sample": Reward + gamma * Q(s', a') 
        # Q(s', a') là Qmax có thể đạt được từ trạng thái kế tiếp
        # Chú ý: self.getValue(nextState) là Q(s', a') ,cũng chính là giá trị V(s') trong công thức
        # self.discount là gamma - hệ số chiết khấu
        sample = reward + self.discount * self.getValue(nextState)
        
        # Cập nhật giá trị Q mới vào bảng self.q_values
        # Công thức: Q(s,a) = (1 - alpha) * Q(s,a) + alpha * sample
        # Trong đó anpha là hệ số học tập
        new_q = (1 - self.alpha) * current_q + self.alpha * sample
        self.q_values[(state, action)] = new_q
        

    # Trả về hành động tốt nhất của trạng thái này. Ví dụ ở ô 1 đi sang Nam 
    # là tốt nhất ==> getPolicy trả về hướng Nam  
    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    # Trả về giá trị trạng thái Vs
    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state): 
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
