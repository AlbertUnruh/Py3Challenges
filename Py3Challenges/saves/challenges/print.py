from ...challenge import Challenge


to_print = "Hello World!"

intro = f"You have to print {to_print!r}"


def validate_function(stdin: str, stdout: str, stderr: str, exc: tuple) -> bool:
    stdout = stdout.removesuffix("\n")
    return stdout == to_print


challenge = Challenge(
    intro=intro, validate_function=validate_function, capture_stdout=True
)
