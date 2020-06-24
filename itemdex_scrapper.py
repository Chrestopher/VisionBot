from bs4 import BeautifulSoup
import requests

# item = "https://serebii.net/itemdex/casteliacone.shtml"
# pokemon = "https://serebii.net/pokedex-swsh/bulbasaur/"

# Berries are broken for this


def grab_items():
    url_list = ["https://serebii.net/itemdex/casteliacone.shtml", "https://serebii.net/itemdex/potion.shtml", "https://serebii.net/itemdex/revive.shtml", "https://serebii.net/itemdex/relicband.shtml"]
    for url in url_list:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        contents = soup.find_all('table', class_="dextable")
        first_row = soup.findAll("td", class_="cen")
        item_name = contents[0].text.strip()
        item_description = contents[4].find("td", class_="fooinfo").text.strip()
        item_image_url = "https://serebii.net" + first_row[0].find("img")["src"]
        item_type = first_row[1].text
        print(item_name)
        print(item_description)
        print(item_image_url)
        print(item_type)
        print()


def build_item_embed():
    pass

grab_items()
