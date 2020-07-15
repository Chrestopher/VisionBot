from discord.embeds import _EmptyEmbed

import help_command
import pokedex
import movedex

def page_flip_handler(reaction, embed):
    emoji = reaction.emoji
    direction = 0
    if emoji == "➡️":
        direction = 1
    elif emoji == "⬅️":
        direction = -1
    return page_flip_commands(embed, direction)


def page_flip_commands(embed, direction):
    if type(embed) is not _EmptyEmbed:
        if "Help" in embed.title:
            return handle_commands_embed(embed, direction)
        elif "Pokedex" in embed.footer.text:
            return handle_pokedex_embed(embed, direction)
        else:
            return "Not a valid embed"


def handle_commands_embed(embed, direction):
    current_page = int(embed.footer.text.split("/")[0])
    if direction == 1 and current_page != 3:
        return help_command.helppages[current_page + 1]
    if direction == -1 and current_page != 1:
        return help_command.helppages[current_page - 1]
    else:
        if direction == 1:
            return help_command.helppages[1]
        elif direction == -1:
            return help_command.helppages[3]
        else:
            print("Direction should be 1 or -1")


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
