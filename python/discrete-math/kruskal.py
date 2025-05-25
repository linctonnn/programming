class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def KruskalMST(self):
        result = []
        i = 0
        e = 0

        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = [i for i in range(self.V)]
        rank = [0] * self.V

        while e < self.V - 1 and i < len(self.graph):
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        # Sort result by weight
        result.sort(key=lambda x: x[2])
        total_weight = sum([w for _, _, w in result])

        print("Alur Penyelesaian dengan Algoritma Kruskal")
        for u, v, w in result:
            print(f"{u+1} - {v+1} \tweight: {w}")
        print(f"Total weight = {total_weight}")


if __name__ == '__main__':
    # A=0, B=1, C=2, D=3, E=4, F=5, G=6
    g = Graph(7)  # 7 vertices
    g.add_edge(0, 1, 7) 
    g.add_edge(0, 3, 5)
    g.add_edge(1, 2, 8)
    g.add_edge(1, 3, 9)
    g.add_edge(1, 4, 7)
    g.add_edge(2, 4, 5)
    g.add_edge(3, 4, 15)
    g.add_edge(3, 5, 6)
    g.add_edge(4, 5, 8)
    g.add_edge(4, 6, 9)
    g.add_edge(4, 6, 11)
    g.KruskalMST()
