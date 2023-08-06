from typing import List, Tuple


def replace_pair(text: str, pairs: List[Tuple[str]]) -> str:
    for char in pairs:
        text = text.replace(char[0], char[1])
    return text
