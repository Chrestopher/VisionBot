def math(content):
    number_list = []
    content = content.strip()
    content = content[6:]
    content = content.split(" ")
    operation = ""
    if len(content) > 3:
        return "Sorry, im only programmed to do basic math. Idk go use a real calculator instead of this shabby one " \
               "that Chres put on my system lol "

    if content[1] and content[1].isnumeric():
        return "Please put your numbers in the correct order: number operator number"

    for item in content:
        if item.isnumeric():
            number_list.append(int(item))
        elif item in ["*", "+", "-", "/"]:
            operation = item
        else:
            return "Sorry, that doesn't look like math. Please put your numbers in the correct order: number operator " \
                   "number "

    if operation == "*":
        return str(number_list[0] * number_list[1])
    elif operation == "+":
        return str(number_list[0] + number_list[1])
    elif operation == "-":
        return str(number_list[0] - number_list[1])
    elif operation == "/":
        return str(number_list[0] / number_list[1])
    else:
        return "Please put your numbers in the correct order: number operator number"
