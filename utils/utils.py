import json
from typing import Any, Dict
from ics import Calendar, Event
from datetime import datetime
import pytz
import os

tz = pytz.timezone("Asia/Shanghai")


def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as f:
        return json.load(f)
    

def save_json(data, file_path: str) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def JSON2ICS(data: Dict[str, Any], timetable:Dict[str, Dict[str, str]], save_path: str) -> None:
    c = Calendar()
    for weeks in data.values():
        for days, events in weeks.items():
            for event in events:
                e = Event()
                e.name = event['course_name'] + ' ' + event['course_id']
                start = days + ' ' + timetable[str(event['lessArr'][0])]['start']
                end = days + ' ' + timetable[str(event['lessArr'][-1])]['end']
                e.begin = tz.localize(datetime.strptime(start, '%Y-%m-%d %H:%M:%S'))
                e.end = tz.localize(datetime.strptime(end, '%Y-%m-%d %H:%M:%S'))
                e.location = event['location']
                e.description = event['course_id']
                c.events.add(e)
    with open(save_path, 'w') as f:
        f.writelines(c)

def JSON2CSV(data: Dict[str, Any], timetable:Dict[str, Dict[str, str]], save_path: str) -> None:
    pass

def mkdirp(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)