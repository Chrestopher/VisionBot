import discord
import requests
import time
from Api_decorator import ApiCallSaver, pull_from_json


def search(search_name, search_type):
    """
    Will perform a search for the query (args) using an API call to the MyAnimeList database. If the search type
    provided is "character", only the MyAnimeList ID for that query is returned. If the search type provided is
    "anime", a tuple containing the Anime's name, its MyAnimeList ID, and the URL to its MyAnimeList host image will
    be returned.
    :param args: The search query
    :param search_type: The type of thing that is to be searched for in the MyAnimeList database.
    :return:
    - For search type "character": The query's MyAnimeList ID.
    - For search type "anime": A tuple with the query's Name, MyAnimeList ID, and the URL to its MyAnimeList host image.
    """
    search_name_no_space = "".join(search_name).lower()
    if search_name_no_space == 'joe':
        return 'https://i.imgur.com/4vAEt1j.png'
    elif len(search_name_no_space) >= 3:
        query = "%20".join(search_name)
        response = requests.get('https://api.jikan.moe/v3/search/' + search_type + '?q=' + query + '&limit=1')
        result = response.json()['results'][0]
        time.sleep(0.5)
        if response.status_code == 404:
            return "404"
        result_id = result['mal_id']
        if search_type == 'anime':
            anime_title = result['title']
            anime_thumbnail = result['image_url']
            anime_summary = result['synopsis']
            anime_info = (result_id, anime_title, anime_thumbnail, anime_summary)
            return anime_info
        else:
            return result_id
    else:
        return "-1"


def anime_stats(args):
    """
    Performs a search for a desired anime's MyAnimeList ID and uses it to first check if a dictionary with the anime's
    information is already stored in the bot's animestats.json file. If it is, it uses that dictionary to build an
    embed that will display the "stats" information of the anime in-question. If a dictionary does not yet exist in
    the animestats.json file, this method will call the required method in order to generate one (also saving it to the
    animestats.json file. Unless the search query does not exist or the user inputs a value less than 3 characters for
    their search, this method will return the first embed page of "stats" information.
    :param args: The search query, inputted by the user.
    :return: The first embed page of "stats" information for the anime in-question.
    """
    anime_info = search(args, 'anime')
    if anime_info == "-1":
        return 'Error: You need a name with more than 3 characters!!!'
    elif anime_info == "404":
        return "The anime does not exist."
    else:
        try:
            anime_stat_dict = pull_from_json(anime_info[1], 'animedb')
        except:
            anime_stat_dict = api_info_getter(anime_info)
        return build_anime_info(anime_stat_dict)


@ApiCallSaver(target_file='animedb')
def api_info_getter(anime_info):
    """
    Takes in an anime name, the MyAnimeList database id of that anime, and the URL link to the MyAnimeList image for
    that anime; it then uses the database id in order to make an API call that retrieves the "stats" info of the
    designated anime from the MyAnimeList database. With this information and the name, id, and URL link provided,
    a dictionary containing all of it is created to store the data, and is also subsequently saved into the
    animestats.json file in the apicalls\ folder. Finally, the completed dictionary is returned.

    :param anime_info: anime info data
    :return: The dictionary containing all of the needed information about the anime in-question.
    """
    stats = requests.get('https://api.jikan.moe/v3/anime/' + str(anime_info[0]) + '/stats')
    time.sleep(0.5)
    home = requests.get('https://api.jikan.moe/v3/anime/' + str(anime_info[0]) + '/')
    stats = stats.json()
    home = home.json()


    # anime info
    anime_name = anime_info[1]
    database_id_name = anime_info[0]
    thumbnail = anime_info[2]
    summary = anime_info[3]

    # stats
    watching = str(stats['watching'])
    completed = str(stats['completed'])
    on_hold = str(stats['on_hold'])
    dropped = str(stats['dropped'])
    plan_to_watch = str(stats['plan_to_watch'])
    total = str(stats['total'])
    scores = (stats['scores'])
    score_string = score_string_builder(scores)

    # home
    genres = get_genres(home["genres"])
    print(genres)

    data_tuple = (anime_name, database_id_name, thumbnail, watching, completed, on_hold, dropped, plan_to_watch, total, score_string, summary, genres)
    anime_info_dict = anime_stats_dictionary_builder(data_tuple)
    return anime_info_dict


def score_string_builder(score_list):
    """
    Takes in a list of scores and appends them together on new lines in order to generate a single formatted string
    containing all of the scores together. It then returns that string.
    :param score_list: The list of scores whose data will be used to create the score string.
    :return: The score string.
    """
    score = []
    for item in score_list:
        dictionary = score_list[item]
        vote_number = dictionary['votes']
        percentage_number = dictionary['percentage']
        final_string = "    #" + str(item) + ": " + "Votes: " + str(vote_number) + " | Percentage: " + str(
            percentage_number) + '\n'
        score.append(final_string)
    score_string = ""
    for item in reversed(score):
        score_string += item
    return score_string


def anime_stats_dictionary_builder(anime_data):
    """
    Takes in a tuple of anime data (which includes information such as name, database id, watching, etc)
    and creates a dictionary with keys that accurately reference each different data piece within the tuple,
    and finally returns that dictionary.
    :param anime_data: The tuple of anime data whose data will be used to create keys under which it will be values for.
    :return: A dictionary containing the data from the anime_data tuple.
    """
    anime_stat_dict = {}
    anime_stat_dict.update({'name': anime_data[0]})
    anime_stat_dict.update({'database_id': anime_data[1]})
    anime_stat_dict.update({'thumbnail': anime_data[2]})
    anime_stat_dict.update({'watching': anime_data[3]})
    anime_stat_dict.update({'completed': anime_data[4]})
    anime_stat_dict.update({'on_hold': anime_data[5]})
    anime_stat_dict.update({'dropped': anime_data[6]})
    anime_stat_dict.update({'plan': anime_data[7]})
    anime_stat_dict.update({'total': anime_data[8]})
    anime_stat_dict.update({'scores': anime_data[9]})
    anime_stat_dict.update({'summary': anime_data[10]})
    anime_stat_dict.update({'genres': anime_data[11]})
    return anime_stat_dict


def build_anime_info(anime_info):
    """
    Takes in a dictionary containing the "stats" information of an anime, and uses it to construct and return an embed
    page (page 1) containing that information.
    :param anime_stat: The dictionary containing the "stats" information of an anime.
    :return: The page 1 embed page of "stats" information for the anime.
    """
    color = int("FEE63C", 16)
    embed = discord.Embed(title=anime_info['name'], colour=discord.Colour(color),
                          description=display_link(anime_info["database_id"]))
    embed.add_field(name="Summary", value=anime_info["summary"])
    embed.set_thumbnail(url=anime_info['thumbnail'])

    embed.set_footer(text="Created by VisionBot AnimeStats Protocols (1/3)",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def build_anime_stats(anime_stat):
    """
    Takes in a dictionary containing the "stats" information of an anime, and uses it to construct and return an embed
    page (page 1) containing that information.
    :param anime_stat: The dictionary containing the "stats" information of an anime.
    :return: The page 1 embed page of "stats" information for the anime.
    """
    embed = (discord.Embed(title=anime_stat['name'], colour=discord.Colour(int("FEE63C", 16))))
    embed.set_thumbnail(url=anime_stat['thumbnail'])
    embed.add_field(name="Watching: ", value=anime_stat['watching'], inline=True)
    embed.add_field(name="Completed: ", value=anime_stat['completed'], inline=False)
    embed.add_field(name="On Hold: ", value=anime_stat['on_hold'], inline=False)
    embed.add_field(name="Dropped: ", value=anime_stat['dropped'], inline=False)
    embed.add_field(name="Plan To Watch: ", value=anime_stat['plan'], inline=False)
    embed.add_field(name="Total: ", value=anime_stat['total'], inline=False)
    embed.set_footer(text="Created by VisionBot AnimeStats Protocols (2/3)",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def build_anime_scores(anime_stat):
    """
    Takes in a dictionary containing the "stats" information of an anime, and uses it to construct and return an embed
    page (page 3) containing that information.
    :param anime_stat: The dictionary containing the "stats" information of an anime.
    :return: The page 2 embed page of "stats" information for the anime.
    """
    embed = (discord.Embed(title=anime_stat['name'], colour=discord.Colour(int("FEE63C", 16))))
    embed.set_thumbnail(url=anime_stat['thumbnail'])
    embed.add_field(name="Scores: " + '\n', value=anime_stat['scores'], inline=True)
    embed.set_footer(text="Created by VisionBot AnimeStats Protocols (3/3)",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def char_pic(args):
    """
    Performs a search for a character based on a user-inputted query (args). If the character query exists, an API
    Call is made that pulls associated pictures to the character from the MyAnimeList database. The URL to the first
    image is returned. If there are no pictures for that character, a message saying so is returned.
    :param args: The user's search query
    :return: The picture URL for a character.
    """
    pic = search(args, 'character')
    if pic == "-1":
        return 'Error: You need a name with more than 3 characters!!!'
    elif pic == "404":
        return "Your character does dot exist."
    elif pic == 'https://i.imgur.com/4vAEt1j.png':
        return 'https://i.imgur.com/4vAEt1j.png'
    else:
        pictures_links = requests.get('https://api.jikan.moe/v3/character/' + str(pic) + '/pictures')
        if len(pictures_links.json()['pictures']) == 0:
            return "No pictures available. Your character has no pictures."
        else:
            result_pic = pictures_links.json()['pictures'][0]['large']
            return result_pic


def display_link(anime_id):
    return "[MAL](" + "https://myanimelist.net/anime/" + str(anime_id) + ")"


def get_genres(genres_list):
    genres = []
    for genre in genres_list:
        genres.append(genre["name"])

    return genres
