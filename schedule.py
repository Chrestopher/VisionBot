import json_api
from datetime import datetime, timedelta

month_word_to_number = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
                        "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
month_number_to_word = {v: k for k, v in month_word_to_number.items()}


def load_json():
    return json_api.get_schedule_json()


def write_json(data):
    return json_api.put_schedule_json(data)


def read_schedule():
    schedule = load_json()["schedule"]

    list_of_events = []
    for k, v in schedule.items():
        list_of_events.append((k, v[0], v[1], v[2]))
    list_of_events.sort(key=lambda x: (x[1], x[2]))

    is_today = False
    title = "Schedule: \n\n"
    for element in list_of_events:
        today_month = datetime.now().date().month
        datetime_in_utc = datetime.utcnow()
        datetime_in_est = datetime_in_utc - timedelta(hours=3)
        today_day = datetime_in_est.day
        event_name = element[0]
        event_month = element[1]
        event_day = element[2]
        event_time = element[3]

        if type(event_month) is int or event_month.isnumeric():
            event_month = month_number_to_word[int(event_month)]

        if today_day is int(event_day) and today_month is month_word_to_number[event_month]:
            is_today = True
        else:
            is_today = False

        if is_today:
            event_text = event_name + " - " + event_month + " " + event_day + " " + event_time + " (TODAY)\n"
        else:
            event_text = event_name + " - " + event_month + " " + event_day + " " + event_time + "\n"
        title += event_text

    return title


def add_event(content):
    content = content.strip()
    content = content[10:]
    content = content.split(" ")

    event_name = content[0]
    event_month = content[1]
    if event_month not in month_word_to_number.keys() and int(event_month) not in month_number_to_word.keys():
        return "The event has an invalid date!"
    if not event_month.isnumeric() and event_month in month_word_to_number.keys():
        event_month = str(month_word_to_number[event_month])

    event_day = content[2]
    event_time = content[3]

    schedule = load_json()
    if event_name in schedule["schedule"].keys():
        return "Event is already in the schedule!"
    else:
        event_name = event_name.replace("_", " ")
        schedule["schedule"][event_name] = []
        schedule["schedule"][event_name].append(event_month)
        schedule["schedule"][event_name].append(event_day)
        schedule["schedule"][event_name].append(event_time)
        write_json(schedule)
        return "Added event \"" + event_name + "\"!"


def remove_event(content):
    content = content.strip()
    event_name = content[13:]
    schedule = load_json()
    if event_name in schedule["schedule"]:
        del schedule["schedule"][event_name]
        write_json(schedule)
        return "The event \"" + event_name + "\" was deleted!"
    else:
        return "The event \"" + event_name + "\" was not in the schedule!"
