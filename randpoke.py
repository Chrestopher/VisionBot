import random

gen_dict = {"1": [0, 170], "2": [171, 270], "3": [271, 407], "4": [408, 514], "5": [515, 671], "6": [672, 743],
            "7": [744, 829],
            "8": [830, 912]}


def get_rand_poke(message, pokelist):
    if len(message) == 9:
        rand_poke_number = random.randint(0, 911)
        print(pokelist[rand_poke_number])
        return pokelist[rand_poke_number]

    gen = message[10]
    if gen not in gen_dict:
        rand_poke_number = random.randint(0, 911)
        print(pokelist[rand_poke_number])
        return pokelist[rand_poke_number]
    else:
        first = gen_dict[gen][0]
        last = gen_dict[gen][1]
        rand_poke_number = random.randint(first, last)
        return pokelist[rand_poke_number]
