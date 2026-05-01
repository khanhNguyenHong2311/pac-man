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
        # Ban đầu tất cả Vk = 0. Để tính Vk + 1 ta cần biết Vk
        # Nếu ta chỉ lặp 1 lần thì chỉ có các Vk + 1 kề V0 mới có điểm, các ô còn lại Vk vẫn = 0 
        # Nên ta lặp lại nhiều lần, để Vk loang hết ra các ô
        for i in range(self.iterations):
            # Tạo bản sao tạm thời để lưu giá trị Vk+1 mới
            new_values = util.Counter()

            # Lấy danh sách tất cả trạng thái và duyệt qua từng trạng thái (ô) đó
            states = self.mdp.getStates()
            for state in states:
                # Nếu trạng thái là trạng thái kết thúc, giá trị luôn là 0
                if self.mdp.isTerminal(state):
                    new_values[state] = 0
                else:
                    # Lấy tất cả hành động có thể làm trong trạng thái này
                    # Với mỗi hành động, AI tính Q_value, sau đó chọn hướng ngon nhất
                    actions = self.mdp.getPossibleActions(state)
                    values = []
                    for action in actions:
                        q_value = self.computeQValueFromValues(state, action)
                        values.append(q_value)
                    new_values[state] = max(values)
            self.values = new_values





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
        # Hàm stateAndProbs tính giá trị của T(s,a,s')
        stateAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        sum = 0
        # Vòng lặp for tương ứng dấu tổng xích ma s' 
        for nextState, prob in stateAndProbs:
            reward = self.mdp.getReward(state, action, nextState)
            # self.discount là hệ số chiết khấu (gamma)
            # self.values[nextState]: Là giá trị của trạng thái kế tiếp ( Vk(s') )
            sum += prob * (reward + self.discount * self.values[nextState])
        return sum
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
        # Nếu agent rơi vào trạng thái kết thúc, tức là không còn hành động nào để thực hiện nữa
        # ta trả về None theo đề bài
        if self.mdp.isTerminal(state):
            return None
        # Hàm getPossibleActions liệt kê tất cả các hướng đi có thể tại ô hiện tại
        # Đây chính là tập hợp actions mà bạn có thể chọn.
        actions = self.mdp.getPossibleActions(state)
        # Với mỗi hành động x trong actions, ta tính toán Q-value và trả về hành động nào có Q-value cao nhất
        bestAction = max(actions, key=lambda x: self.computeQValueFromValues(state, x))

        return bestAction
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

    # Nhược điểm của Value Iteration:  Ở mỗi vòng lặp, bạn bắt tất cả các ô trên bản đồ phải tính lại Qmax và cập nhật V. 
    # Ngay cả những ô ở xa chưa được loang V tới, hoặc những ô đã có V rồi cũng bị duyệt lại. Điều này cực kỳ lãng phí tài nguyên.
    # Giải pháp: Prioritized Sweeping: Bạn chỉ cập nhật những ô có sai lệch giữa V và Qmax là lớn nhất. Nếu một ô đã có giá trị ổn định, 
    # nó sẽ không bao giờ bị "gọi tên" vào hàng đợi. Bên cạnh đó nhờ vào danh sách Predecessors, ngay khi một ô được cập nhật, nó sẽ 
    # "nhắc" các ô dẫn đến nó kiểm tra lại giá trị ngay. => Tiết kiệm tài nguyên

    def runValueIteration(self):
        # Bước 1: Xây dựng mảng lưu các tiền bối cho từng trạng thái ==> Để biết được đến được trạng thái A thì có thể đi từ những ô nào?.
        predecessors = {}
        # Duyệt qua tất cả các ô trên bản đồ
        for s in self.mdp.getStates():
            # Nếu ô đó không phải trạng thái kết thúc
            if not self.mdp.isTerminal(s):
                # Duyệt qua các hướng đi( hành động) có thể đi
                for action in self.mdp.getPossibleActions(s):
                    # Kiểm tra xem nếu thực hiện hướng đi đó, bạn có cơ hội nhảy sang ô nextState nào và xác suất là bao nhiêu.
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(s, action):
                        # Nếu xác suất > 0, tức là có thể từ s nhảy sang nextState
                        if prob > 0:
                            # Nếu nextState chưa có tên trong danh sách, hãy tạo một cái "rổ" (set) cho nó.
                            if nextState not in predecessors:
                                predecessors[nextState] = set()
                            # Bỏ ô s vào rổ của nextState. Điều này ghi nhận rằng: s là một tiền bối của nextState.
                            predecessors[nextState].add(s)

        # Bước 2: Khởi tạo hàng đợi ưu tiên trống
        pq = util.PriorityQueue()

        # Bước 3: Với mỗi trạng thái không phải kết thúc, tính diff ban đầu và đẩy vào PQ.
        # Bước này giống như việc bạn đi kiểm tra tất cả các phòng trong một tòa nhà, đo xem phòng 
        # nào bẩn nhất rồi ghi tên chúng vào một danh sách ưu tiên để chuẩn bị dọn dẹp.
        # Duyệt qua các trạng thái
        for s in self.mdp.getStates():
            # Nếu không phải trạng thái kết thúc
            if not self.mdp.isTerminal(s):
                # Tìm Q-value cao nhất và tính độ lệch diff
                max_q = max([self.getQValue(s, a) for a in self.mdp.getPossibleActions(s)])
                diff = abs(self.values[s] - max_q)
                # Đẩy vào PQ với độ ưu tiên là -diff (vì đây là min-heap)
                pq.push(s, -diff)

        # Bước 4. Vòng lặp cập nhật giá trị (Lau dọn)
        for i in range(self.iterations):
            # Thuật toán dừng khi hàng đợi rỗng
            if pq.isEmpty():
                break
            
            # Lấy trạng thái s có sai lệch lớn nhất ra
            s = pq.pop()

            # Cập nhật giá trị cho s (nếu không phải terminal)
            # Việc cập nhật V = Qmax của Prioritized Sweeping giống với Value Iteration. Nhưng khác ở chỗ Prioritized Sweeping
            # chỉ chạy cho duy nhất một ô s vừa được lấy ra khỏi hàng đợi ưu tiên. Trong khi đó Value Iteration thì ở mỗi vòng lặp 
            # đều tính lại max_q cho tất cả các ô

            if not self.mdp.isTerminal(s):
                max_q = max([self.getQValue(s, a) for a in self.mdp.getPossibleActions(s)])
                self.values[s] = max_q

            # Khi một ô vừa được cập nhật một giá trị mới, tất cả những ô có thể dẫn đến s (tức là các predecessors p) đều bị ảnh hưởng.
            # ==> Phải xét lại các predecessors
            # Kiểm tra các tiền bối (p) của s
            for p in predecessors.get(s, []):
                if not self.mdp.isTerminal(p):
                    # Tính lại diff cho p
                    max_q_p = max([self.getQValue(p, a) for a in self.mdp.getPossibleActions(p)])
                    diff = abs(self.values[p] - max_q_p)
                    
                    # Thuật toán không cập nhật tất cả mọi ô để tránh lãng phí.
                    # Chỉ khi sai lệch lớn hơn theta thì mới cập nhật, đưa vào/cập nhật trong PQ
                    if diff > self.theta:
                        pq.update(p, -diff)

