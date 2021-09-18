import random


def random_boolean_value():
    if random.random() < 0.5:
        return "False"
    else:
        return "True"
