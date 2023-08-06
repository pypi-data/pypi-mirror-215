class Calculator:
    """
    A calculator class that performs basic mathematical operations.

    Attributes:
        memory (float): The current value stored in the calculator's memory.

    """

    def __init__(self):
        """
        Initialize a new Calculator object with memory set to 0.
        """
        self.memory = 0

    def add(self, x, y):
        """
        Add two numbers together.

        Args:
            x (float): The first number.
            y (float): The second number.

        Returns:
            float: The result of the addition.

        """
        return x + y

    def subtract(self, x, y):
        """
        Subtract one number from another.

        Args:
            x (float): The number to subtract from.
            y (float): The number to subtract.

        Returns:
            float: The result of the subtraction.

        """
        return x - y

    def multiply(self, x, y):
        """
        Multiply two numbers together.

        Args:
            x (float): The first number.
            y (float): The second number.

        Returns:
            float: The result of the multiplication.

        """
        return x * y

    def divide(self, x, y):
        """
        Divide one number by another.

        Args:
            x (float): The dividend.
            y (float): The divisor.

        Raises:
            ValueError: If the divisor is zero.

        Returns:
            float: The result of the division.

        """
        if y == 0:
            raise ValueError("Cannot divide by zero.")
        return x / y

    def root(self, x, y):
        """
        Calculate the y-th root of a number.

        Args:
            x (float): The number.
            y (float): The root.

        Raises:
            ValueError: If the number is negative and the root is even.

        Returns:
            float: The result of the root calculation.

        """
        if x < 0 and y % 2 == 0:
            raise ValueError("Cannot calculate even root of a negative number.")
        return x ** (1 / y)

    def reset (self):
        """
        Reset the calculator's memory value to 0.
        """
        self.memory = 0

