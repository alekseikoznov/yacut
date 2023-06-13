from random import choice
from re import match
from string import ascii_letters, digits

from .models import URLMap


def get_unique_short_id():
    letters = ascii_letters + digits
    while True:
        random_link = ''.join(choice(letters) for i in range(6))
        if URLMap.query.filter_by(short=random_link).first() is None:
            break
    return random_link


def correct_short(short):
    pattern = "^[A-Za-z0-9]*$"
    return bool(match(pattern, short))
