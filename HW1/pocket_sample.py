import matplotlib.pyplot as plt
import numpy as np
import operator
import random
 
# 網路上找的 dataset 再加上亂數的 data 不可以線性分割
def rand_samples(m, b, n_points, rand_param):
    left_x_coors, left_y_coors = np.array([]), np.array([])
    right_x_coors, right_y_coors = np.array([]), np.array([])

    pos_points = int(n_points/2)
    neg_points = n_points - pos_points
    pos_count = 0
    neg_count = 0

    for _ in range(n_points):
        x = np.random.randint(0, rand_param)
        flag = 0
        while flag != 1:
            r = np.random.randint(250, 1000)
            s = random.choice([-1,1])
            state = m * x + b + r*s
            if  s < 0 and pos_count < pos_points:
                pos_count += 1
                flag = 1
                right_x_coors = np.append(right_x_coors, x)
                right_y_coors = np.append(right_y_coors, state)
            elif s > 0 and neg_count < neg_points:
                neg_count += 1
                flag = 1
                left_x_coors = np.append(left_x_coors, x)
                left_y_coors = np.append(left_y_coors, state)

    x_coors = np.append(left_x_coors, right_x_coors)
    y_coors = np.append(left_y_coors, right_y_coors)
    a = tuple(x_coors)
    b = tuple(y_coors)
    c = zip(a, b)
    d = [-1]*neg_points + [1]*pos_points
    e = zip(c,d)
    dataset = [((1,) + x, y) for x, y in list(e)]
    return dataset
 
 
# 內積
def dot(*v):
    return sum(map(operator.mul, *v))
 
 
# 取 sign (1, 0, -1)
def sign(v):
    if v > 0:
        return 1
    elif v == 0:
        return 0
    else:  # v < 0
        return -1
 
 
# 判斷有沒有分類錯誤
def check_error(w, x, y):
    if sign(dot(w, x)) != y:
        return True
    else:
        return False
 
 
# 更新 w
def update(w, x, y):
    u = map(operator.mul, [y] * len(x), x)
    w = map(operator.add, w, u)
    return list(w)
 
 
# 總錯誤數
def sum_errors(w, dataset):
    errors = 0
    for x, y in dataset:
        if check_error(w, x, y):
            errors += 1
 
    return errors
 
 
# POCKET 演算法實作
def pocket(dataset):
    # 初始化 w
    w = [0] * 3
    min_e = sum_errors(w, dataset)
 
    max_t = 500
    for t in range(0, max_t):
        wt = None
        et = None
 
        while True:
            x, y = random.choice(dataset)
            if check_error(w, x, y):
                wt = update(w, x, y)
                et = sum_errors(wt, dataset)
                break
 
        if et < min_e:
            w = wt
            min_e = et
 
        print("{}: {}".format(t, tuple(w)))
        print("min erros: {}".format(min_e))
 
        t += 1
 
        if min_e == 0:
            break
 
    return (w, min_e)
 
 
# 主程式
def main():

    # 執行，並輸入新的 list
    m = random.randint(-100, 100)
    b = random.randint(-100, 100)
    n_points = 30
    rand_param = 100
    dataset = rand_samples(m, b, n_points, rand_param)
    w, e = pocket(list(dataset))
 
    # 畫圖
    fig = plt.figure()
 
    # numrows=1, numcols=1, fignum=1
    ax1 = fig.add_subplot(111)
 
    xx = list(filter(lambda d: d[1] == -1, dataset))
    ax1.scatter([x[0][1] for x in xx], [x[0][2] for x in xx],
                s=100, c='b', marker="x", label='-1')
    oo = list(filter(lambda d: d[1] == 1, dataset))
    ax1.scatter([x[0][1] for x in oo], [x[0][2] for x in oo],
                s=100, c='r', marker="o", label='1')
    l = np.linspace(-2, 2)
 
    # w0 + w1x + w2y = 0
    # y = -w0/w2 - w1/w2 x
    if w[2]:
        a, b = -w[1] / w[2], -w[0] / w[2]
        ax1.plot(l, a * l + b, 'b-')
    else:
        ax1.plot([-w[0] / w[1]] * len(l), l, 'b-')
 
    plt.legend(loc='upper left', scatterpoints=1)
    plt.show()
    plt.savefig('pocket_sample.png')
 
 
if __name__ == '__main__':
    main()