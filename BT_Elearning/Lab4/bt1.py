from multiprocessing import Process
from   collections import defaultdict

class Graph:
    def __init__ (self, dothi):
        self.dothi = dothi
        self.row= len(dothi)
        
    def tang_luong (self,a,z,p):
        visited =[False]*[self.row]
        queue= []
        queue.append(a)
        visited[a]=True
        while queue: 
            u =queue.pop(0)
                
        for ind , val in enumerate (self.dothi[u]):
            if (visited [ind]== False and val >0):
                queue.append(ind)
                visited[ind]= True 
                p[ind]=u
                if (ind == z):
                    return True
        return False
    def luong_cuc_dai (self, a,z)
        p = [1]*(self*row)
        f=0
        while self.tang_luong(a,z,p):
            flow = float ('inf')
            s=z
            while (s!=a):
                flow = min (flow, self.dothi[p[s][s]])
                s=p[s]
            f += flow
            while (v! =a ):
                u = p[v]
                self.dothi[u][v] -= flow 
                self.dothi[u][v] += flow
                v= p[v]
        return f
dothi = [[0,3,5,0,0,0],
         [0,0,0,2,0,0],
         [0,0,0,2,0,0],
         [0,0,0,0,0,4],
         [0,0,0,0,0,4],
         [0,0,0,0,0,0]]
g= Graph (dothi)
a= 0, z= 5
print ("luong cuc dai la %d" % g.luong_cuc_dai(a,z))

if __name__ == "__main__":
    p= Process(target = Graph,args=(g,))
    p.start()
    p.join()