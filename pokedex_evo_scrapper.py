from bs4 import BeautifulSoup
import requests


def scrape_evolution(url):
    item_dict = {}
    # url = "https://www.serebii.net/pokedex-swsh/bulbasaur/"
    r = requests.get(url)
    if r.status_code == 404:
        return "Could not find item"
    soup = BeautifulSoup(r.text, 'html.parser')

    evochain = soup.find('table', class_="evochain")
    # print(evochain)
    evo_list = []
    method_list = []
    pokemon_list = []
    evo_dict = {}

    images = evochain.find_all("img")
    for image in images:
        if "evoicon" in image["src"]:
            if "Level" in image["alt"]:
                evo_list.append(image["alt"] + image["src"][23:-4])
                method_list.append(image["alt"] + image["src"][23:-4])
            if "Trade" in image["alt"]:
                evo_list.append("Trade")
                method_list.append("Trade")
            if "Use " in image["alt"]:
                evo_list.append(image["alt"][4:])
                method_list.append(image["alt"][4:])
        else:
            if "Gigantamax" not in image["alt"]:
                evo_list.append(image["alt"])
                pokemon_list.append(image["alt"])
    # print(evo_list)
    # print(pokemon_list)
    # print(method_list)

    pokemon_count = 0
    for pokemon in pokemon_list:
        # print(pokemon_count)
        evo_dict[pokemon] = []
        if pokemon_count < len(pokemon_list)-1:
            if pokemon_count <= 1:
                evo_dict[pokemon].append({"method": method_list[pokemon_count], "next": pokemon_list[pokemon_count+1]})
                previous_pokemon = pokemon
            else:
                evo_dict[previous_pokemon].append(
                    {"method": method_list[pokemon_count], "next": pokemon_list[pokemon_count + 1]})

        pokemon_count += 1

    return evo_dict


def scrape_mons_list():
    item_dict = {}
    url = "https://www.serebii.net/pokedex-swsh/bulbasaur/"
    r = requests.get(url)
    if r.status_code == 404:
        return "Could not find item"
    soup = BeautifulSoup(r.text, 'html.parser')

    all_options = soup.find_all('option')
    names = []
    for option in all_options:
        if "pokedex-swsh" in option["value"] and option["value"][14:-1] not in names and ".shtm" not in option["value"][14:-1] and option["value"][14:-1] != "":
            names.append(option["value"][14:-1])
    print(names)
    return names


scrape_mons_list()