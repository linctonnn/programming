import heapq

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def prim_mst(self):
        pq = []
        src = 0
        key = [float('inf')] * self.V
        parent = [-1] * self.V
        in_mst = [False] * self.V
        heapq.heappush(pq, (0, src))
        key[src] = 0

        while pq:
            u = heapq.heappop(pq)[1]

            if in_mst[u]:
                continue
            in_mst[u] = True

            for v, weight in self.adj[u]:
                if not in_mst[v] and key[v] > weight:
                    key[v] = weight
                    heapq.heappush(pq, (key[v], v))
                    parent[v] = u

        # Collect MST edges
        mst_edges = []
        total_weight = 0

        for i in range(1, self.V):
            u, v, w = parent[i], i, key[i]
            # Convert to 1-based indexing for readability
            mst_edges.append((u + 1, v + 1, w))
            total_weight += w

        # Sort by weight
        mst_edges.sort(key=lambda x: x[2])

        print("Alur Penyelesaian dengan Algoritma Prim")
        for u, v, w in mst_edges:
            print(f"{u} - {v} \tweight: {w}")
        print(f"Total weight = {total_weight}")  # 1-based for readability
        
if __name__ == "__main__":
    V = 8
    g = Graph(V)
    # A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7
    g.add_edge(0, 1, 40)   # A-B
    g.add_edge(0, 2, 15)   # A-C
    g.add_edge(0, 3, 35)   # A-D 
    g.add_edge(1, 4, 25)   # A-D 
    g.add_edge(2, 3, 45)   # A-D 
    g.add_edge(3, 4, 30)   # A-D 
    g.add_edge(4, 5, 48)   # A-D 
    g.add_edge(4, 6, 50)   # A-D 
    g.add_edge(3, 7, 20)   # A-D 
    g.add_edge(7, 6, 14)   # A-D 
    g.add_edge(5, 6, 10)   # A-D 

    g.prim_mst()

