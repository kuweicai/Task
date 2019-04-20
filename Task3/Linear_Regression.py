#coding=utf-8
import numpy as np
import math
from sklearn.datasets import load_boston #load data, there is house price of Boston
import collections


def squared_distance(v, w):
    vector_subtract = [v_i - w_i for v_i, w_i in zip(v, w)]
    return sum(vector_subtract_i * vector_subtract_i for vector_subtract_i, vector_subtract_i
               in zip(vector_subtract, vector_subtract))


def distance(v, w):
    return math.sqrt(squared_distance(v, w))

# Linear Regression base on batch gradient descent
class LinearRegression:
    def __init__(self, data, target):   # data is the data to learn, target, the regression data
        self.data = data
        self.target = target
        theta = (np.zeros((1, len(data[0])))).tolist()  # init theta as 0
        self.theta = [item for sublist in theta for item in sublist]
        # for i in self.theta:
            # i=i+1
        self.last_cost = self.cost_fun()

    #  hypothesis function: h = theta * X
    #  X is learning data
    def hypothesis(self, X):
        result = 0
        for i, j in zip(X, self.theta):
            result = result + i * j
        return result

    # cost function: cost =  0.5 * sum((hypothesis_value - real_value)^2) / m
    def cost_fun(self):
        cost = 0
        for X, y in zip(data, target):
            cost = cost + 0.5 * (self.hypothesis(X)-y) ** 2
        return cost

    # loss function: loss = sum((hypothesis_value - real_value) * X) / m
    # def loss_fun(self):
    #     loss = 0
    #     for X, y in zip(data, target):
    #         loss = loss + (self.hypothesis(X)-y) * self.hypothesis(X)
    #     return loss

    # gradient descent function: theta =  theta + learning_rate * gradient
    # gradient = sum((hypothesis_value - real_value) * X) / m
    def gradient_descent(self, learning_rate = 0.01):
        self.last_cost = self.cost_fun()
        new_theta = []
        for j in range(len(self.theta)):
            gradient = 0    # init gradient as 0
            for i in range(len(self.data)):
                gradient = gradient + (target[i] - self.hypothesis(data[i])) * data[i][j]
            new_t = self.theta[j] + learning_rate * gradient  # batch gradient descent
            new_theta.append(new_t)
        self.theta = new_theta  # record new theta

    def regress(self):
        step_count = 0
        max_loop = 100000
        while True:
            step_count = step_count + 1
            if step_count > max_loop:
                break
            theta_before = self.theta
            self.gradient_descent(0.00000001)
            theta_after = self.theta
            print(step_count, self.theta, '\n', self.cost_fun())
            if distance(theta_after, theta_before) < 0.000000001:
                break
        print("After ", step_count, "steps,achieve iterative convergence!")


if __name__ == '__main__':
    # 从sklearn的数据集中获取相关向量数据集data和房价数据集target
    data, target = load_boston(return_X_y=True)
    model = LinearRegression(data, target)
    model.regress()
    # 选取一部分的样本用来验证最终回归模型的效果
    test_data = []
    for i in range(len(data)):
        if i % 17 == 0:
            test_data.append([data[i], target[i]])
    for i in test_data:
        print("real: ", i[1], "  estimate: ", model.hypothesis(i[0]))