import generate_data
import random

joe_keyword_responses = generate_data.generate_joe_keyword_responses_list()
joe_emotes = ["👀", "<:lol:288909608745959434>"]


def get_joe_keyword_response():
    index = random.randint(0, len(joe_keyword_responses)-1)
    return joe_keyword_responses[index]


def get_joe_emote_response():
    index = random.randint(0, len(joe_emotes)-1)
    return joe_emotes[index]

