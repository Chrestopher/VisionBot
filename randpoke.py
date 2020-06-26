import random


import generate_data


pokemon_list = generate_data.generate_pokemon()

gen_dict = {"1": [0, 170], "2": [171, 270], "3": [271, 407], "4": [408, 514], "5": [515, 671], "6": [672, 743],
            "7": [744, 829],
            "8": [830, 912]}


def get_rand_poke(message, pokelist):
    gentest = message.split()
    if len(gentest) == 1 or gentest[1] not in gen_dict:
        rand_poke_number = random.randint(0, 911)
        print(pokelist[rand_poke_number])
        return pokelist[rand_poke_number]
    elif len(gentest) == 2 and gentest[2] in gen_dict:
        first = gen_dict[gentest[1]][0]
        last = gen_dict[gentest[1]][1]
        rand_poke_number = random.randint(first, last)
        return pokelist[rand_poke_number]
    else:
        return "This is not a valid input!"

4