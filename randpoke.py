import random
import generate_data


pokemon_list = generate_data.generate_pokemon()

gen_dict = {"1": [0, 170], "2": [171, 270], "3": [271, 407], "4": [408, 514], "5": [515, 671], "6": [672, 743],
            "7": [744, 829],
            "8": [830, 912]}


def get_rand_poke(args):

    if len(args) == 0 or args[0] not in gen_dict:
        rand_poke_number = random.randint(0, 911)
        return pokemon_list[rand_poke_number]
    elif len(args) == 1 and args[0] in gen_dict:
        first = gen_dict[args[0]][0]
        last = gen_dict[args[0]][1]
        rand_poke_number = random.randint(first, last)
        return pokemon_list[rand_poke_number]
    else:
        return "This is not a valid input!"
