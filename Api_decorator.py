import json


class api_call_saver():

    def __init__(self, apiCall):
        self.function = apiCall

    def __call__(self, callParameter):

        result = self.function(callParameter)
        data = [result]
        with open("apicalls/{}.json".format(callParameter), "w") as outfile:
            json.dump(data, outfile)
            print("{} has been saved to file".format(callParameter))


def pull_from_json(query):
    try:
        with open("apicalls/{}.json".format(query)) as file:
            data = json.load(file)
            return data
    except:
        raise Exception("query not found")


print(pull_from_json("2"))
