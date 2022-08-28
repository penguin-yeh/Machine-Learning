import numpy as np
import matplotlib.pyplot as plt
import operator
import random



#generate linear sepearable dataset
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
            r = np.random.randint(200, 1000)
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
    print(neg_count,pos_count)
    e = zip(c,d)
    print(list(e))
    dataset = [((1,) + x, y) for x, y in list(e)]
    return dataset

def dot(u, v):
    return sum(map(operator.mul, u, v))

def sign(v):
    if v > 0:
        return 1
    elif v == 0:
        return 0
    else:
        return -1

def check_error(w, x, y):
    if sign(dot(w, x)) != y: # inner product
        return True
    else:
        return False

def update(w, x, y):
    u = map(operator.mul, [y]*len(x), x)
    w = map(operator.add, w, u)
    return list(w)

def check_error(w, x, y):
    if sign(dot(w, x)) != y: # inner product
        return True
    else:
        return False
def sum_errors(w_t, dataset):
    errors = 0
    for x, y in dataset:
        if check_error(w_t, x, y) == True:
            errors = errors + 1
    return errors


def pla(dataset):
    w = np.zeros(3)
    min_errs = sum_errors(w, dataset)
    w_t = []
    t = 0
    while t < 1000:
        no_error = True
        while True:
            x, y = random.choice(dataset)
            if check_error(w, x, y) == True:
                w_t = update(w, x, y)
                err_t = sum_errors(w_t, dataset)
                no_error = False
                break
        if err_t < min_errs:
            w = w_t
            min_errs = err_t
            print(min_errs)
        t += 1
        if sum_errors(w, dataset)==0:
            break
    return w, t


def main():

    rawData = [
    ((-0.4, 0.3), -1),
    ((-0.3, -0.1), -1),
    ((-0.2, 0.4), -1),
    ((-0.1, 0.1), -1),
    ((0.9, -0.5), 1),
    ((0.7, -0.9), 1),
    ((0.8, 0.2), 1),
    ((0.4, -0.6), 1),
    ((0.2, 0.6), -1),
    ((-0.5, -0.5), -1),
    ((0.7, 0.3), 1),
    ((0.9, -0.6), 1),
    ((-0.1, 0.2), -1),
    ((0.3, -0.6), 1),
 ]
 
# 加入 x0
    dataset = [((1,) + x, y) for x, y in rawData]

    num = []
    m = np.random.randint(-100,100)
    b = np.random.randint(-100,100)
    n_points = 14
    rand_param = 30
    dataset = rand_samples(m, b, n_points, rand_param)
    w, t = pla(dataset)
    num.append(t)

    xx = list(filter(lambda d: d[1] == -1, dataset))
    #print(xx)
    for i in range(int(n_points/2)):
        #print(i)
        plt.plot(xx[i][0][1], xx[i][0][2], 'o', color='red')   # negative 

    oo = list(filter(lambda d: d[1] == 1, dataset))
    for i in range(int(n_points/2)):
        plt.plot(oo[i][0][1], oo[i][0][2], 'o', color='blue')   # negative 
    
    x = np.linspace(-2, 2)

    # w0 + w1x + w2y = 0
    # y = -w0/w2 - w1/w2 x
    #plot line
    plt.plot(x, (-w[1] / w[2]) * x + (-w[0] / w[2]))
    plt.show()
    plt.savefig('problem2.png')
    """
    sum = 0
    for i in num:
        sum = sum + i
    print('each iteration :',num)
    print('average iterations :%.2f' % (sum/3))
    """
    print(sum_errors(w, dataset))

if __name__ == '__main__':
    main()