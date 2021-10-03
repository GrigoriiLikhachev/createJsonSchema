import random


def calculate_key(_, __):
    array_for_key_computation = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    key_summa = 0
    for ___ in __:
        key_summa += int(___) * array_for_key_computation[_]
        _ += 1
    ____ = key_summa - (key_summa // 11) * 11
    if ____ < 10:
        __.append(str(____))
    else:
        __.append(str(____ - (____ // 10) * 10))
    return __


def create_inn_without_keys(_):
    __ = []
    for i in range(0, _):
        __.append(str(random.randint(0, 9)))
    return __


def create_russian_random_inn(characters=10):
    """
    :param characters: 10 - organization, 12 - IP
    :return: valid inn
    """
    if characters == 10:
        valid_inn = calculate_key(2, create_inn_without_keys(9))
    else:
        valid_inn = calculate_key(0, calculate_key(1, create_inn_without_keys(10)))
    return ''.join(valid_inn)
