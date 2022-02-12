__all__ = ("Challenge",)


import sys
from abc import ABC
from io import TextIOWrapper, BytesIO
from itertools import count
from types import TracebackType
from typing import (
    Callable,
    Iterator,
    Literal,
    Optional,
    Type,
)


_STD = Literal["in", "out", "err", "stdin", "stdout", "stderr"]
_EXC_TYPE = Optional[Type[BaseException]]
_EXC_VAL = Optional[BaseException]
_EXC_TB = Optional[TracebackType]
_EXC_tuple = tuple[_EXC_TYPE, _EXC_VAL, _EXC_TB]
_ValidateFunction = Callable[[str, str, str, _EXC_tuple], bool]


class STDCopy(TextIOWrapper):
    captured: str
    _std: _STD
    _sys_std: TextIOWrapper

    __slots__ = (
        "captured",
        "_std",
        "_sys_std",
    )

    def __init__(self, std: _STD, *args, **kwargs):
        if not std.startswith("std"):
            std = "std" + std
        self._std = std
        self._sys_std = getattr(sys, std.lower())
        self.captured = ""

        super().__init__(BytesIO(), *args, **kwargs)

    def write(self, s):
        ret = self._sys_std.write(s)
        self.captured += s
        return ret

    def read(self, size=-1):
        ret = self._sys_std.read(size)
        self.captured += ret
        return ret.removesuffix("\n")

    def __enter__(self):
        setattr(sys, self._std.lower(), self)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(sys, self._std.lower(), self._sys_std)
        return super().__exit__(exc_type, exc_val, exc_tb)


class Challenge(ABC):
    """
    The base for every challenge.
    """

    values: dict[str, ...]
    _intro: str
    _name: str
    _raise: bool
    _stdin: Optional[STDCopy]
    _stdout: Optional[STDCopy]
    _stderr: Optional[STDCopy]
    _val_func: _ValidateFunction
    __counter: Iterator[int] = count()

    __slots__ = (
        "values",
        "_intro",
        "_name",
        "_raise",
        "_stdin",
        "_stdout",
        "_stderr",
        "_val_func",
    )

    def __init__(
        self,
        intro: str,
        validate_function: _ValidateFunction,
        *,
        values: dict[str, ...] = None,
        name: str = None,
        # params for validation
        capture_stdin: bool = False,
        capture_stdout: bool = False,
        capture_stderr: bool = False,
        # params for behaviour
        do_raise: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        intro: str
            The intro which will be printed on __enter__.
        validate_function: _ValidateFunction
            The function which validates the output on __exit__.
        values: dict[str, ...]
            The values for the challenge.
        name: str
            The name for the challenge.
        capture_stdin: bool
            Whether to capture stdin or not.
        capture_stdout: bool
            Whether to capture stdout or not.
        capture_stderr: bool
            Whether to capture stderr or not.
        do_raise: bool
            Whether exceptions should be raised or not. If set to ``False`` the
            exception will only be printed into stderr, but won't crash the code.
        """
        self._intro = intro
        self._val_func = validate_function
        self.values = values.copy() if values is not None else {}

        many = next(self.__counter)
        self._name = name or f"Challenge {many}"

        if capture_stdin:
            import warnings

            warnings.warn(
                "Capturing sys.stdin is currently not possible! "
                "This option is automatically disabled.",
                RuntimeWarning,
            )
            capture_stdin = False

        self._stdin = STDCopy("stdin") if capture_stdin else None
        self._stdout = STDCopy("stdout") if capture_stdout else None
        self._stderr = STDCopy("stderr") if capture_stderr else None

        self._raise = do_raise

    def __enter__(self):
        if self._stdin is not None:
            self._stdin.__enter__()
        if self._stdout is not None:
            self._stdout.__enter__()
        if self._stderr is not None:
            self._stderr.__enter__()

        welcome = f"Welcome To {self.__class__.__name__}!"
        print(welcome)
        print("*" * len(welcome))
        print(self._intro)

    def __exit__(
        self,
        exc_type: _EXC_TYPE,
        exc_val: _EXC_VAL,
        exc_tb: _EXC_TB,
    ):
        exc = exc_type, exc_val, exc_tb

        stdin = ""
        if self._stdin is not None:
            stdin = self._stdin.captured
            self._stdin.__exit__(*exc)
        stdout = ""
        if self._stdout is not None:
            stdout = self._stdout.captured
            self._stdout.__exit__(*exc)
        stderr = ""
        if self._stderr is not None:
            stderr = self._stderr.captured
            self._stderr.__exit__(*exc)

        result = self._val_func(stdin, stdout, stderr, exc)
        if result:
            print("\n***********")
            print("You passed!")
        else:
            print("\n**********")
            print("Try again!")


def func(stdin, stdout, stderr, exc):
    print("*" * 50)
    print("stdin")
    print(stdin)
    print("*" * 50)
    print("stdout")
    print(stdout)
    print("*" * 50)
    print("stderr")
    print(stderr)
    print("*" * 50)
    print("exc")
    print(exc)
    return True


with Challenge(
    "Hello World!", func, capture_stdin=True, capture_stdout=True, capture_stderr=True
):
    pass
