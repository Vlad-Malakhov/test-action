def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        print("Error: Cannot divide by zero.")
        return None
    return a / b

if __name__ == "__main__":
    print("Simple Calculator")

    num1 = input("Enter first number: ")
    num2 = input("Enter second number: ")
    operation = input("Enter operation (+, -, *, /): ")

    num1 = float(num1)
    num2 = float(num2)

    if operation == "+":
        result = add(num1, num2)
    elif operation == "-":
        result = subtract(num1, num2)
    elif operation == "*":
        result = multiply(num1, num2)
    elif operation == "/":
        result = divide(num1, num2)
    else:
        print("Invalid operation.")
        result = None

    if result is not None:
        print("Result:", result)