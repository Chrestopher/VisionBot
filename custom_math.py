def math(args):
    number_list = []
    if len(args) is not 3:
        return "Please put your numbers in the correct order: number operator number"

    first_number = args[0]
    operation = args[1]
    second_number = args[2]

    if (not first_number.isnumeric()) or (not second_number.isnumeric()):
        return "Please use numbers"

    if operation == "*":
        return str(int(args[0]) * int(args[2]))
    elif operation == "+":
        return str(int(args[0]) + int(args[2]))
    elif operation == "-":
        return str(int(args[0]) - int(args[2]))
    elif operation == "/":
        return str(str(int(args[0]) / int(args[2])))
    elif operation == "^":
        return str(str(int(args[0]) ** int(args[2])))
    else:
        return "Please use a supported operation: * - + /"
