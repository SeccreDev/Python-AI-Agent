class Calculator:
    def __init__(self):
        """Initialize operator functions and their precedence levels."""
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        """
        Evaluate a string mathematical expression in infix notation.

        Args:
            expression (str): The input mathematical expression (e.g., "3 + 10 * 2").

        Returns:
            float or None: The result of the evaluation or None if expression is empty.
        """
        if not expression or expression.isspace():
            return None

        # Split the expression into tokens based on whitespace  
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        """
        Evaluate a list of tokens using the shunting-yard algorithm.

        Args:
            tokens (List[str]): A list of tokens from the expression.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid or contains unknown tokens.
        """
        values = [] # Stack to store numbers
        operators = [] # Stack to store operators

        for token in tokens:
            if token in self.operators:
                # Pop operators with higher or equal precedence
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")

        # Apply any remaining operators
        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        """
        Apply the operator at the top of the stack to the top two values.

        Args:
            operators (List[str]): Stack of operators.
            values (List[float]): Stack of values.

        Raises:
            ValueError: If there are not enough operands for the operator.
        """
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"Not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()

        # Apply the operator and push the result onto the value stack
        values.append(self.operators[operator](a, b))