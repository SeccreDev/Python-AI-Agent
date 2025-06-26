def render(expression, result):
    """
    Render a styled box displaying the expression and its result.

    Args:
        expression (str): The mathematical expression as a string.
        result (float or int): The computed result of the expression.

    Returns:
        str: A formatted string displaying the expression and result inside a box.
    """
    # Convert result to integer string if it is a whole number
    if isinstance(result, float) and result.is_integer():
        result_str = str(int(result))
    else:
        result_str = str(result)

    # Determine the width of the box based on the longest line
    box_width = max(len(expression), len(result_str)) + 4

    box = []
    box.append("┌" + "─" * box_width + "┐")
    box.append("│" + " " * 2 + expression + " " * (box_width - len(expression) - 2) + "│")
    box.append("│" + " " * box_width + "│")
    box.append("│" + " " * 2 + "=" + " " * (box_width - 3) + "│")
    box.append("│" + " " * box_width + "│")
    box.append("│" + " " * 2 + result_str + " " * (box_width - len(result_str) - 2) + "│")
    box.append("└" + "─" * box_width + "┘")
    return "\n".join(box)