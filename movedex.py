from bs4 import BeautifulSoup
import generate_data
import discord
import string

movedex_url_prefix = "https://www.serebii.net/attackdex-swsh/"
movedex_url_postfix = ".shtml"
movedex_list = generate_data.generate_movedex_list()

movedex_dictionary = generate_data.generate_movedex_dictionary()

color_type_dictionary = dict(normal="BDBDAE", poison="A85CA0", psychic="0B0C0C", grass="8CD751", ground="EAC854",
                             ice="96F1FF", fire="FA5543", rock="CBBB71", dragon="8674FF", water="56AEFF", bug="C2D21F",
                             dark="8D6955", fighting="A85644", ghost="7A75D7", steel="C2C1D8", flying="79A4FF",
                             electric="FEE63C", fairy="F8ACFF")


def get_move(args):
    move_name = string.capwords(" ".join(args))
    movetone = ''
    for move in movedex_list:
        if move.startswith(move_name):
            movetone = move
            break
    if not movetone:
        return "move not found"
    return build_embed(movetone)


def build_embed(move_name):
    thismove = movedex_dictionary[move_name]
    move_color = color_type_dictionary[thismove['type']]
    secondary_effect = secondary_effect_process(thismove['effect_rate'], thismove['secondary_effect'])
    print(secondary_effect)
    embed = discord.Embed(title=thismove['name'],
                          description=display_link(move_name),
                          colour=int(move_color, 16))
    embed.add_field(name="__Type__", value=thismove['type'].capitalize(), inline=True)
    embed.add_field(name="__Battle Effects__", value=thismove['battle_effect'] + '\n' + secondary_effect, inline=False)
    embed.set_thumbnail(url='https://' + thismove['thumbnail'])
    embed.set_footer(text="Created by VisionBot \n Movedex (1/2)",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def build_embed_2(move_name):
    thismove = movedex_dictionary[move_name]
    move_color = color_type_dictionary[thismove['type']]
    embed = discord.Embed(title=thismove['name'],
                          description=display_link(move_name),
                          colour=int(move_color, 16))
    embed.add_field(name='__Category__', value=thismove['category'], inline=False)
    embed.add_field(name='__Battle Power__', value=thismove['bp'], inline=True)
    embed.add_field(name='__Power Points__', value=thismove['pp'], inline=True)
    embed.add_field(name='__Accuracy__', value=thismove['acc'], inline=True)
    embed.set_footer(text="Created by VisionBot \n Movedex (2/2)",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url='https://' + thismove['thumbnail'])
    return embed


def secondary_effect_process(effectrate, secondary_effect):
    effectrate_outcome = ''
    secondary_effect_outcome = ''
    if effectrate == "-- %":
        pass
    else:
        effectrate_outcome = 'Effect chance: {}'.format(effectrate)
    if secondary_effect == 'No effect.':
        pass
    else:
        secondary_effect_outcome = 'Secondary effect: ' + secondary_effect
    return '{}\n{}'.format(secondary_effect_outcome, effectrate_outcome)


def display_link(move_name):
    return "[Serebii](" + movedex_url_prefix + ''.join(move_name.lower().rsplit()) + movedex_url_postfix + ")"
