from bs4 import BeautifulSoup
import requests
import discord

itemdex_url_prefix = "https://serebii.net/itemdex/"
itemdex_url_postfix = ".shtml"


def get_item(message):
    item_name = message.content[9:]
    print(item_name)
    scrape_response = scrape(item_name)
    if type(scrape_response) is not dict:
        return scrape_response
    else:
        return build_item_embed(scrape_response)


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
    item_dict["item_description"] = contents[4].find("td", class_="fooinfo").text.strip()
    item_dict["item_image_url"] = "https://serebii.net" + first_row[0].find("img")["src"]
    if first_row[1].text.startswith("Decorations"):
        item_dict["item_type"] = first_row[1].text[11:]
    else:
        item_dict["item_type"] = first_row[1].text

    return item_dict


def build_item_embed(item_dict):
    color_in_int = int("F36A04", 16)
    embed = discord.Embed(title=item_dict["item_name"], colour=discord.Colour(color_in_int),
                          description=item_dict["item_description"])

    embed.set_thumbnail(url=item_dict["item_image_url"])
    # embed.set_author(name=item_dict["item_name"])
    embed.add_field(name="Type", value=item_dict["item_type"], inline=False)
    embed.set_footer(text="Created by VisionBot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed