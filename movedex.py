from bs4 import BeautifulSoup
import generate_data

movedex_url_prefix = "https://www.serebii.net/attackdex-swsh/"
movedex_url_postfix = ".shtml"
movedex_list = generate_data.generate_movedex_list()

movedex_dictionary= generate_data.generate_movedex_dictionary()