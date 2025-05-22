def create_Mtx2D(row, col):
    mtx = []
    for i in range(row): 
        rw = []
        for j in range(col):
            m = i + 1
            n = j + 1
            element = int(input("Enter [" + str(m)  + "][" + str(n) + "]: "))
            rw.append(element)
        mtx.append(rw) 
    return mtx

def print_Mtx2D(mtx):
    for row in mtx:
        print(row)

def add_Mtx2D(mtx1, mtx2):
    rw, cl = (len(mtx1), len(mtx1[0]))
    mtx = [[0]* cl]*rw
    mtx = [[mtx1[i][j] + mtx2[i][j] for j in range(cl)]for i in range(rw)]
    return mtx

    

row = int(input("Enter number of rows: "))
col = int(input("Enter number of columns: "))
print("Enter First Matrix: ")
mtx1 = create_Mtx2D(row, col)
print("Enter Second Matrix: ")
mtx2 = create_Mtx2D(row, col)
print("First Matrix: ")
print_Mtx2D(mtx1)
print("Second Matrix: ")
print_Mtx2D(mtx2)
mtx = add_Mtx2D(mtx1,mtx2)
print("Result Matrix: ")
print_Mtx2D(mtx)
