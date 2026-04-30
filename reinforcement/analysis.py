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
    # Ban đầu: answerNoise = 0.2
    # Ta giảm noise xuống 0 để xác suất đi đúng hướng là 100%
    answerNoise = 0.0
    return answerDiscount, answerNoise

# Thích lỗi thoát gần và chấp nhận rủi ro 
def question3a():
    # Giảm discount về gần bằng 0 để chỉ quan tâm đích ngắn
    answerDiscount = 0.2
    # Giản noise về 0 để tự tin không bị ngã
    answerNoise = 0
    # Phạt nhẹ để về đích nhanh
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Thích lối thoát gần nhưng không chấp nhận rủi ro => Phải đi xa hơn
def question3b():
    # Quan tâm tới đích ngắn
    answerDiscount = 0.2
    # Có rủi ro
    answerNoise = 0.2
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Thích lỗi thoát xa và chấp nhận rủi ro
def question3c():
    # Tăng discount gần bằng 1 để duy trì giá trị các phần thưởng ở xa
    answerDiscount = 0.9
    # Giản noise về 0 để tự tin không bị ngã ( Không rủi ro)
    answerNoise = 0.0
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Thích lối thoát xa nhưng không chấp nhận rủi ro
def question3d():
    # Đích có giá trị
    answerDiscount = 0.9
    # Có rủi ro
    answerNoise = 0.2
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Không quan tâm tới lối thoát và vực thẳm, agent sẽ đi lòng vòng để
# tích điểm vô tận 
def question3e():
    # Giá trị các phần thưởng ở xa không bị giảm
    answerDiscount = 1
    # Không rủi ro
    answerNoise = 0
    # Thưởng cực lớn. Mỗi bước đi được cộng 10 điểm, trong khi về đích cao nhất cũng chỉ được 10 điểm. 
    # Agent sẽ chọn đi lòng vòng để tích điểm vô tận.
    answerLivingReward = 10
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question7():
    answerEpsilon = None
    answerLearningRate = None
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
