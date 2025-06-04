
class Stack:
    def __init__(self):
        self.items = []

    def push(self, c):
        self.items.append(c)

    def pop(self):
        if self.is_empty():
            print("Stack is empty")
            exit(1)
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

class SyntaxChecker:
    def check_balanced(filename):
        try:
            with open(filename, 'r') as file:
                stack = Stack()
                while True:
                    c = file.read(1)
                    if not c:
                        break
                    if c in '([{':
                        stack.push(c)
                    elif c in ')]}':
                        if stack.is_empty():
                            return 0
                        opening_ch = stack.pop()
                        if (c == ')' and opening_ch != '(') or (c == ']' and opening_ch != '[') or (c == '}' and opening_ch != '{'):
                            return 0
                return 1 if stack.is_empty() else 0
        except IOError as e:
            print(e)
            return 0

    def main():
        try:
            filename = input("Path to the source file: ")
            if SyntaxChecker.check_balanced(filename) == 1:
                print("The input file is balanced")
            else:
                print("The input file is not balaned")
        except IOError as e:
            print(e)

if __name__ == "__main__":
    SyntaxChecker.main()
