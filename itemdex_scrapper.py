from bs4 import BeautifulSoup
import requests

# item = "https://serebii.net/itemdex/casteliacone.shtml"
# pokemon = "https://serebii.net/pokedex-swsh/bulbasaur/"

# Berries are broken for this


def grab_items():
    url_list = ["https://serebii.net/itemdex/potion.shtml"]
    for url in url_list:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # contents = soup.find_all('table', class_="dextable")
        first_row = soup.findAll("option")

    dex_list = []
    x = -1
    for item in first_row:
        x += 1
        #print(x)
        #print(item)
        print(item["value"][9:-6])
        if "/" not in item["value"][9:-6]:
            dex_list.append(item["value"][9:-6])

    print(dex_list)
    dex_list.sort()
    write_to_text_file(dex_list)


def build_item_embed():
    pass


def write_to_text_file(dex_list):
    f = open("content/pokemon/itemdex/itemdex_dictionary.txt", "a")
    for item in dex_list:
        f.write(item + "\n")
    f.close()

grab_items()
