import random
import string


def random_full_name() -> str:
    letters = random.choices(string.ascii_lowercase, k=6)
    word = "".join(ch.upper() if random.random() >= 0.5 else ch for ch in letters)
    number = str(random.randint(100, 999))
    return (word + number)[::-1]
