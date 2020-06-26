import os

os_project_path = os.path.dirname(os.path.abspath(__file__)).replace("/", "\\")


def generate_joe():
    file_path = os.path.join(os_project_path, 'botrepo.txt')
    joe_messages = []
    with open(file_path, 'r', encoding="utf-8-sig") as f:
        for x in f:
            joe_messages.append(x.strip())
    return joe_messages


def generate_pokemon():
    file_path = os.path.join(os_project_path, 'pokemon_list.txt')
    pokemon_list = []
    with open(file_path, 'r', encoding="utf-8-sig") as f:
        for x in f:
            pokemon_list.append(x.strip())

    return pokemon_list


def generate_itemdex_list():
    file_path = os.path.join(os_project_path, 'content\\pokemon\\itemdex\\itemdex_dictionary.txt')
    item_list = []
    with open(file_path, 'r', encoding="ISO-8859-1") as f:
        for x in f:
            item_list.append(x.strip())

    return item_list

