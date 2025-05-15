from multiprocessing import Process
import sys

class Graph:
    def __init__(self, cung, dinh):
        self.cung_x = dinh
        self.cung_graph = [[0 for column in range(dinh)] for row in range(dinh)]

    def inkettqua(self, cung, L, a):
        print("Dinh nguon xuat phat tu:", a)
        for nut in range(self.cung_x):
            print(f"a, 'den dinh', nut, 'do dai duong di la:', L[nut]")

    def duongdinhonhat(self, cung, L, P):
        min = sys.maxsize
        for x in range(self.cung_x):
            if L[x] < min and P[x] == False:
                min = L[x]
                min_index = x
        return min_index

    def timduongdi(self, cung, a):
        L = [sys.maxsize] * self.cung_x
        P = [False] * self.cung_x
        L[a] = 0
        for count in range(self.cung_x):
            u = self.duongdinhonhat(L, P)
            P[u] = True
            for x in range(self.cung_x):
                if (self.cung_graph[u][x] > 0 and P[x] == False and L[x] > L[u] + self.cung_graph[u][x]):
                    L[x] = L[u] + self.cung_graph[u][x]
        self.inkettqua(L, a)

# Ví dụ sử dụng
if __name__ == '__main__':
    g = Graph(6)
    g.cung_graph = [
        [0, 1, 3, 0, 0, 0],
        [0, 0, 5, 0, 0, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0]
    ]

    p = Process(target=Graph.timduongdi, args=(g, 0,))
    p.start()
    p.join()