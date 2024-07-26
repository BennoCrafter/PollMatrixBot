import random

invisible_char = '\u200B'


def insert_invisible_char(name):
  position = len(name) // 2

  # Insert the invisible character at the chosen position
  new_name = name[:position] + invisible_char + name[position:]

  return new_name
