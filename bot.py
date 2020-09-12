import discord
import os
import random
from discord.ext import commands
import schedule
import custom_math
import generate_data
import profile
import itemdex
import pokedex
import num_util_functions
import randpoke
import help_command
import embed_page_handler
import movedex
import joe_methods
import anime

bot = commands.Bot(command_prefix="!")

# Global Variables
bot_client_id = "691856016333078540"
messages = 0
blacklisted_channels = ["botandvoicechat", "waifu-bot-spam", "slick-dealz", "waifu-bot-rolls"]
joe_messages = generate_data.generate_joe()
joe_keywords = generate_data.generate_joe_keyword_list()


@bot.command(name="visionbot")
async def visionbot_command(ctx):
    msg = 'Hello {}! I am VisionBot. I post things that Vision may or may not post. @me for random ' \
          'message or !help for a list of commands'.format(ctx.message.author.mention)
    await ctx.send(msg)


@bot.command(name="linkcode")
async def linkcode_command(ctx):
    await ctx.send(num_util_functions.random_linkcode())


@bot.command(name="coinflip")
async def coinflip_command(ctx):
    await ctx.send(num_util_functions.coin_flip())


@bot.command(name="credits")
async def credits_command(ctx):
    msg = "This bot was developed by @Chres, @Khajeet, @neffrw, @Big Bass. Show them some pictures of quints to make their " \
          "day! "
    await ctx.send(msg)


@bot.command(name="schedule")
async def schedule_command(ctx):
    await ctx.send(schedule.read_schedule())


@bot.command(name="addevent")
async def addevent_command(ctx, *args):
    await ctx.send(schedule.add_event(args))


@bot.command(name="removeevent")
async def removeevent_command(ctx, *args):
    await ctx.send(schedule.remove_event(args))


@bot.command(name="itemdex")
async def itemdex_command(ctx, *args):
    response = itemdex.get_item(args)
    if type(response) is discord.embeds.Embed:
        await ctx.send(" ", embed=response)
    elif type(response) is str:
        await ctx.send(response)


@bot.command(name="pokedex")
async def pokedex_command(ctx, *args):
    response = pokedex.get_pokemon(args)
    if type(response) is discord.embeds.Embed:
        message = await ctx.send(" ", embed=response)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
    elif type(response) is str:
        await ctx.send(response)


@bot.command(name='movedex')
async def movedex_command(ctx, *args):
    response = movedex.get_move(args)
    if type(response) == discord.embeds.Embed:
        await ctx.send(' ', embed=response)
    elif type(response) == str:
        await ctx.send(response)


@bot.command(name="randpoke")
async def randpoke_command(ctx, *args):
    await ctx.send(randpoke.get_rand_poke(args))


@bot.command(name="choose")
async def randpoke_command(ctx, *args):
    args = " ".join(args)
    args = args.split(",")
    await ctx.send(num_util_functions.choose_randomly(args))


@bot.command(name="profile")
async def profile_command(ctx, *args):
    response = profile.profile(ctx, args)
    if type(response) is discord.embeds.Embed:
        await ctx.send(" ", embed=response)
    elif type(response) is str:
        await ctx.send(response)


@bot.command(name="categories")
async def categories_command(ctx):
    await ctx.send("The possible profile categories are: " + profile.category_list())


@bot.command(name="math")
async def math_command(ctx, *args):
    msg = custom_math.math(args)
    if msg != "":
        await ctx.send(msg)


@bot.command(name="simonsays")
async def simonsays_command(ctx, *args):
    msg = " ".join(args)
    await ctx.send(msg)


@bot.command(name="animechar")
async def animechar_command(ctx, *args):
    msg = anime.char_pic(args)
    await ctx.send(msg)


@bot.command(name="anime")
async def anime_command(ctx, *args):
    response = anime.anime_stats(args)
    if type(response) is discord.embeds.Embed:
        message = await ctx.send(" ", embed=response)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
    elif type(response) is str:
        await ctx.send(response)


@bot.command(name="commands")
async def commands_command(ctx, *args):
    if len(args) == 0:
        response = help_command.start_help_command()
    elif args[0].isdigit() and 3 >= int(args[0]) >= 1:
        response = help_command.start_help_command_at_page(int(args[0]))
    else:
        await ctx.send("This page does not exist!")
        return
    message = await ctx.send(" ", embed=response)
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")


@bot.event
async def on_message(message):
    if str(message.channel) in blacklisted_channels:
        return

    if message.author == bot.user:
        return

    index = random.randint(0, 2574)

    if bot_client_id in str(message.content):
        mention = '{0.author.mention} '.format(message)
        final_message = mention + str(joe_messages[index])
        await message.channel.send(final_message)
        return

    global messages
    messages += 1

    for word in joe_keywords:
        if word in message.content:
            if random.randint(0, 10) > 9:
                await message.add_reaction(joe_methods.get_joe_emote_response())
            else:
                await message.channel.send(joe_methods.get_joe_keyword_response())
            return

    if messages % 100 == 0:
        await message.channel.send(joe_messages[index])
        return

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    if len(reaction.message.embeds) > 0:
        embed = embed_page_handler.page_flip_handler(reaction, reaction.message.embeds[0])
        await reaction.message.edit(embed=embed)
    return


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


if os.environ.get("bot_cli_key"):
    bot_cli_key = os.environ.get("bot_cli_key")
else:
    import API_KEYS

    bot_cli_key = API_KEYS.bot_cli_key

bot.run(bot_cli_key)
