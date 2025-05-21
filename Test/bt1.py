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

    def timduongdi(self, a):
        L = [sys.maxsize] * self.dinh_x
        P = [False] * self.dinh_x
        L[a] = 0
        for count in range(self.dinh_x):
            u = self.duongdinhonhat(L, P)
            P[u] = True
            for x in range(self.dinh_x):
                if (self.graph[u][x] > 0 and not P[x] and L[x] > L[u] + self.graph[u][x]):
                    L[x] = L[u] + self.graph[u][x]
        self.inkettqua(L, a)

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

    g.timduongdi(0)