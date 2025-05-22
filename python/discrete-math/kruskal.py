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
    g = Graph(6)  # 6 vertices
    g.add_edge(0, 1, 10)  # 1-2
    g.add_edge(0, 3, 30)  # 1-4
    g.add_edge(0, 4, 45)  # 1-5
    g.add_edge(1, 2, 50)  # 2-3
    g.add_edge(1, 4, 40)  # 2-5
    g.add_edge(1, 5, 25)  # 2-6
    g.add_edge(2, 4, 35)  # 3-5
    g.add_edge(2, 5, 15)  # 3-6
    g.add_edge(3, 5, 20)  # 4-6
    g.add_edge(4, 5, 55)  # 5-6

    g.KruskalMST()
