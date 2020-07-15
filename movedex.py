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
    embed = discord.Embed(title=thismove['name'],
                          description=display_link(move_name),
                          colour=int(move_color, 16))
    embed.add_field(name="__Move Description__", value=thismove['battle_effect'], inline=False)
    if thismove['secondary_effect'] != 'No effect.':
        if thismove['effect_rate'] == "-- %":
            embed.add_field(name="__Secondary Effect__", value=thismove['secondary_effect'], inline=False)
        else:
            embed.add_field(name="__Secondary Effect__",
                            value=thismove['secondary_effect'] + ' ' + thismove['effect_rate'].replace(" ", "") + '.',
                            inline=False)
    embed.add_field(name="__Type__", value=thismove['type'].capitalize(), inline=True)
    embed.add_field(name='__Category__', value=thismove['category'].capitalize(), inline=True)
    embed.add_field(name='‎ ‎', value=' ‎')  # Don't mess with these values, they're an empty unicode.
    embed.add_field(name='__Battle Power__', value=thismove['bp'], inline=True)
    embed.add_field(name='__Power Points__', value=thismove['pp'], inline=True)
    embed.add_field(name='__Accuracy__', value=thismove['acc'], inline=True)
    embed.set_thumbnail(url='https://' + thismove['thumbnail'])
    embed.set_footer(text="Created by VisionBot",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def display_link(move_name):
    return "[Serebii](" + movedex_url_prefix + ''.join(move_name.lower().rsplit()) + movedex_url_postfix + ")"
