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


def convert_meters_to_feet_inches(value):
    value = float(value)
    inches = value * 39.37
    feet = int(inches / 12)
    inches = int(round(inches % 12, 0))
    return str(feet) + "'" + str(inches) + '"'


def convert_kilograms_to_lbs(value):
    value = float(value)
    lbs = round(value * 2.205, 1)
    return str(lbs) + " lbs"
