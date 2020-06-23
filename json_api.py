import requests
import API_KEYS

get_headers = {"secret-key": API_KEYS.json_api_key}
put_headers = {"secret-key": API_KEYS.json_api_key, "Content-Type": "application/json", "versioning": "false"}
profiles_file = API_KEYS.profiles_file
schedule_file = API_KEYS.schedule_file


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
