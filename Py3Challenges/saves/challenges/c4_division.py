"""
To master this you should consider using the ``/``-operator.
"""
from ...challenge import Challenge
from random import randint


x = randint(1, 100)
y = randint(1, 100)

intro = f"You have to print the quotient of {x} and {y}. (values: x, y)"


def validate_function(stdin: str, stdout: str, stderr: str, exc: tuple) -> bool:
    try:
        z = float(stdout.removesuffix("\n"))
    except ValueError:
        return False
    else:
        return (x / y) == z


challenge = Challenge(
    intro=intro,
    validate_function=validate_function,
    help=__doc__,
    values={"x": x, "y": y},
    capture_stdout=True,
)
