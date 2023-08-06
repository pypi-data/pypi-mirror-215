import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculator.calculator import Calculator

def perform_calculations(x, y):
    calc = Calculator()

    print(f"Test: x={x} & y={y}")

    result = calc.add(x, y)
    print(f"Addition: {x} + {y} = {result}")

    result = calc.subtract(x, y)
    print(f"Subtraction: {x} - {y} = {result}")

    result = calc.multiply(x, y)
    print(f"Multiplication: {x} * {y} = {result}")

    try:
        result = calc.divide(x, y)
        print(f"Division: {x} / {y} = {result}")
    except ValueError:
        print("ValueError: Cannot divide by zero.")

    if y != 0:
        if x == 0 and y < 0:
            print("Cannot calculate even root of zero.")
        else:
            try:
                result = calc.root(x, y)
                print(f"{y} Root of {x}: {result}")
            except ValueError:
                print("ValueError: Cannot calculate even root of a negative number.")
    else:
        print(f"Cannot calculate {y} Root of {x}")

    print(f"Calculator Memory: {calc.memory}")

class CalculatorTest(unittest.TestCase):
    """
    Unit tests for the Calculator class.
    """

    def test_calculations(self):
        perform_calculations(16, 4)
        perform_calculations(-16, -4)
        perform_calculations(16, -4)
        perform_calculations(-16, 4)
        perform_calculations(16, 0)
        perform_calculations(-16, 0)
        perform_calculations(0, 4)
        perform_calculations(0, -4)
        perform_calculations(0, 0)
        perform_calculations(16, float('inf'))
        perform_calculations(-16, float('inf'))
        perform_calculations(float('inf'), 4)
        perform_calculations(float('inf'), -4)
        perform_calculations(float('inf'), float('inf'))

if __name__ == '__main__':
    unittest.main()
