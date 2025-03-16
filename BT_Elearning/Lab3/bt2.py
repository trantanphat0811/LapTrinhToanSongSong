import numpy as np 
from numba import njit, prange
a=np.array([[1,2,3],[4,5,6]])
b=np.array([[10,20],[30,40],[50,60]])
def matrix_multi(a, b):
    assert a.shape [1]== b.shape[0]
    c= np.zeros((a.shape[0], b.shape[1]))
    for i in prange (a.shape[0]):
        for j in prange (b.shape[1]):
            for k in prange (a.shape[1]):
                c[i][j]+= a[i][k]*b[k][j]
    return c
result = matrix_multi(a,b)
print(result)