import random
from typing import Union, Any


def number_random(maximum_number_integer_digits: int, maximum_number_float_digits: int,
                  minimum_number_integer_digits=0, minimum_number_float_digits=0):
    number_integer_digits = random.randint(minimum_number_integer_digits, maximum_number_integer_digits)
    number_float_digits = random.randint(minimum_number_float_digits, maximum_number_float_digits)
    if number_integer_digits == number_float_digits == 0:
        return 0
    elif number_float_digits == 0:
        _, __ = 10 ** (number_integer_digits - 1), 10 ** number_integer_digits - 1
        return random.randint(_, __)
    elif number_integer_digits == 0:
        _, __ = 10 ** (number_float_digits - 1), 10 ** number_float_digits - 1
        return random.randint(_, __) / (10 ** number_float_digits)
    else:
        _, __ = 10 ** (number_integer_digits - 1), 10 ** number_integer_digits - 1
        ___ = random.randint(_, __)
        _, __ = 10 ** (number_float_digits - 1), 10 ** number_float_digits - 1
        ____: Union[float, Any] = random.randint(_, __) / (10 ** number_float_digits)
        return ___ + ____
