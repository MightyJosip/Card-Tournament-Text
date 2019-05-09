import os


def clear_screen() -> None:
    """
Delete everything on the screen
    """
    os.system('cls')


def full_line(character: str, size: int) -> str:
    """
Make full line out of a single character; for example full_line('-', 10) will return ----------
    """
    return character * size


def center_line(text: str, size: int, character: str = ' ') -> str:
    """
Return the text that between the character based on the size
    """
    return text.center(size, character)
