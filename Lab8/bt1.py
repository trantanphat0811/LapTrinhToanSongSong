import numpy as np
from threading import Thread

# Định nghĩa hai ma trận A và B
A = np.array([[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]])

B = np.array([[0, 10, 20],
              [30, 40, 50],
              [60, 70, 80]])

# Tính phép nhân ma trận
pro = np.matmul(A, B)

# Hàm pro() để in kết quả
def pro():
    print("matrix multiplication:", pro)

# In kết quả trực tiếp
print("matrix multiplication:", pro)

# Sử dụng luồng để gọi hàm pro()
step = Thread(target=pro)
step.start()
step.join()