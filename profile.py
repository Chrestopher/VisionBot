import discord
import json_api

profile_keys = ["color", "bio", "emote", "anime", "pokemon", "game", "waifu", "main", "song"]

def categorylist():
  return ", ".join(profile_keys)

def profile(message):
    content = message.content
    name = message.author.name
    descriptor = message.author.discriminator
    user = name + descriptor
    avatar_url = message.author.avatar_url
    print(avatar_url)
    print(message.author)

    return process_message(user, content, avatar_url)


def process_message(user, content, avatar_url):
    content = content.strip()
    content = content[9:]
    content_splitted = content.split(" ")

    if content_splitted[0] == "update":
        if content_splitted[1] in profile_keys:
            param = content_splitted[1]
            del content_splitted[0]
            del content_splitted[0]
            value = " ".join(content_splitted)
            return update_account(user, param, value)
        else:
            return "That category does not exist! Try one of these: "+categorylist()
    elif content_splitted[0] == "create":
        return create_account(user)
    elif content_splitted[0] == "view":
        return view_account(user, avatar_url)
    else:
        return "That command does not exist!"


def view_account(user, avatar_url):
    profiles = json_api.get_profiles_json()
    if user not in profiles.keys():
        return "You do not have a profile! Use !profile create to make one!"
    print(profiles)
    return construct_embed(user, profiles, avatar_url)


def update_account(user, param, value):
    profiles = json_api.get_profiles_json()
    if user not in profiles.keys():
        return "You need a profile to update your account! use !profile create"
    else:
        profiles[user][param] = value
        json_api.put_profiles_json(profiles)
        return "Your profile has been updated! View your new profile with !profile view"


def create_account(user):
    profiles = json_api.get_profiles_json()
    if user not in profiles.keys():
        color = "0xF2F2FA"
        bio = "N/A"
        emote = "N/A"
        anime = "N/A"
        pokemon = "N/A"
        game = "N/A"
        waifu = "N/A"
        main = "N/A"
        song = "N/A"

        profiles[user] = {}
        profiles[user]["color"] = color
        profiles[user]["bio"] = bio
        profiles[user]["emote"] = emote
        profiles[user]["anime"] = anime
        profiles[user]["pokemon"] = pokemon
        profiles[user]["game"] = game
        profiles[user]["waifu"] = waifu
        profiles[user]["main"] = main
        profiles[user]["song"] = song

        json_api.put_profiles_json(profiles)
        return "Profile was created! Do !profile update {category} {value} to make changes!"
    else:
        return "You already have a profile!"


def construct_embed(user, profiles, avatar_url):
    color_in_string = profiles[user]["color"]
    color_in_int = int(color_in_string, 16)

    bio = profiles[user]["bio"]
    emote = profiles[user]["emote"]
    anime = profiles[user]["anime"]
    pokemon = profiles[user]["pokemon"]
    game = profiles[user]["game"]
    waifu = profiles[user]["waifu"]
    main = profiles[user]["main"]
    song = profiles[user]["song"]

    embed = discord.Embed(title="Bio", colour=discord.Colour(color_in_int),
                          description=bio)

    embed.set_thumbnail(url=avatar_url)
    embed.set_author(name=user[:-4] + "'s Profile")
    embed.set_footer(text="Created by VisionBot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="My favorite emote:", value=emote, inline=False)
    embed.add_field(name="My favorite game:", value=game, inline=False)
    embed.add_field(name="My favorite anime:", value=anime, inline=False)
    embed.add_field(name="My favorite song:", value=song, inline=False)
    embed.add_field(name="My waifu/husbando:", value=waifu, inline=False)
    embed.add_field(name="My favorite pokemon:", value=pokemon, inline=False)
    embed.add_field(name="My smash main(s):", value=main, inline=False)

    return embed
