"""
To master this you should consider using the builtin-``sum``-function.
"""
from ...challenge import Challenge
from random import randint


x = []
for _ in range(randint(2, 10)):
    x.append(randint(1, 100))

intro = f"You have to print the sum of {', '.join(str(_) for _ in x[:-1])} and {x[-1]}."


def validate_function(stdin: str, stdout: str, stderr: str, exc: tuple) -> bool:
    try:
        z = int(stdout.removesuffix("\n"))
    except ValueError:
        return False
    else:
        return sum(x) == z


challenge = Challenge(
    intro=intro,
    validate_function=validate_function,
    help=__doc__,
    values={"x": x},
    capture_stdout=True,
)
