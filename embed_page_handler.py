import help_command


def page_flip_handler(reaction, embed):
    emoji = reaction.emoji
    direction = 0
    if emoji == "➡️":
        direction = 1
    elif emoji == "⬅️":
        direction = -1
    return page_flip_commands(embed, direction)


def page_flip_commands(embed, direction):
    if "Help" in embed.title:
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
    else:
        pass
    print(type(embed.title))