import discord

helppages = dict([(1, discord.Embed(title="Help Profile", colour=discord.Colour(int("FF0000", 16)))),
                  (2, discord.Embed(title="Help Pokemon", colour=discord.Colour(int("3B4CCA", 16)))),
                  (3, discord.Embed(title="Help Gadgets", colour=discord.Colour(int("FFDE00", 16)))),
                  (4, discord.Embed(title="Help Anime", colour=discord.Colour(int("008000", 16))))])

# Help Page 1
helppages[1].set_footer(text="\t\t\t\t1/4")
helppages[1].add_field(name="profile create", value="Creates a new profile for you, with all categories filled as N/A",
                       inline=False)
helppages[1].add_field(name="profile view", value="View your current profile", inline=False)
helppages[1].add_field(name="profile update [category] {value}", value="Changes the value in a chosen category to a " \
                                                                       "new one", inline=False)
helppages[1].add_field(name="categories", value="Lists all categories")

# Help Page 2
helppages[2].set_footer(text="\t\t\t\t2/4")
helppages[2].add_field(name="randpoke [generation]", value="Prints a random pokemon, and you may optionally include a "
                                                           "generation to pull a pokemon from a specific generation",
                       inline=False)
helppages[2].add_field(name="pokedex", value="Coming Soon!", inline=False)
helppages[2].add_field(name="itemdex [item name]", value="Search for a specific item", inline=False)
helppages[2].add_field(name="linkcode", value="Generates random link codes", inline=False)

# Help page 3
helppages[3].set_footer(text="\t\t\t\t3/4")
helppages[3].add_field(name="visionbot", value="An introduction to joebot", inline=False)
helppages[3].add_field(name="math [number] {operator} [number]", value="A simple math program", inline=False)
helppages[3].add_field(name="coinflip", value="Flips a coin", inline=False)
helppages[3].add_field(name="credits", value="Prints the credits for the bot's developement", inline=False)
helppages[3].add_field(name="simonsays [anything]", value="Makes visionbot repeat whatever you say", inline=False)

# Help page 4
helppages[4].set_footer(text="\t\t\t\t4/4")
helppages[4].add_field(name="animechar [character]", value="Searches and displays a picture of a specified anime/manga character", inline=False)
helppages[4].add_field(name="anime [anime name]", value="Searches and displays an anime with info like summary, stats, scores, etc", inline=False)

def start_help_command():
    return helppages[1]


def start_help_command_at_page(page):
    return helppages[page]
