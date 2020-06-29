import discord
import os
import random
from discord.ext import commands

import randpoke
import schedule
import custom_math
import generate_data
import profile
import itemdex
import num_util_functions

bot = commands.Bot(command_prefix="!")

# Global Variables
bot_client_id = "691856016333078540"
messages = 0
blacklisted_channels = ["botandvoicechat", "waifu-bot-spam", "slick-dealz", "waifu-bot-rolls"]
joe_messages = generate_data.generate_joe()


@bot.command(name="visionbot")
async def visionbot_command(ctx):
    msg = 'Hello {0.author.mention}! I am VisionBot. I post things that Vision may or may not post. @me for random ' \
          'message or !randpoke for a random pokemon.'.format(ctx.message.author)
    await ctx.send(msg)


@bot.command(name="linkcode")
async def linkcode_command(ctx):
    await ctx.send(num_util_functions.random_linkcode())


@bot.command(name="coinflip")
async def coinflip_command(ctx):
    await ctx.send(num_util_functions.coin_flip())


@bot.command(name="credits")
async def credits_command(ctx):
    msg = "This bot was developed by @Chres, @Khajeet, and @neffrw. Show them some pictures of quints to make their " \
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


@bot.command(name="randpoke")
async def randpoke_command(ctx, *args):
    await ctx.send(randpoke.get_rand_poke(args))


@bot.command(name="profile")
async def profile_command(ctx, *args):
    response = profile.profile(ctx, args)
    if type(response) is discord.embeds.Embed:
        await ctx.send(" ", embed=response)
    elif type(response) is str:
        await ctx.send(response)


@bot.command(name="math")
async def math_command(ctx, *args):
    msg = custom_math.math(args)
    if msg != "":
        await ctx.send(msg)


@bot.command(name="categories")
async def categories_command(ctx):
        msg="The categories for a profile are: "+profile.categorylist()
        await ctx.send(msg)


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

    if messages % 100 == 0:
        await message.channel.send(joe_messages[index])
        return

    await bot.process_commands(message)


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
