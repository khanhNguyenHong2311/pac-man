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
            V = util.Counter()

            for state in self.mdp.getStates():
                maxQ = -99999
                possibleActions = self.mdp.getPossibleActions(state)
                if self.mdp.isTerminal(state):
                    V[state] = 0.0
                elif not possibleActions:
                    V[state] = 0.0
                else:         
                    for action in possibleActions:
                        q = self.computeQValueFromValues(state,action)
                        if q > maxQ:
                            maxQ = q
                if maxQ != -99999:
                    V[state] = maxQ
                else: 
                    V[state] = 0.0

            self.values = V

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # Hàm tính toán Q_value từ các giá trị của các ô V có sẵn (Tính Q từ V)
    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0.0
        # Hàm stateAndProbs tính giá trị của T(s,a,s')
        # Vòng lặp for dưới đây là [ tổng xích ma s' * T(s,a,s') ] trong công thức Bellman
        for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
            # reward = R(s,a,s')
            # self.discount là hệ số chiết khấu (gamma)
            # self.values[nextState]: Là giá trị của trạng thái kế tiếp ( là Vk(s') trong công thức)
            reward = self.mdp.getReward(state, action, nextState)
            q_value += probability * (reward + self.discount * self.values[nextState])

        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Nếu agent rơi vào trạng thái kết thúc, tức là không còn hành động nào để thực hiện nữa
        # ta trả về None theo đề bài
        if state == self.mdp.isTerminal(state):
            return None
        
        # Hàm getPossibleActions liệt kê tất cả các hướng đi có thể tại ô hiện tại
        # Đây chính là tập hợp actions mà bạn có thể chọn.
        possibleActions = self.mdp.getPossibleActions(state)
        if not possibleActions:
            return None
        
        maxValue = -99999
        action_res = None
        # Với mỗi hành động x trong actions, ta tính toán Q-value và trả về hành động nào có Q-value cao nhất
        for action in possibleActions:
            q = self.computeQValueFromValues(state,action)
            if q > maxValue:
                maxValue = q
                action_res = action 
        
        return action_res


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
        # Xây dựng mảng lưu các tiền bối cho từng trạng thái ==> Để biết được đến được trạng thái 
        # A thì có thể đi từ những ô nào?.
        predecessors = self.computeAllPredecessors()

        pq = util.PriorityQueue()

        # Thêm tất cả các trạng thái kèm diff vào pq
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                diff = self.computeDiff(s)
                # min heap
                pq.push(s, -diff)

        # Vòng lặp cập nhật maxQvalue
        # Thay vì cập nhật toàn bộ bản đồ ở mỗi vòng lặp, ta chỉ lặp đúng self.iterations lần 
        # và mỗi lần chỉ xử lý duy nhất một ô đang sai lệch nhiều nhất.
        for i in range(self.iterations):
            # Lấy ô sai nhất ra sửa 
            if pq.isEmpty():
                break

            s = pq.pop()

            # Cập nhật V(s)=Q max(s,a) ( Đây là đoạn sửa V(s) )
            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                self.values[s] = max([self.getQValue(s, a) for a in actions])

            # Duyệt tiền nhiệm của s (là cái ô mình mới sửa) để tính toán lại điểm của mình
            for p in predecessors[s]:
                # Nếu không phải ô kết thúc
                if not self.mdp.isTerminal(p):
                    # Tính toán lại diff
                    diff = self.computeDiff(p)
                    # self.theta là là một ngưỡng sai số rất nhỏ do cấu hình bài toán đặt ra
                    # Dòng này kiểm tra xem ô p này có bị sai lệch nhiều hay không. Nếu sai số diff của nó lớn hơn ngưỡng theta, 
                    # tức là ô p này đang bị đánh giá sai về giá trị thực tế của nó => Cần phải sửa sai cho nó sớm.
                    if diff > self.theta:
                        # Đẩy ô p này vào trong hàng đợi ưu tiên pq 
                        # (hoặc nếu nó đã nằm sẵn trong hàng đợi rồi thì cập nhật lại độ ưu tiên mới cho nó).
                        pq.update(p, -diff)

    def computeAllPredecessors(self):
        # Mỗi state s 1 set tiền nhiệm
        predecessors = {s: set() for s in self.mdp.getStates()}
        
        for s in self.mdp.getStates():
            # Ô kết thúc thì không đi đâu tiếp được nên bỏ qua
            if self.mdp.isTerminal(s):
                continue
            # Duyệt tất cả các trạng thái tiếp theo (next_state) có thể đến từ ô s
            for action in self.mdp.getPossibleActions(s):
                 # Nếu từ s có thể đi tới next_state, nghĩa là s chính là TIỀN NHIỆM của next_state
                for next_state, prob in self.mdp.getTransitionStatesAndProbs(s, action):
                    if prob > 0:
                        predecessors[next_state].add(s)
        return predecessors

    # Mục đích hàm này là: Tính toán độ sai lệch giữa giá trị hiện tại của 1 ô V(s) và giá trị 
    # thực tế tốt nhất mà nó có thể đạt được max Q(s,a)
    def computeDiff(self, state):
        # Lấy ra danh sách hành động hợp lệ
        actions = self.mdp.getPossibleActions(state)
        # Nếu không có hành động khả thi (ô kết thúc) thì trả về 0
        if not actions:
            return 0
        # Tính Q-value lớn nhất trong các hành động có thể thực hiện từ ô này
        max_q = max([self.getQValue(state, action) for action in actions])
        # Sai số chính là trị tuyệt đối của hiệu hai giá trị V(s) và Qvalue max
        return abs(self.values[state] - max_q)

