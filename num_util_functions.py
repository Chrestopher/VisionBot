import random


def random_linkcode():
    message = ""
    for i in range(8):
        if i == 4:
            message += " "

        message += str(random.randint(0, 9))

    print(message)
    return message
