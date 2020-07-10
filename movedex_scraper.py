import json

import requests
from bs4 import BeautifulSoup

import generate_data
import movedex_help

movedex_url_prefix = "https://www.serebii.net/attackdex-swsh/"
movedex_url_postfix = ".shtml"
movedex_list = generate_data.generate_movedex_list()
# movedex_dictionary= generate_data.generate_movedex_dictionary()

moves_list_manual_fix = []


def write_move_names_to_file():
    r = requests.get('https://www.serebii.net/attackdex-swsh/')
    soup = BeautifulSoup(r.text, 'html.parser')
    moveslist = []
    moveslist_manual_entry = []
    for option in soup.find_all('option'):
        f = option.text
        if 'AttackDex' not in f and f not in moveslist:
            moveslist.append(f)
    f = open('content/pokemon/movedex/moves_list.txt', 'a')
    for move in moveslist:
        f.write(move + '\n')
    f.close()


def scrape_move(item_name):
    movesdict = {}
    url = movedex_url_prefix + ''.join(item_name.lower().rsplit()) + movedex_url_postfix
    moverequest = requests.get(url)
    if moverequest.status_code == 404:
        return "could not find move"
    soup = BeautifulSoup(moverequest.text, 'html.parser')
    maintable = soup.find_all('table', class_='dextable')
    target = maintable[0].find_all(class_='cen')
    target_block = maintable[0].find_all(class_='fooinfo')
    movesdict['name'] = item_name
    movesdict['type'] = movedex_help.find_type(target[1].find('a').get('href'))
    movesdict['category'] = movedex_help.find_category(target[2].find('a').get('href'))
    movesdict['pp'] = target[3].text.strip()
    movesdict['bp'] = target[4].text.strip()
    movesdict['acc'] = target[5].text.strip()
    movesdict['effect_rate'] = target[6].text.strip()
    movesdict['thumbnail'] = movedex_help.find_thumbnail(target[2].find('img').get('src'))
    movesdict['battle_effect'] = target_block[0].text.strip()
    if maintable[0].find_all(class_='fooleft')[1].text == 'In-Depth Effect:':
        if len(target_block) == 3:
            movesdict['secondary_effect'] = target_block[2].text.strip()
        else:
            movesdict['secondary_effect'] = target_block[1].text.strip()

        moves_list_manual_fix.append(item_name)
    elif movesdict['category'] == 'other':
        movesdict['secondary_effect'] = target_block[1].text.strip()
    else:
        movesdict['secondary_effect'] = target_block[1].text.strip()

    return movesdict


def dump_to_json_and_print(data):
    with open('content/pokemon/movedex/movedex.json', 'a') as fp:
        json.dump(data, fp)


def dump_moves():
    moves_dict = {}
    with open('content/pokemon/movedex/moves_list.txt') as fp:
        lines = [line.rstrip() for line in fp]
        for line in lines:
            if "Max " not in line:
                print(line)
                moves_dict_entry = scrape_move(line)
                moves_dict[line] = moves_dict_entry
                print(moves_dict_entry)
    print(moves_dict)
    dump_to_json_and_print(moves_dict)


dump_moves()
print(moves_list_manual_fix)
