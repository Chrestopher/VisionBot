from discord.embeds import _EmptyEmbed

import help_command
import pokedex
import mal
import Api_decorator


def page_flip_handler(reaction, embed):
    emoji = reaction.emoji
    direction = 0
    if emoji == "➡️":
        direction = 1
    elif emoji == "⬅️":
        direction = -1
    return page_flip_commands(embed, direction)


def page_flip_commands(embed, direction):
    try:
        if "Help" in embed.title:
            return handle_commands_embed(embed, direction)
        elif "Pokedex" in embed.footer.text:
            return handle_pokedex_embed(embed, direction)
        elif "AnimeStats" in embed.footer.text:
            return handle_mal_embed(embed, direction, 'animedb')
        elif "MangaStats" in embed.footer.text:
            print('manga')
            return handle_mal_embed(embed, direction, 'mangadb')
        else:
            return "Not a valid embed"
    except:
        pass


def handle_commands_embed(embed, direction):
    current_page = int(embed.footer.text.split("/")[0])
    if direction == 1 and current_page != 4:
        return help_command.helppages[current_page + 1]
    if direction == -1 and current_page != 1:
        return help_command.helppages[current_page - 1]
    else:
        if direction == 1:
            return help_command.helppages[1]
        elif direction == -1:
            return help_command.helppages[4]
        else:
            print("Direction should be 1 or -1")


def handle_mal_embed(embed, direction, db):
    anime_name = embed.title
    animedex_page_mapper = {"1": 2, "2": 3, "3": 1}
    animedex_page_mapper_reverse = {"1": 3, "3": 2, "2": 1}
    page = embed.footer.text[43]

    if direction == 1:
        next_page = animedex_page_mapper[page]
    else:
        next_page = animedex_page_mapper_reverse[page]

    json_data = Api_decorator.pull_from_json(anime_name, db)

    if next_page == 1:
        return mal.build_mal_info(json_data, db)
    elif next_page == 2:
        return mal.build_mal_stats(json_data, db)
    elif next_page == 3:
        return mal.build_mal_scores(json_data, db)
    else:
        print('not a number')


def handle_pokedex_embed(embed, direction):
    pokemon_name = embed.title
    pokedex_page_mapper_1 = {"1": 2, "2": 3, "3": 1}
    pokedex_page_mapper_n1 = {"1": 3, "3": 2, "2": 1}
    page = embed.footer.text[30]
    if direction == 1:
        next_page = pokedex_page_mapper_1[page]
    else:
        next_page = pokedex_page_mapper_n1[page]

    if next_page == 1:
        return pokedex.build_pokemon_summary_embed(pokemon_name)
    elif next_page == 2:
        return pokedex.build_pokemon_stats_embed(pokemon_name)
    elif next_page == 3:
        return pokedex.build_pokemon_weaknesses_resists_embed(pokemon_name)
