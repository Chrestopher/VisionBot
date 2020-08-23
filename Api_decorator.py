"""Use for Api Calls"""
import json
from functools import wraps


class api_call_saver():

    def __init__(self, *, target_file):
        self.target_file = target_file

    def __call__(self, apiCall):

        @wraps(apiCall)
        def callable(callParameter):
            result = apiCall(callParameter)
            data = [result]
            self.appending_to_json(callParameter, data)
            return result
        return callable

    def appending_to_json(self, callParameter, data):
        target = "apicalls/{}.json".format(self.target_file)
        newfile = self.try_reading_json(target)
        with open(target, "w") as outfile:
            newkey = {callParameter: data}
            newfile.update(newkey)
            json.dump(newfile, outfile)
            print("{} has been saved to file".format(callParameter))

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

    target = "apicalls/{}.json".format(target_file)
    try:
        with open(target, "r") as file:
            data = json.loads(file.read())
    except:
        raise Exception("target file not found")
    try:
        return data[query]
    except:
        raise Exception("query not found")

