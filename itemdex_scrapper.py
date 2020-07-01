from bs4 import BeautifulSoup
import requests
import json
import itemdex
import itemdex_helper


def scrape_to_file():
    itemdex_big_dict = {}
    with open("content/pokemon/itemdex/itemdex_list.txt") as fp:
        lines = [line.rstrip() for line in fp]
        # lines = lines[907:] - did this so when the code broke, i can resume
        for line in lines:
            print(line)
            itemdex_entry = itemdex.scrape(line)
            itemdex_big_dict[line] = itemdex_entry
    fp.close()
    dump_to_json_and_print(itemdex_big_dict)


def scrape_berries():
    item_dict = {}

    url = "https://serebii.net/itemdex/roseliberry.shtml"
    r = requests.get(url)
    if r.status_code == 404:
        return "Could not find item"
    soup = BeautifulSoup(r.text, 'html.parser')
    contents = soup.find_all('table', class_="dextable")
    first_row = soup.findAll("td", class_="cen")

    item_dict["item_name"] = contents[0].text.strip()
    item_dict["item_type"] = first_row[1].get_text(separator="\n").strip()

    x = 0
    for item in contents:
        print(x)
        print(item)
        x += 1

    item_dict["item_description"] = itemdex_helper.get_description(contents, item_dict["item_type"])

    item_dict["item_image_url"] = itemdex_helper.get_image(first_row)
    print(item_dict)


def build_item_embed():
    pass


def write_to_text_file(dex_list):
    f = open("content/pokemon/itemdex/itemdex_list.txt", "a")
    for item in dex_list:
        f.write(item + "\n")
    f.close()


def dump_to_json_and_print(data):
    with open('content/pokemon/itemdex/itemdex_data.json', 'a') as fp:
        json.dump(data, fp)

    new_dict = {}
    with open('content/pokemon/itemdex/itemdex_data.json') as fp:
        data = json.load(fp)
        print(data)


# grab_items()
# scrape_berries()
scrape_to_file()
