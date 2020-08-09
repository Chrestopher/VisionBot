import requests
import time

def search(args):
    test = "".join(args).lower()
    if test == 'joe':
        return 'https://i.imgur.com/4vAEt1j.png'
    if len(test) >= 3:
        character = "%20".join(args)
        result = requests.get('https://api.jikan.moe/v3/search/character?q=' + character +'&limit=1')
        if result.status_code == 404:
            return "Your Character does not exist."
        time.sleep(1)
        result_id = result.json()['results'][0]['mal_id']
        pictures_links = requests.get('https://api.jikan.moe/v3/character/' + str(result_id) + '/pictures')
        if len(pictures_links.json()['pictures']) == 0:
            return "No Pictures Available. Your Character has no pictures."
        else:
            result_pic = pictures_links.json()['pictures'][0]['large']
            return result_pic
    else:
        return "Error: You need a name with more than 3 characters!!! (weeb)"