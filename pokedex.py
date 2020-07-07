from bs4 import BeautifulSoup
import requests
import generate_data
import num_util_functions
import discord

pokedex_url_prefix = "https://serebii.net/pokedex-swsh/"
pokedex_url_postfix = "/"
pokedex = generate_data.generate_pokedex_dictionary()

color_type_dictionary = dict(Normal="BDBDAE", Poison="A85CA0", Psychic="0B0C0C", Grass="8CD751", Ground="EAC854",
                             Ice="96F1FF", Fire="FA5543", Rock="CBBB71", Dragon="8674FF", Water="56AEFF", Bug="C2D21F",
                             Dark="8D6955", Fighting="A85644", Ghost="7A75D7", Steel="C2C1D8", Flying="79A4FF",
                             Electric="FEE63C", Fairy="F8ACFF")


def scrape_mons_list():
    url = "https://www.serebii.net/pokedex-swsh/bulbasaur/"
    r = requests.get(url)
    if r.status_code == 404:
        return "Could not find item"
    soup = BeautifulSoup(r.text, 'html.parser')

    all_options = soup.find_all('option')
    names = []
    for option in all_options:
        if "pokedex-swsh" in option["value"] and option["value"][14:-1] not in names and ".shtm" not in option["value"][
                                                                                                        14:-1] and \
                option["value"][14:-1] != "":
            names.append(option["value"][14:-1])
    return names


def get_pokemon(args):
    pokemon = "".join(args).lower()
    found_pokemon = ""
    for mon in pokedex.keys():
        if mon.lower().startswith(pokemon):
            found_pokemon = mon
            break

    if not found_pokemon:
        return "Could not find pokemon"

    if pokemon is {}:
        return "Could not find pokemon"

    return build_pokemon_summary_embed(found_pokemon)


def retrieve(pokemon_name):
    pokemon_name = pokemon_name.lower()
    if pokemon_name not in pokedex:
        return {}
    else:
        return pokedex[pokemon_name]


def build_pokemon_summary_embed(pokemon_name):
    pokemon = retrieve(pokemon_name)
    type1 = pokemon["properties"]["type1"]
    color = get_color(type1)

    embed = discord.Embed(title=pokemon["name"], colour=discord.Colour(color), description=display_link(pokemon_name))
    embed.set_thumbnail(url=pokemon["image"])
    embed.add_field(name="Height", value=num_util_functions.convert_meters_to_feet_inches(pokemon["properties"]["height"][:-1]), inline=True)
    embed.add_field(name="Weight", value=num_util_functions.convert_kilograms_to_lbs(pokemon["properties"]["weight"][:-2]), inline=True)
    embed.add_field(name="Type", value=display_type(pokemon["properties"]["type1"], pokemon["properties"]["type2"]), inline=False)
    embed.add_field(name="Abilities:", value=format_abilities(pokemon["abilities"]), inline=False)
    embed.set_footer(text="Created by VisionBot Pokedex (1/3)", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def build_pokemon_stats_embed(pokemon_name):
    pokemon = retrieve(pokemon_name)
    stats = pokemon["base_stats"]
    thumbnail = pokemon["image"]
    type1 = pokemon["properties"]["type1"]
    color = get_color(type1)

    embed = discord.Embed(title=pokemon["name"], colour=discord.Colour(color))
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="Base Stats", value=format_stats(stats), inline=False)
    embed.set_footer(text="Created by VisionBot Pokedex (2/3)", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def build_pokemon_weaknesses_resists_embed(pokemon_name):
    pokemon = retrieve(pokemon_name)
    thumbnail = pokemon["image"]
    type1 = pokemon["properties"]["type1"]
    color = get_color(type1)
    weakness = get_weaknesses_or_resists(1, pokemon["weakness"])
    resists = get_weaknesses_or_resists(-1, pokemon["weakness"])

    embed = discord.Embed(title=pokemon["name"], colour=discord.Colour(color))
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="Weaknesses", value=format_weaknesses_or_resists(weakness), inline=True)
    embed.add_field(name="Resists", value=format_weaknesses_or_resists(resists), inline=True)
    embed.set_footer(text="Created by VisionBot Pokedex (3/3)", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def format_abilities(abilities):
    ability_string = ""
    for ability in abilities.keys():
        if abilities[ability]["HA"]:
            ability_string += ability + " (HA)\n"
        else:
            ability_string += ability + "\n"
    return ability_string


def format_stats(stats):
    stat_string_list = ["HP:  **" + stats["hp"] + "**\n", "Att:  **" + stats["att"] + "**\n", "Def:  **" + stats["def"] + "**\n",
                        "SpA: **" + stats["spa"] + "**\n", "SpD: **" + stats["spd"] + "**\n", "Spe:  **" + stats["spe"] + "**\n\n",
                        "Total: **" + stats["total"] + "**"]
    return "".join(stat_string_list)


def get_weaknesses_or_resists(selection, chart):
    elements_without_1x = dict(filter(lambda element: element[1] != 1.0, chart.items()))
    if selection == 1:
        return dict(filter(lambda element: element[1] > 1.0, elements_without_1x.items()))
    elif selection == -1:
        return dict(filter(lambda element: element[1] < 1.0, elements_without_1x.items()))


def format_weaknesses_or_resists(elements):
    info = ""
    for type1 in elements.keys():
        mulitiplier = str(elements[type1])
        if str(elements[type1])[-1] == "0":
            mulitiplier = mulitiplier[:-2] + "x"
        else:
            mulitiplier = "x" + mulitiplier
        info += type1.capitalize() + ": " + mulitiplier + "\n"
    return info


def display_link(pokemon_name):
    return "[Serebii](" + pokedex_url_prefix + pokemon_name.lower() + pokedex_url_postfix + ")"


def display_type(type1, type2):
    if type2 == "":
        return type1
    else:
        return type1 + "/" + type2


def get_color(type1):
    return int(color_type_dictionary[type1], 16)
