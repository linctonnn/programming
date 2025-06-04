class Point:
    def __init__(self, row = 0, col = 0):
        self.row = row
        self.col = col
    
    # Tambahan
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

class Stack:
    def __init__(self, capacity):
        self.items = [None] * capacity
        self.top = -1
    
    def is_empty(self):
        return self.top == -1
    
    def push(self, item):
        self.top += 1
        self.items[self.top] = item

    def pop(self):
        if self.is_empty():
            print("Stack is empty")
            exit(1)
        item = self.items[self.top]
        self.top -= 1
        return item

class Maze:
    ROWS = 15
    COLS = 15

    def __init__(self):
        self.stack = Stack(self.ROWS * self.COLS)
        self.matrix = [
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        ]

    def can_move(self, row, col):
        return (0 <= row < self.ROWS and 
                0 <= col < self.COLS and 
                self.matrix[row][col] == 0)
    
    def print_maze(self):
        for row in self.matrix:
            print(" ".join(str(cell) for cell in row))
    
    def solve(self, row, col):
        if row == self.ROWS -1 and col == self.COLS -1:
            self.stack.push(Point(row, col))
            return 1
        
        if self.can_move(row, col):
            self.stack.push(Point(row, col))
            self.matrix[row][col] = 1

            if self.solve(row, col + 1) == 1:
                return 1
            if self.solve(row + 1, col) == 1:
                return 1
            if self.solve(row, col -1) == 1:
                return 1
            if self.solve(row - 1, col) == 1:
                return 1
            
            self.stack.pop()
            self.matrix[row][col] = 0
            return 0
        return 0

    # Tambahan
    def print_maze_with_path(self, path_points):
        visual = []
        for r in range(self.ROWS):
            row_visual = []
            for c in range(self.COLS):
                if Point(r, c) in path_points:
                    row_visual.append('✱')
                elif self.matrix[r][c] == 1:
                    row_visual.append('■')
                else:
                    row_visual.append('□')
            visual.append(" ".join(row_visual))
        for row in visual:
            print(row)


if __name__ == "__main__":
    maze = Maze()
    maze.print_maze()
    
    print("\nSolving...\n")
    if maze.solve(0, 0) == 1:
        print("Path found!\n")

        # Ambil path dari stack ke list biar ga ilang
        path = []
        while not maze.stack.is_empty():
            point = maze.stack.pop()
            path.append(point)
        
        path.reverse()  # Biar dari start ke goal
        print("Maze with solution path:\n")
        maze.print_maze_with_path(path)

        print("\nPath coordinates:")
        for p in path:
            print(f"({p.row}, {p.col})")
    else:
        print("No path found.")
