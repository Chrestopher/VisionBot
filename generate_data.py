import os
import json

os_project_path = os.path.dirname(os.path.abspath(__file__))

if os.environ.get("bot_cli_key"):
    pass
    # os_project_path = os.path.join(os_project_path)


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
    file_path = os.path.join(os_project_path, 'content/pokemon/itemdex/itemdex_list.txt')
    item_list = []
    with open(file_path, 'r', encoding="ISO-8859-1") as f:
        for x in f:
            item_list.append(x.strip())

    return item_list


def generate_movedex_list():
    file_path = os.path.join(os_project_path, 'content/pokemon/movedex/moves_list.txt')
    move_list= []
    with open(file_path, 'r', encoding="ISO-8859-1") as f:
        for x in f:
            move_list.append(x.strip())

    return move_list


def generate_movedex_dictionary():
    file_path = os.path.join(os_project_path, 'content/pokemon/movedex/moves.json')
    with open(file_path, 'r', encoding="utf-8-sig") as f:
        return json.load(f)


def generate_itemdex_dictionary():
    file_path = os.path.join(os_project_path, 'content/pokemon/itemdex/itemdex_data.json')
    with open(file_path, 'r', encoding="utf-8-sig") as f:
        return json.load(f)


def generate_pokedex_dictionary():
    file_path = os.path.join(os_project_path, 'content/pokemon/pokedex/pokemon.json')
    with open(file_path, 'r', encoding="utf-8-sig") as f:
        return json.load(f)


