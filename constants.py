from enum import Enum

replace_values = {"g'": "gʻ", "o'": "oʻ", "G'": "Gʻ", "O'": "Oʻ"}


class Sex(Enum):
    GIRL = 1
    BOY = 2
    OTHER = 3
