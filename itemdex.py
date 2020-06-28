from bs4 import BeautifulSoup
import requests
import generate_data
import itemdex_helper
import discord

itemdex_url_prefix = "https://serebii.net/itemdex/"
itemdex_url_postfix = ".shtml"
itemdex_list = generate_data.generate_itemdex_list()

itemdex_dictionary = generate_data.generate_itemdex_dictionary()


def get_item(args):
    item_name = "".join(args).lower()
    found_item_name = ""
    for item in itemdex_list:
        if item.startswith(item_name):
            found_item_name = item
            break

    if not found_item_name:
        return "Could not find item"

    response = retrieve(found_item_name)

    if type(response) is not dict:
        return response
    else:
        return build_item_embed(response)


def retrieve(item_name):
    print(item_name)
    if item_name not in itemdex_dictionary:
        return "Could not find item"
    else:
        return itemdex_dictionary[item_name]


def scrape(item_name):
    item_dict = {}
    url = itemdex_url_prefix + item_name + itemdex_url_postfix
    r = requests.get(url)
    if r.status_code == 404:
        return "Could not find item"
    soup = BeautifulSoup(r.text, 'html.parser')
    contents = soup.find_all('table', class_="dextable")
    first_row = soup.findAll("td", class_="cen")

    item_dict["item_name"] = contents[0].text.strip()
    item_dict["item_type"] = first_row[1].get_text(separator="\n").strip()

    item_dict["item_description"] = itemdex_helper.get_description(contents, item_dict["item_type"])

    item_dict["item_image_url"] = itemdex_helper.get_image(first_row)

    return item_dict


def build_item_embed(item_dict):
    color_in_int = int("F36A04", 16)
    embed = discord.Embed(title=item_dict["item_name"], colour=discord.Colour(color_in_int),
                          description=item_dict["item_description"])

    embed.set_thumbnail(url=item_dict["item_image_url"])
    embed.add_field(name="Type", value=item_dict["item_type"], inline=False)
    embed.set_footer(text="Created by VisionBot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed
