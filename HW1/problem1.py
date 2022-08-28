import numpy as np
import matplotlib.pyplot as plt
import random

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
            r = np.random.randint(-1000, 1000)
            state = m * x + b + r
            if  r < 0 and pos_count < pos_points:
                pos_count += 1
                flag = 1
                right_x_coors = np.append(right_x_coors, x)
                right_y_coors = np.append(right_y_coors, state)
            elif r > 0 and neg_count < neg_points:
                neg_count += 1
                flag = 1
                left_x_coors = np.append(left_x_coors, x)
                left_y_coors = np.append(left_y_coors, state)
    return left_x_coors, left_y_coors, right_x_coors, right_y_coors

if __name__ == '__main__':
    # y = mx + b
    m, b = 2, 5
    n_points = 2000
    rand_param = 30
    pos_num = int(n_points / 2)

    #plot
    x = np.arange(rand_param + 1)
    y = m * x + b
    plt.plot(x, y)

    #random generate ponts
    left_x_coors, left_y_coors, right_x_coors, right_y_coors = rand_samples(m, b, n_points, rand_param)

    # plot random points. Blue: positive, red: negative
    plt.plot(right_x_coors[:], right_y_coors[:], 'o', color='blue')   # positive
    plt.plot(left_x_coors[:], left_y_coors[:], 'o', color='red')    # negative
    plt.show()
    plt.savefig('problem1.png')

    x, y = random.choice(dataset)
    print(x)
    print(y)