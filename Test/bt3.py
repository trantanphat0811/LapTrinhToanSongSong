xxfrom threading import Thread
import sys

class Graph:
    def __init__(self, dinh):
        self.dinh_x = dinh
        self.graph = [[0 for column in range(dinh)] for row in range(dinh)]

    def inkettqua(self, L, a):
        print("Dinh nguon xuat phat tu:", a)
        for nut in range(self.dinh_x):
            print(f"a, 'den dinh', nut, 'do dai duong di la:', L[nut]")

    def duongdinhonhat(self, L, P):
        min = sys.maxsize
        for x in range(self.dinh_x):
            if L[x] < min and not P[x]:
                min = L[x]
                min_index = x
        return min_index

    def timduongdi(self, a, L, P):
        L[a] = 0
        for count in range(self.dinh_x):
            u = self.duongdinhonhat(L, P)
            P[u] = True
            for x in range(self.dinh_x):
                if (self.graph[u][x] > 0 and not P[x] and L[x] > L[u] + self.graph[u][x]):
                    L[x] = L[u] + self.graph[u][x]

# Hàm bọc để chạy trong luồng
def run_graph(g, a, L, P):
    g.timduongdi(a, L, P)
    g.inkettqua(L, a)

# Ví dụ sử dụng
if __name__ == '__main__':
    g = Graph(8)
    g.graph = [
        [0, 2, 0, 5, 0, 0, 0, 0],  # 0
        [0, 0, 3, 0, 8, 0, 0, 0],  # 1
        [0, 0, 0, 1, 0, 6, 0, 0],  # 2
        [0, 0, 0, 0, 6, 0, 5, 0],  # 3
        [0, 0, 0, 0, 0, 2, 0, 9],  # 4
        [0, 0, 0, 0, 0, 0, 2, 3],  # 5
        [0, 0, 0, 0, 0, 0, 0, 3],  # 6
        [0, 0, 0, 0, 0, 0, 0, 0]   # 7
    ]

    # Khởi tạo mảng khoảng cách và tập hợp đỉnh đã xử lý
    L = [sys.maxsize] * g.dinh_x
    P = [False] * g.dinh_x

    # Tạo và chạy luồng
    t = Thread(target=run_graph, args=(g, 0, L, P))
    t.start()
    t.join()