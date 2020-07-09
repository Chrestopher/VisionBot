from bs4 import BeautifulSoup
import generate_data
import requests
import movedex_help
movedex_url_prefix = "https://www.serebii.net/attackdex-swsh/"
movedex_url_postfix = ".shtml"
movedex_list = generate_data.generate_movedex_list()
#movedex_dictionary= generate_data.generate_movedex_dictionary()

moves_list_manual_fix=[]

def write_move_names_to_file():
    r= requests.get('https://www.serebii.net/attackdex-swsh/')
    soup= BeautifulSoup(r.text, 'html.parser')
    moveslist= []
    moveslist_manual_entry=[]
    for option in soup.find_all('option'):
        f=option.text
        if 'AttackDex' not in f and f not in moveslist:
            moveslist.append(f)
    f= open('content/pokemon/movedex/moves_list.txt','a')
    for move in moveslist:
        f.write(move + '\n')
    f.close()


def scrape_move(item_name):
    movesdict={}
    url= movedex_url_prefix + ''.join(item_name.lower().rsplit()) + movedex_url_postfix
    moverequest = requests.get(url)
    if moverequest.status_code==404:
        return "could not find move"
    soup=BeautifulSoup(moverequest.text,'html.parser')
    maintable = soup.find_all('table', class_='dextable')
    target=maintable[0].find_all(class_='cen')
    target_block=maintable[0].find_all(class_='fooinfo')
    movesdict['name']= item_name
    movesdict['type']= movedex_help.find_type(target[1].find('a').get('href'))
    movesdict['category']=movedex_help.find_category(target[2].find('a').get('href'))
    movesdict['pp']= target[3].text.rsplit()
    movesdict['bp']=target[4].text.rsplit()
    movesdict['acc']=target[5].text.rsplit()
    movesdict['effect_rate']= ''.join(target[6].text.rsplit())
    movesdict['max_power']=target[7].text.rsplit()
    movesdict['thumbnail']=movedex_help.find_thumbnail(target[2].find('img').get('src'))
    movesdict['battle_effect'] = ' '.join(target_block[0].text.rsplit())
    if maintable[0].find_all(class_='fooleft')[1].text=='In-Depth Effect:':
        movesdict['secondary_effect'] = ' '.join(target_block[2].text.rsplit())
        if movesdict['category'] != 'other':
            movesdict['max_move'] = target_block[3].find('u').text
        moves_list_manual_fix.append(item_name)
    if movesdict['category']=='other':
        movesdict['secondary_effect'] = ' '.join(target_block[1].text.rsplit())
    else:
        movesdict['secondary_effect'] = ' '.join(target_block[1].text.rsplit())
        movesdict['max_move'] = target_block[2].find('u').text



def dump_moves():
    moves_dict={}
    with open('content/pokemon/movedex/moves_list.txt') as fp:
        lines= [line.rstrip() for line in fp]
        for line in lines:
            print(line)
            moves_dict_entry=scrape_move(line)
            moves_dict[line]=moves_dict_entry
    print(moves_dict)
dump_moves()
print(moves_list_manual_fix)