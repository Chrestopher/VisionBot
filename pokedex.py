from bs4 import BeautifulSoup
import requests
import generate_data
import itemdex_helper
import num_util_functions
import discord

pokedex_url_prefix = "https://serebii.net/pokedex-swsh/"
pokedex_url_postfix = "/"
pokedex = generate_data.generate_pokedex_dictionary()


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

    color_in_int = int("F36A04", 16)
    embed = discord.Embed(title=pokemon["name"], colour=discord.Colour(color_in_int), description=display_link(pokemon_name))

    embed.set_thumbnail(url=pokemon["image"])
    embed.add_field(name="Height", value=num_util_functions.convert_meters_to_feet_inches(pokemon["properties"]["height"][:-1]), inline=True)
    embed.add_field(name="Weight", value=num_util_functions.convert_kilograms_to_lbs(pokemon["properties"]["weight"][:-2]), inline=True)
    embed.add_field(name="Type", value="/".join([pokemon["properties"]["type1"], pokemon["properties"]["type2"]]), inline=False)
    embed.add_field(name="Abilities:", value=build_abilities(pokemon["abilities"]), inline=False)
    embed.set_footer(text="Created by VisionBot Pokedex (1/2)", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def build_pokemon_stats_embed(pokemon_name):
    pokemon = retrieve(pokemon_name)
    stats = pokemon["base_stats"]
    thumbnail = pokemon["image"]

    color_in_int = int("F36A04", 16)
    embed = discord.Embed(title=pokemon["name"], colour=discord.Colour(color_in_int))

    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="Base Stats", value=build_stats(stats), inline=False)
    embed.set_footer(text="Created by VisionBot Pokedex (2/2)", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def build_abilities(abilities):
    ability_string = ""
    for ability in abilities.keys():
        if abilities[ability]["HA"]:
            ability_string += ability + " (HA)\n"
        else:
            ability_string += ability + "\n"
    return ability_string


def build_stats(stats):
    stat_string_list = ["HP:         " + stats["hp"] + "\n", "Att:  " + stats["att"] + "\n", "Def:  " + stats["def"] + "\n",
                        "SpA: " + stats["spa"] + "\n", "SpD: " + stats["spd"] + "\n", "Spe:  " + stats["spe"] + "\n\n",
                        "Total: " + stats["total"]]
    return "".join(stat_string_list)


def display_link(pokemon_name):
    return "[Serebii](" + pokedex_url_prefix + pokemon_name.lower() + pokedex_url_postfix + ")"
