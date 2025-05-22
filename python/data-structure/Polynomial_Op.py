import array as arr

def create_poly(poly):
    while True:
        cof = int(input("Enter Coefficient: "))
        pwr = int(input("Enter Power: "))
        poly[pwr] = cof
        ch = input("Continue?(y/n): ")
        if ch.upper() == 'N':
            break

def display(poly):
    size = len(poly)
    for i in range(size-1, -1, -1):
        if poly[i] != 0:
            print(str(poly[i]) + "x^" + str(i), end="+")
    print("\b")

def add_poly(poly1, poly2):
    ln = len(poly1)
    poly3 = arr.array('i', [0]*ln)
    for i in range(ln):
        poly3[i] = poly1[i] + poly2[i]
    return poly3

p1 = int(input("Enter the highest power of 1st Polynomial: "))
p2 = int(input("Enter the highest power of 2nd Polynomial: "))
p = max(p1, p2)
poly1 = arr.array('i', [0]*(p+1))
poly2 = arr.array('i', [0]*(p+1))
print("Enter values for 1st Polynomial: ")
create_poly(poly1)
print("Enter values for 2nd Polynomial: ")
create_poly(poly2)
poly3 = add_poly(poly1, poly2)
print("\n1st Polynomial: ", end="")
display(poly1)
print("\n2nd Polynomial: ", end="")
display(poly2)
print("\nResult Polynomial: ", end="")
display(poly3)





      

        
