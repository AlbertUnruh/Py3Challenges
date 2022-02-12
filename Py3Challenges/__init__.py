__author__ = "AlbertUnruh"
__url__ = "https://github.com/AlbertUnruh/Py3Challenges"
__license__ = "MIT"
__copyright__ = f"(c) 2022 - present {__author__}"
__version__ = "1.0.1"
__description__ = "A collection of challenges for programming beginners."


from . import helper
from . import challenge

from .helper import *
from .challenge import *


all_challenges: list[Challenge] = load_challenges()
