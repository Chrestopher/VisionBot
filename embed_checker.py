import help_command


def embedpageswitch(reaction,embed):

    emoji = reaction.emoji
    direction= 0
    if emoji == "➡️":
        direction = 1
    elif emoji == "⬅️":
        direction = -1
    if embed.title.find("Help")== 0:
        current_page = int(embed.footer.text.split("/")[0])
        if direction == 1 and current_page != 3:
            return help_command.helppages[current_page+1]
        if direction == -1 and current_page != 1:
            return help_command.helppages[current_page-1]
        else:
            return
    else:
        return
