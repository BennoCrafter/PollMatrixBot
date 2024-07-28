INVISIBLE_CHAR = "\u200B"

def insert_invisible_char(name):
    """Insert the invisible character in the middle of the name."""
    position = len(name) // 2

    new_name = name[:position] + INVISIBLE_CHAR + name[position:]

    return new_name
