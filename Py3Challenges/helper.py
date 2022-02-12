r"""
Notes
-----
It would be best if you import this project as ``Py3C``.
(``import Py3Challenges as Py3C``)

Getting Started
---------------
First you have to get your challenge.
Go get them you can use ``Py3C.get_challenge(name_o_id)``
where ``name_o_id`` is the name of the challenge or the
numeric id (in the order in which the< where loaded).

Then you can use following code-structure to make the
challenges:

>>> import Py3Challenges as Py3C
... challenge = Py3C.get_challenge(0)  # the "print"-challenge
... with challenge:
...     # do whatever you want inside here to complete the challenge
...     pass

Sometimes the challenges also provides the argument
``values`` which is an instance of ``dict``.

They can be accessed using ``my_dictionary["key"]``.
A short example on a challange:

>>> import Py3Challenges as Py3C
... challenge = Py3C.get_challenge(1)  # the "addition"-challenge
... x = challenge.values["x"]
... y = challenge.values["y"]
... with challenge:
...     # do whatever you want inside here to complete the challenge
...     pass

Getting Help
------------
You should try the method ``challenge.get_help()``. If this
doesn't help you feel free to open an issue over on GitHub
(https://github.com/AlbertUnruh/Py3Challenges/issues).
"""


__all__ = (
    "get_help",
    "getting_started",
)


from .challenge import get_challenge


def get_help(
    name_o_id,
    /,
) -> str:
    """
    Prints the help into the terminal.

    Parameters
    ----------
    name_o_id: str, int
        The name or ID from the challenge.

    Returns
    -------
    str
        The help provided by the challenge.
    """
    help = get_challenge(name_o_id).help  # noqa
    print(help)
    return help


def getting_started() -> str:
    """
    Prints everything you need to know to start.

    Returns
    -------
    str
        The string which was printed.
    """
    print(__doc__)
    return __doc__
