# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.016
    # Ban đầu: answerNoise = 0.2
    # Ta giảm noise xuống gần 0 (hoặc bằng 0) để xác suất đi đúng hướng là 100%
    return answerDiscount, answerNoise

# Thích lỗi thoát gần và chấp nhận rủi ro 
def question3a():
    # Giảm discount về gần bằng 0 để chỉ quan tâm đích ngắn
    answerDiscount = 0.1
    # Giảm noise về 0 để tự tin không ngã (cân mọi rủi ro)
    answerNoise = 0
    # Phạt nhẹ để pacman về đích sớm
    # Nếu để livingReward dương thì mỗi bước đi pacman đều có thêm điểm => Pacman sẽ lòng vòng không kết thúc game
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Thích lối thoát gần nhưng không chấp nhận rủi ro => Phải đi xa hơn
def question3b():
    # Quan tâm tới đích ngắn
    answerDiscount = 0.1
    # Có rủi ro 
    answerNoise = 0.1
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Thích lỗi thoát xa và chấp nhận rủi ro
def question3c():
    #  Quan tâm đích xa
    answerDiscount = 1
    # Cân mọi rủi ro
    answerNoise = 0
    answerLivingReward = -0.01
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Thích lối thoát xa nhưng không chấp nhận rủi ro ( né vực )
def question3d():
    # Đích có giá trị
    answerDiscount = 1
    # Có rủi ro 
    answerNoise = 0.1
    answerLivingReward = -0.01
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 1000
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Nếu để e thấp, AI không dám đi liều => Không bao giờ thấy phần thường ở cuối cấp
# Nếu để e cao, AI dám đi liều, nhưng vì liều nên sẽ liên tục bị rơi xuống cấu
# Trong một môi trường mà "sai một ly đi một dặm" như cây cầu này, 50 ván là khoảng thời gian quá 
# ngắn để thuật toán Q-Learning có thể vừa khám phá ra đường đi, vừa cập nhật đủ giá trị Q để khẳng định 
# đó là đường tối ưu với độ tin cậy 99%. ==> NOT POSSIBLE
def question7():
    answerEpsilon = None
    answerLearningRate = None
    # If not possible, return 'NOT POSSIBLE'
    return 'NOT POSSIBLE'   

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
