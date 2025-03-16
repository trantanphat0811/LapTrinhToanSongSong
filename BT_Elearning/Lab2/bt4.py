import math
from multiprocessing import Pool

def g(n):
    return n*n

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(g, [1,4,9,16,25]))
        