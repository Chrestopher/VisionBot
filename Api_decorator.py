"""Use for Api Calls"""
import json
from functools import wraps


class ApiCallSaver:

    def __init__(self, *, target_file):
        self.target_file = target_file

    def __call__(self, api_call):

        @wraps(api_call)
        def callable(*args):
            result = api_call(*args)
            data = result
            self.appending_to_json(args[0], data)
            return result
        return callable

    def appending_to_json(self, call_parameter, data):
        target = "content/anime/{}.json".format(self.target_file)
        newfile = self.try_reading_json(target)
        with open(target, "w") as outfile:
            newkey = {call_parameter[1]: data}
            newfile.update(newkey)
            json.dump(newfile, outfile)
            print("{} has been saved to file".format(call_parameter))

    def try_reading_json(self, target):
        try:
            with open(target, "r") as infile:
                newfile = json.loads(infile.read())
        except:
            with open(target, 'w') as createfile:
                json.dump({}, createfile)
            with open(target, "r") as infile:
                newfile = json.loads(infile.read())
        return newfile


def pull_from_json(query, target_file):
    target = "content/anime/{}.json".format(target_file)
    try:
        with open(target, "r") as file:
            data = json.loads(file.read())
    except:
        raise Exception("target file not found")

    try:
        return data[query]
    except KeyError:
        raise KeyError

