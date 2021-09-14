import random


def create_russian_letters():
    a = ord('а')
    return [chr(i) for i in range(a, a + 32)], 31


def random_russian_word(maximum_length_word):
    length_word= random.randint(0, maximum_length_word)
    _, __ = create_russian_letters()
    b = ''
    return b.join([_[random.randint(0, __)] for i in range(0, length_word)])