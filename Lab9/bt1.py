from multiprocessing import Process
from collections import defaultdict

class Graph:
    def __init__(self, dothi):
        self.dothi = dothi
        self.ROW = len(dothi)

    def tang_luong(self, a, z, P):
        # Bàn đầu tất cả các đỉnh là chưa xét
        visited = [False] * (self.ROW)

        # BFS - tìm kiếm theo chiều rộng
        queue = []
        # Đánh dấu nút (đỉnh) đã xét và đưa vào hàng đợi
        queue.append(a)
        visited[a] = True

        # Giảm lượng đường dẫn còn lại
        while queue:
            # Lấy một phần tử ra khỏi hàng đợi
            u = queue.pop(0)

            # Xét các đỉnh liền kề với u - là các đỉnh thuộc tập hợp các hàng đợi
            for ind, val in enumerate(self.dothi[u]):
                if (visited[ind] == False and val > 0):
                    visited[ind] = True
                    P[ind] = u
                    if (ind == z):
                        return True
        return False

    def luong_cuc_dai(self, a, z):
        # Lưu trữ đường đi nghịch
        P = [-1] * (self.ROW)
        f = 0  # Lưu lượng ban đầu bằng 0

        # Tăng lưu lượng khi có con đường từ a đến z
        while self.tang_luong(a, z, P):
            # Tìm lưu lượng con đường hiện tại
            flow = float("Inf")
            s = z
            while (s != a):
                flow = min(flow, self.dothi[P[s]][s])
                s = P[s]

            # Thêm lưu lượng vào lưu lượng tổng
            f += flow

        return f

# Ví dụ minh họa
dothi = [[0, 3, 5, 0, 0, 0],
         [0, 0, 2, 2, 0, 0],
         [0, 0, 0, 0, 2, 0],
         [0, 0, 0, 0, 0, 2],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

g = Graph(dothi)
a = 0
z = 5
print("Luong cuc dai la %d" % g.luong_cuc_dai(a, z))

if __name__ == '__main__':
    p = Process(target=Graph, args=(g,))
    p.start()
    p.join()