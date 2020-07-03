from bs4 import NavigableString


def get_description(contents, item_type):
    if item_type == "Fossil":
        return parse_fossil(contents)
    elif item_type == "Berry":
        return parse_berry(contents)
    else:
        return parse_normally(contents)


def get_image(contents):
    url = contents[0].find("img")
    if url is not None:
        return "https://serebii.net" + url["src"]
    else:
        return ""


def parse_berry(contents):
    if len(contents) < 8:
        description = contents[4].find("td", class_="fooinfo")
        if description is None:
            return contents[5].find("td", class_="fooinfo").get_text(separator="\n").strip()
        else:
            return description.get_text(separator="\n").strip()
    else:
        td_list = contents[7].find_all("td", class_="fooinfo")
        return contents[7].find_all("td", class_="fooinfo")[len(td_list)-1].text


def parse_fossil(contents):
    return "".join([element for element in contents[4].find_all("td", class_="fooinfo")[0] if
                    isinstance(element, NavigableString)]).replace(".", ". ")


def parse_normally(contents):
    return contents[4].find("td", class_="fooinfo").get_text(separator="\n").strip()
