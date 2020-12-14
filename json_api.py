import requests
import os

if os.environ.get("json_api_key"):
    json_api_key = os.environ.get("json_api_key")
else:
    import API_KEYS
    json_api_key = API_KEYS.json_api_key

get_headers = {"secret-key": json_api_key}
put_headers = {"secret-key": json_api_key, "Content-Type": "application/json", "versioning": "false"}
profiles_file = "https://api.jsonbin.io/b/5ed27a4579382f568bcfd675/1"
schedule_file = "https://api.jsonbin.io/b/5ed1939b60775a5685848841"


def put_schedule_json(json):
    r = requests.put(schedule_file, json=json, headers=put_headers)
    print(r.json())
    print("Successfully Updated JSON")


def get_schedule_json():
    return requests.get(schedule_file, headers=get_headers).json()


def put_profiles_json(json):
    r = requests.put(profiles_file, json=json, headers=put_headers)
    print(r.json())
    print("Successfully Updated JSON")


def get_profiles_json():
    return requests.get(profiles_file, headers=get_headers).json()
