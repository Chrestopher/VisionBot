from bs4 import BeautifulSoup
import requests
import generate_data
import itemdex_helper
import discord

itemdex_url_prefix = "https://serebii.net/itemdex/"
itemdex_url_postfix = "/"
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
        if "pokedex-swsh" in option["value"] and option["value"][14:-1] not in names and ".shtm" not in option["value"][14:-1] and option["value"][14:-1] != "":
            names.append(option["value"][14:-1])
    print(names)
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

    name, response = retrieve_image_url(found_pokemon)

    return build_pokemon_image_embed(name, response)


def retrieve_image_url(pokemon_name):
    if pokemon_name not in pokedex:
        return "Could not find item"
    else:
        return [pokedex[pokemon_name]["name"], pokedex[pokemon_name]["image"]]


def build_pokemon_image_embed(pokemon, image_url):
    color_in_int = int("F36A04", 16)
    embed = discord.Embed(title=pokemon, colour=discord.Colour(color_in_int))

    # embed.set_thumbnail(url=image_url)
    embed.set_image(url=image_url)
    # embed.add_field(name="Type", value=item_dict["item_type"], inline=False)
    embed.set_footer(text="Created by VisionBot Pokedex", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed
