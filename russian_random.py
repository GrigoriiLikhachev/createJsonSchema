import random


def createRussinaLetters():
    a = ord('а')
    return [chr(i) for i in range(a, a + 32)], 31


def randomRussianWord(maximumLengthWord):
    lenghtWord = random.randint(0, maximumLengthWord)
    _, __ = createRussinaLetters()
    b = ''
    return b.join([_[random.randint(0, __)] for i in range(0, lenghtWord)])