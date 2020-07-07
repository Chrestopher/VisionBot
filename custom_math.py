def math(args):
    number_list = []
    if len(args) is not 3:
        return "Please put your numbers in the correct order: number operator number"
    try:
        first_number = int(args[0])
        second_number = int(args[2])
    except ValueError:
        return "Please use real numbers."
    operation= args[1]


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
