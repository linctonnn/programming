def create_Mtx2D(row, col):
    Mtx = []  # Initialize an empty list to store rows of the matrix
    for i in range(row):
        row_list = []  # Create an empty list for the current row
        for j in range(col):
            value = int(input(f"Enter row: [{i + 1}] [{j + 1}]: "))
            row_list.append(value)  # Add the entered value to the row list
        Mtx.append(row_list)  # Add the row to the matrix
    return Mtx

# Main code
print("Enter first matrix: ")
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))
matrix = create_Mtx2D(rows, cols)

# Optionally, display the matrix
print("\nThe entered matrix is:")
for row in matrix:
    print(row)

