import sys
from pkg.calculator import Calculator
from pkg.render import render


def main():
    calculator = Calculator()

    # Show usage instructions if no expression is provided
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    # Join all command-line arguments to form the expression
    expression = " ".join(sys.argv[1:])

    try:
        # Evaluate the expression and render the result
        result = calculator.evaluate(expression)
        to_print = render(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()