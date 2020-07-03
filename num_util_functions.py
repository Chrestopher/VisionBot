import random


def coin_flip():
    flip = random.randint(1, 1000)
    if flip > 500:
        return "heads"
    else:
        return "tails"


def random_linkcode():
    message = ""
    for i in range(8):
        if i == 4:
            message += " "

        message += str(random.randint(0, 9))

    print(message)
    return message
