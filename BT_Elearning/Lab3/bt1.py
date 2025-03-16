import numpy as np

# Chuyển đổi thành ma trận 2D
a = np.array([[1, 2, 3], [4, 5, 6]])   # Ma trận 2x3
b = np.array([[10, 20], [30, 40], [50, 60]])  # Ma trận 3x2

def matrix_multi(a, b):
    c = np.zeros((a.shape[0], b.shape[1]))  # Ma trận kết quả kích thước (2x2)
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            for k in range(a.shape[1]):
                c[i][j] += a[i][k] * b[k][j]
    return c

# Thực hiện phép nhân thủ công
print("Kết quả nhân ma trận (thủ công):")
print(matrix_multi(a, b))

# Sử dụng dot() của NumPy
print("Kết quả nhân ma trận (numpy.dot()):")
print(np.dot(a, b))
