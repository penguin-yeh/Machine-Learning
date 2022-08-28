import matplotlib.pyplot as plt
import numpy as np
import operator
import random
 
a = [1,2,3,4]
b = [4,5,6,7]

a = tuple(a)
b = tuple(b)
c = zip(a, b)
d = [-1]*2 + [1]*2
e = zip(c,d)
#print(list(e))
dataset = [((1,) + x, y) for x, y in list(e)]
print(len(dataset))