from multiprocessing import Process
from collections import defaultdict

class Graph:
    def __init__(self, dothi):
        self.dothi = [row[:] for row in dothi]  # Tạo bản sao để tránh thay đổi ma trận gốc
        self.ROW = len(dothi)

    def tang_luong(self, a, z, P):
        # Ban đầu tất cả các đỉnh là chưa xét
        visited = [False] * self.ROW

        # BFS - tìm kiếm theo chiều rộng
        queue = []
        # Đánh dấu nút (đỉnh) đã xét và đưa vào hàng đợi
        queue.append(a)
        visited[a] = True

        # Tìm đường tăng lưu lượng
        while queue:
            u = queue.pop(0)
            # Xét các đỉnh liền kề với u
            for ind, val in enumerate(self.dothi[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    P[ind] = u
                    if ind == z:
                        return True
        return False

    def luong_cuc_dai(self, a, z):
        # Lưu trữ đường đi nghịch
        P = [-1] * self.ROW
        f = 0  # Lưu lượng ban đầu bằng 0

        # Tăng lưu lượng khi có con đường từ a đến z
        while self.tang_luong(a, z, P):
            # Tìm lưu lượng con đường hiện tại
            flow = float("Inf")
            s = z
            while s != a:
                flow = min(flow, self.dothi[P[s]][s])
                s = P[s]

            # Cập nhật lưu lượng trên các cạnh
            v = z
            while v != a:
                u = P[v]
                self.dothi[u][v] -= flow
                self.dothi[v][u] += flow  # Cập nhật lưu lượng ngược
                v = P[v]

            f += flow

        return f

# Hàm bọc để chạy trong tiến trình
def run_graph(dothi, a, z):
    g = Graph(dothi)
    max_flow = g.luong_cuc_dai(a, z)
    print("Luong cuc dai la %d" % max_flow)
    return max_flow

# Ví dụ minh họa
dothi = [[0, 3, 5, 0, 0, 0],
         [0, 0, 2, 2, 0, 0],
         [0, 0, 0, 0, 2, 0],
         [0, 0, 0, 0, 0, 2],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

# Chạy trực tiếp
a = 0
z = 5
g = Graph(dothi)
print("Luong cuc dai la %d" % g.luong_cuc_dai(a, z))

# Chạy trong tiến trình
if __name__ == '__main__':
    p = Process(target=run_graph, args=(dothi, a, z))
    p.start()
    p.join()