import discord
import os
import random
import schedule
import randpoke
import custom_math
import generate_data
import profile
import itemdex
import num_util_functions

client = discord.Client()

# Global Variables
bot_client_id = "691856016333078540"
messages = 0
blacklisted_channels = ["botandvoicechat", "waifu-bot-spam", "slick-dealz", "waifu-bot-rolls"]
joe_messages = generate_data.generate_joe()

async def command_checker(message):
    if message.content.startswith('!visionbot'):
        msg = 'Hello {0.author.mention}! I am VisionBot. I post things that Vision may or may not post. @me for random message or !randpoke for a random pokemon.'.format(
            message)
        await message.channel.send(msg)
        return

    if message.content.startswith("!randpoke"):
        msg = randpoke.get_rand_poke(message.content)
        await message.channel.send(msg)
        return

    if message.content.startswith("!linkcode"):
        await message.channel.send(num_util_functions.random_linkcode())
        return

    if message.content.startswith("!coinflip"):
        coin_flip = random.randint(1, 1000)
        if coin_flip > 500:
            await message.channel.send("heads")
        else:
            await message.channel.send("tails")
        return

    if message.content.startswith("!math"):
        msg = custom_math.math(message.content)
        if msg != "":
            await message.channel.send(msg)
        return

    if message.content.startswith("!profile"):
        response = profile.profile(message)
        if type(response) is not str:
            embed = response
            await message.channel.send(" ", embed=embed)
        else:
            msg = response
            await message.channel.send(msg)
        return

    if message.content.startswith("!credits"):
        msg = "This bot was made by @Chres. Show him some pictures of quints to make his day!"
        await message.channel.send(msg)
        return

    if message.content.startswith("!itemdex"):
        response = itemdex.get_item(message)
        if type(response) is not str:
            embed = response
            await message.channel.send(" ", embed=embed)
        else:
            msg = response
            await message.channel.send(msg)
        return

    if message.content.startswith("!schedule"):
        await message.channel.send(schedule.read_schedule())
        return

    if message.content.startswith("!addevent"):
        msg = schedule.add_event(message.content)
        await message.channel.send(msg)
        return

    if message.content.startswith("!removeevent"):
        msg = schedule.remove_event(message.content)
        await message.channel.send(msg)
        return
    if message.content.startswith("!categories"):
        msg="The categories for a profile are: "+profile.categorylist()
        await message.channel.send(msg)
        return
    if message.content.startswith("!testrun"):
        msg = "This command is meant for debugging and testing."
        await message.channel.send(msg)
        return
@client.event
async def on_message(message):
    if str(message.channel) in blacklisted_channels:
        return

    if message.author == client.user:
        return

    await command_checker(message)

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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


if os.environ.get("bot_cli_key"):
    bot_cli_key = os.environ.get("bot_cli_key")
else:
    import API_KEYS
    bot_cli_key = API_KEYS.bot_cli_key

client.run(bot_cli_key)
