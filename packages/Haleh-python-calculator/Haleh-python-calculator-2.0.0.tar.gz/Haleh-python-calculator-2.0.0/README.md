# Python Calculator Package

The Python Calculator package is a lightweight and easy-to-use module that provides basic calculator functionality for performing mathematical operations in Python. It offers a convenient way to perform addition, subtraction, multiplication, division, root calculations, and memory management.

This package is designed to be beginner-friendly and aims to simplify common mathematical calculations within Python scripts or applications. Whether you're working on a simple script or a complex data analysis project, the Python Calculator package can be a valuable tool for performing calculations efficiently.

This package provides a basic calculator module that allows you to perform mathematical operations. It includes the `Calculator` class, which can add, subtract, multiply, divide, take roots, and reset its memory value.

## Key Features

- Addition and subtraction operations
- Multiplication and division operations
- Nth root calculations
- Memory management to store and reset calculator values

## Installation

To use the Python Calculator package, follow these steps:

1. Clone the repository to your local machine:
git clone https://github.com/TuringCollegeSubmissions/hkafas-DWWP.1.git

2. Navigate to the project directory:
cd hkafas-DWWP.1

3. Install the package using pip:
pip install hkafas-DWWP.1


## Usage

Using the Python Calculator package is straightforward. Here's an example of how to perform basic calculations:

1. Import the `Calculator` class from the `calculator` module:
```python
from calculator.calculator import Calculator

1.Create an instance of the Calculator class:
calc = Calculator()

2.Perform mathematical operations by calling the appropriate methods on the Calculator instance. For example:
Add numbers to the calculator's memory:
calc.add(5)
calc.add(3)
Subtract a number from the calculator's memory:
calc.subtract(2)
Multiply the calculator's memory by a number:
calc.multiply(4)
Divide the calculator's memory by a number:
calc.divide(2)
Take the square root of the calculator's memory:
calc.root(2)
Reset the calculator's memory value to 0:calc.reset()
calc.reset()
Access the final result from the calculator's memory:
print(calc.memory)  # Output: 0.0

Note: All methods accept numeric values as arguments. The parameters are positional arguments.

Usage Notes:

Division: If the divisor is 0, a ZeroDivisionError will be raised. Handle this exception to prevent program crashes.
Root Calculation: The root calculation only works with positive numbers. If a negative number is provided as the base and the root is an even number, a ValueError will be raised. Handle this exception accordingly.
For more detailed information about the class and its methods, refer to the calculator/calculator.py file.

Contribution
Contributions to the Python Calculator package are welcome! To contribute, follow these steps:

1.Clone the repository to your local machine:
git clone https://github.com/TuringCollegeSubmissions/hkafas-DWWP.1.git

2.Set up a development environment. You may want to create a virtual environment and install the necessary dependencies.

3.Run tests to ensure everything is functioning correctly. Instructions for running tests can be found in the project's documentation or README file.

4.Make your desired changes, add features, fix bugs, etc.

5.Submit a pull request on the GitHub repository. Please provide a clear description of your changes and the problem it solves.

Please follow the coding conventions and guidelines specified in the project's documentation.

License
The Python Calculator package is released under the MIT License. See the LICENSE file for more information.

We hope you find the Python Calculator package helpful for your mathematical calculations. Happy coding!

In this updated version, the README file includes examples for each method, clarifies the parameter usage, provides usage notes for specific scenarios, ensures formatting and consistency, corrects installation instructions, includes a link to the source code, improves contribution guidelines, and adds license information. These changes aim to provide more clarity and completeness to the README file.

