import matplotlib.pyplot as plt
import numpy as np
import operator
import random
import time
import statistics

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
            r = np.random.randint(500, 1000)
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
    mean_x = np.mean(x_coors)
    std_x = statistics.pstdev(x_coors)
    for i in range(len(x_coors)):
        x_coors[i] = (x_coors[i]-mean_x)/std_x

    y_coors = np.append(left_y_coors, right_y_coors)
    mean_y = np.mean(y_coors)
    std_y = statistics.pstdev(y_coors)
    for i in range(len(y_coors)):
        y_coors[i] = (y_coors[i]-mean_y)/std_y

    a = tuple(x_coors)
    b = tuple(y_coors)
    c = zip(a, b)
    d = [-1]*(neg_points-50) + [1]*(50) + [1]*(pos_points-50) + [-1]*(50)    
    e = zip(c,d)
    mis_dataset = [((1,) + x, y) for x, y in list(e)]
    #print(len(mis_dataset))

    a = tuple(x_coors)
    b = tuple(y_coors)
    c = zip(a, b)
    d = [-1]*(neg_points) + [1]*(pos_points)    
    e = zip(c,d)
    cor_dataset = [((1,) + x, y) for x, y in list(e)]
    #print(len(cor_dataset))
    #print(mis_dataset)
    return mis_dataset, cor_dataset

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

def sum_errors(w_t, dataset):
    errors = 0
    for x, y in dataset:
        if check_error(w_t, x, y) == True:
            errors = errors + 1
    return errors
 
def pocket(dataset, updates=1000):
    w = np.zeros(3)
    for _ in range(updates):
        
        """"
        while True:
            x, y = random.choice(dataset)
            if check_error(w, x, y):
                break
        """
        x, y = random.choice(dataset)
        w_t = update(w, x, y)
        error = sum_errors(w, dataset)
        error_t = sum_errors(w_t, dataset)
        if error_t < error:
            w = w_t
        if error_t == 0:
            break
    return w, error_t
    
def main():

    m = random.randint(-100, 100)
    b = random.randint(-100, 100)
    n_points = 2000
    rand_param = 100
    mis_dataset, cor_dataset = rand_samples(m, b, n_points, rand_param)

    #correct labelled
    w, err = pocket(cor_dataset)
    w_cor = w
    plt.subplot(211)
    xx = list(filter(lambda d: d[1] == -1, cor_dataset))
    #print(xx)
    for i in range(int(n_points/2)):
        #print(i)
        plt.plot(xx[i][0][1], xx[i][0][2], 'o', color='red')   # negative 

    oo = list(filter(lambda d: d[1] == 1, cor_dataset))
    for i in range(int(n_points/2)):
        plt.plot(oo[i][0][1], oo[i][0][2], 'o', color='blue')   # negative 
    x = np.linspace(-2, 2)

    # w0 + w1x + w2y = 0
    # y = -w0/w2 - w1/w2 x
    plt.plot(x, (-w[1]/w[2])*x + (-w[0]/w[2]))
    #print('find',(-w[1]/w[2]))
    plt.show()
    plt.title('Correct labelled')


    #with mislabelled data
    w, t = pocket(mis_dataset)
    w_mis = w
    plt.subplot(212)
    xx = list(filter(lambda d: d[1] == -1, mis_dataset))
    #print(xx)
    for i in range(int(n_points/2)):
        #print(i)
        plt.plot(xx[i][0][1], xx[i][0][2], 'o', color='red')   # negative 

    oo = list(filter(lambda d: d[1] == 1, mis_dataset))
    for i in range(int(n_points/2)):
        plt.plot(oo[i][0][1], oo[i][0][2], 'o', color='blue')   # negative 
    x = np.linspace(-2, 2)

    # w0 + w1x + w2y = 0
    # y = -w0/w2 - w1/w2 x
    plt.plot(x, (-w[1]/w[2])*x + (-w[0]/w[2]))
    plt.show()
    plt.title('mislabelled')
    #print((-w[1]/w[2]))
    plt.savefig('problem4.png')
    #print(sum_errors(w_poc, dataset))
    accurate_rate_cor = (2000-sum_errors(w_cor, cor_dataset))/2000
    accurate_rate_mis_to_cor = (2000-sum_errors(w_mis, cor_dataset))/2000
    accurate_rate_mis_to_mis = (2000-sum_errors(w_mis, mis_dataset))/2000
    #print(sum_errors(w_cor, cor_dataset))
    #print(sum_errors(w_mis, cor_dataset))
    print('accurate rate of correct dataset: {:.2%}' .format(accurate_rate_cor))
    print('accurate rate of mislabelled dataset to correct dataset: {:.2%}' .format(accurate_rate_mis_to_cor))
    print('accurate rate of mislabelled dataset to mislabelled dataset: {:.2%}' .format(accurate_rate_mis_to_mis))
    #print(sum_errors(w, dataset))
    
if __name__ == '__main__':
    main()