
print("===== SIMPLE CALCULATOR =====")

while True:
    print("\n1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "5":
        print("Calculator closed.")
        break

    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice!")
        continue

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input! Enter numbers only.")
        continue

    if choice == "1":
        result = num1 + num2
        operation = "Addition"
    elif choice == "2":
        result = num1 - num2
        operation = "Subtraction"
    elif choice == "3":
        result = num1 * num2
        operation = "Multiplication"
    else:
        if num2 == 0:
            print("Error: Cannot divide by zero!")
            continue
        result = num1 / num2
        operation = "Division"

    print(f"{operation} Result: {result:g}")
