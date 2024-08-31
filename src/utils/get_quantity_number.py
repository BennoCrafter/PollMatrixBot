import re


def get_quantity_number(s) -> tuple[int, str]:
    # Check if the string starts with a number followed by 'x' and a ' '
    match = re.match(r'^(\d+)x ', s)
    if match:
        return int(match.group(1)), str(s[match.end():]).strip()
    return 0, s


if __name__ == "__main__":
    print(get_quantity_number("2x pizza hawaii"))
