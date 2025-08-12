class Calculator:
    """
    A simple calculator class that provides basic arithmetic operations:
    addition, subtraction, multiplication, division, and exponentiation.
    
    Each method takes two float values and returns a float result.
    """

    def add(self, a: float, b: float) -> float:
        """
        Add two numbers.

        Parameters:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The sum of a and b.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """
        Subtract the second number from the first.

        Parameters:
            a (float): The number to subtract from.
            b (float): The number to subtract.

        Returns:
            float: The result of a - b.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """
        Multiply two numbers.

        Parameters:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of a and b.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """
        Divide the first number by the second.

        Parameters:
            a (float): The numerator.
            b (float): The denominator.

        Returns:
            float: The result of a / b.

        Raises:
            ValueError: If b is zero, since division by zero is undefined.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def power(self, a: float, b: float) -> float:
        """
        Raise the first number to the power of the second.

        Parameters:
            a (float): The base.
            b (float): The exponent.

        Returns:
            float: The result of a raised to the power b (a ** b).
        """
        return a ** b
