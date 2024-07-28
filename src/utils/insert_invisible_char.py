import random
from src.const import INVISIBLE_CHAR


def insert_invisible_char(name):
    position = len(name) // 2

    # Insert the invisible character at the chosen position
    new_name = name[:position] + INVISIBLE_CHAR + name[position:]

    return new_name
