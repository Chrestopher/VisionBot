def generate_joe():
    joe_messages = []
    with open("botrepo.txt", 'r', encoding="utf-8-sig") as f:
        for x in f:
            joe_messages.append(x.strip())
    return joe_messages


def generate_pokemon():
    pokemon_list = []
    with open("pokemon_list.txt", 'r', encoding="utf-8-sig") as f:
        for x in f:
            pokemon_list.append(x.strip())

    return pokemon_list


def generate_itemdex_list():
    pokemon_list = []
    with open("content/pokemon/itemdex/itemdex_dictionary.txt", 'r') as f:
        for x in f:
            pokemon_list.append(x.strip())

    return pokemon_list
