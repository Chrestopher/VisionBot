from bs4 import BeautifulSoup
import requests
import json

# pokemon = "https://serebii.net/pokedex-swsh/bulbasaur/"


class Pokedex_Entry:

    # Dictionary template for a pokedex entry
    entry = {}

    # Initialize pokemon name
    def __init__(self, name):
        self.entry = {
            "name": "",
            "dex_number": None,
            "other_names": {
                "jname": "",
                "fname": "",
                "gname": "",
                "kname": ""
            },
            "properties": {
                "type1": "",
                "type2": "",
                "ev": "",
                "classification": "",
                "height": None,
                "weight": None,
                "capture_rate": None,
                "base_egg_steps": None,
                "egg_groups": []
            },
            "weakness": {
                "normal": 0,
                "fire": 0,
                "water": 0,
                "electric": 0,
                "grass": 0,
                "ice": 0,
                "fighting": 0,
                "poison": 0,
                "ground": 0,
                "flying": 0,
                "psychic": 0,
                "bug": 0,
                "rock": 0,
                "ghost": 0,
                "dragon": 0,
                "dark": 0,
                "steel": 0,
                "fairy": 0
            },
            "base_stats": {
                "total": None,
                "hp": None,
                "att": None,
                "def": None,
                "spa": None,
                "spd": None,
                "spe": None
            },
            "abilities": {},
            "moves": {
                "levelup": {},
                "tms": {},
                "trs": {},
                "eggmoves": {},
                "tutor": {}
            }
        }
        self.entry["name"] = name


def get_entry(url, name):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    dex_entry = Pokedex_Entry(name)

    # Find the "Other Names" data row
    tr = soup.find('td', string="Other Names").find_parent(
        "tr").find_next('tr')
    td = tr.find_all('td')  # Index the entire row
    languages = td[1].find_all("td")  # Grab the languages box
    dex_entry.entry["other_names"]["jname"] = languages[1].text  # Japanese
    dex_entry.entry["other_names"]["fname"] = languages[3].text  # French...
    dex_entry.entry["other_names"]["gname"] = languages[5].text  # And so on
    dex_entry.entry["other_names"]["kname"] = languages[7].text

    # Pokedex number
    numbers = td[10].find_all("td")
    dex_entry.entry["dex_number"] = int(numbers[1].text[1:])

    # Types
    types = td[22].find_all("img")
    dex_entry.entry["properties"]["type1"] = types[0]["alt"].split('-')[0]
    if(len(types) > 1):
        dex_entry.entry["properties"]["type2"] = types[1]["alt"].split('-')[0]

    # Classification
    tr = soup.find('td', string="Classification").find_parent(
        "tr").find_next('tr')
    td = tr.find_all('td')  # Index the entire row
    dex_entry.entry["properties"]["classification"] = td[0].text

    # Height
    dex_entry.entry["properties"]["height"] = td[1].text.split("\n")[1].strip()

    # Weight
    dex_entry.entry["properties"]["weight"] = td[2].text.split("\n")[1].strip()

    # Capture Rate
    dex_entry.entry["properties"]["capture_rate"] = int(td[3].text)

    # Base Egg Steps
    egg_string = ''.join(ch for ch in td[4].text if ch.isdigit())
    dex_entry.entry["properties"]["base_egg_steps"] = int(egg_string)

    # Abilities
    tr = tr.find_next('tr').find_next('tr')
    abilities = tr.text.split('\n')
    for ability in abilities:
        if(ability):
            # I know this is ugly duplication but I'm tired so too bad
            if(ability.startswith("Hidden Ability")):
                ability = ability.replace("Hidden Ability (Available):", "")
                ability_split = ability.split(':')
                name = ability_split[0].strip()
                desc = ability_split[1].strip()
                dex_entry.entry["abilities"][name] = {}
                dex_entry.entry["abilities"][name]["name"] = name
                dex_entry.entry["abilities"][name]["description"] = desc
                dex_entry.entry["abilities"][name]["HA"] = "true"
            else:
                ability_split = ability.split(':')
                name = ability_split[0]
                desc = ability_split[1].strip()
                dex_entry.entry["abilities"][name] = {}
                dex_entry.entry["abilities"][name]["name"] = name
                dex_entry.entry["abilities"][name]["description"] = desc
                dex_entry.entry["abilities"][name]["HA"] = "false"

    # EV
    tr = tr.find_next('tr').find_next('tr')
    td = tr.find_all('td')
    dex_entry.entry["properties"]["ev"] = td[2].text

    # Weakness
    tr = tr.find_next('tr').find_next('tr').find_next('tr')
    td = tr.find_all('td')
    i = 0
    for weakness in dex_entry.entry["weakness"]:
        dex_entry.entry["weakness"][weakness] = float(td[i].text[1:])
        i += 1

    # Egg Groups
    tr = tr.find_next('tr').find_next('tr')
    string = tr.text.strip()
    i = 0
    for character in string:
        if(character.isupper() & i):
            string = string[0:i]
            break
        i += 1
    dex_entry.entry["properties"]["egg_groups"].insert(0, string)

    tr = tr.find_next('tr').find_next('tr')
    string = tr.text.strip()
    i = 0
    for character in string:
        if(character.isupper() & i):
            string = string[0:i]
            break
        i += 1
    dex_entry.entry["properties"]["egg_groups"].insert(0, string)

    # Base Stats
    tr = soup.find_all('td', string="Stats")[1].find_parent(
        "tr").find_next('tr').find_next('tr')
    td = tr.find_all('td')  # Index the entire row
    # Strip all the non-numbers from the string
    base_stats = ''.join(ch for ch in td[0].text if ch.isdigit())
    dex_entry.entry["base_stats"]["total"] = base_stats
    dex_entry.entry["base_stats"]["hp"] = td[1].text
    dex_entry.entry["base_stats"]["att"] = td[2].text
    dex_entry.entry["base_stats"]["def"] = td[3].text
    dex_entry.entry["base_stats"]["spa"] = td[4].text
    dex_entry.entry["base_stats"]["spd"] = td[5].text
    dex_entry.entry["base_stats"]["spe"] = td[6].text

    # Moves (Oh boy)

    # Level Up Moves

    tr = soup.find('th', string="Attack Name").find_parent(
        "tr").find_next('tr')
    while(tr.text != 'Technical Machine Attacks'):
        td = tr.find_all('td')  # Index the entire row
        movename = td[1].text
        dex_entry.entry["moves"]["levelup"][movename] = {}

        if(td[0].text == '—'):
            dex_entry.entry["moves"]["levelup"][movename]["level"] = 1
        else:
            dex_entry.entry["moves"]["levelup"][movename]["level"] = td[0].text

        typename = td[2].img["alt"].split('-')[1].strip()
        dex_entry.entry["moves"]["levelup"][movename]["type"] = typename

        catname = td[3].img["alt"].split(' ')[1].strip()
        dex_entry.entry["moves"]["levelup"][movename]["category"] = catname

        if(td[4].text == "--"):
            dex_entry.entry["moves"]["levelup"][movename]["attack"] = 0
        else:
            dex_entry.entry["moves"]["levelup"][movename]["attack"] = int(
                td[4].text)

        dex_entry.entry["moves"]["levelup"][movename]["accuracy"] = int(
            td[5].text)

        dex_entry.entry["moves"]["levelup"][movename]["pp"] = int(td[6].text)

        effpcnt = td[7].text
        if(effpcnt == '--'):
            dex_entry.entry["moves"]["levelup"][movename]["effectpcnt"] = 0
        else:
            dex_entry.entry["moves"]["levelup"][movename]["pp"] = effpcnt

        tr = tr.find_next('tr')
        dex_entry.entry["moves"]["levelup"][movename]["description"] = tr.text
        tr = tr.find_next('tr')

    # TM Moves

    # print(dex_entry.entry)

    return dex_entry.entry


def generate_pokedex():
    Pokedex = {}
    url_base = "https://serebii.net/pokedex-swsh/"
    pokedex_names = "short_pokemon_list.txt"
    with open(pokedex_names, "r") as pokedex_names:
        for pokemon in pokedex_names:
            name = pokemon.strip()
            try:
                Pokedex[name] = get_entry(url_base + name.lower(), name)
            except:
                print("There was trouble accessing " + name + "'s page")

    print(Pokedex)

    with open('pokemon.json', 'w') as outfile:
        json.dump(Pokedex, outfile, indent=4)


generate_pokedex()
