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


image_type_dictionary = dict(normal="https://i.imgur.com/VHI1QGb.png", poison="https://i.imgur.com/8TOnG6t.png", psychic="https://i.imgur.com/MPQU5rR.png", grass="https://i.imgur.com/pYtAlxr.png", ground="https://i.imgur.com/GLlBhxe.png",
                             ice="https://i.imgur.com/qeCzZDi.png", fire="https://i.imgur.com/zhPTMJo.png", rock="https://i.imgur.com/03LnrUA.png", dragon="https://i.imgur.com/gqhORgQ.png", water="https://i.imgur.com/10Avd13.png", bug="https://i.imgur.com/uefJjFB.png",
                             dark="https://i.imgur.com/2cVK4CQ.png", fighting="https://i.imgur.com/BcjA0cX.png", ghost="https://i.imgur.com/W42sf0Y.png", steel="https://i.imgur.com/6HoeQTO.png", flying="https://i.imgur.com/J2Vsx11.png",
                             electric="https://i.imgur.com/S2ZXBvj.png", fairy="https://i.imgur.com/E7nWQI3.png")


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
    thumbnail = image_type_dictionary[thismove['type']]
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
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text="Created by VisionBot",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    return embed


def display_link(move_name):
    return "[Serebii](" + movedex_url_prefix + ''.join(move_name.lower().rsplit()) + movedex_url_postfix + ")"
