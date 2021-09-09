import os
import json
import keyring
import pathlib
from getpass import getpass


path_to_project_folder = pathlib.Path(__file__).parent.resolve()
json_path = str(path_to_project_folder) + "\settings.json"

chrome_driver_paths = {
    'w': str(path_to_project_folder) + '\drivers\chromedriver_windows.exe',
    'l': 'drivers/chromedriver_linux',
    'm': 'drivers/chromedriver_mac'
}

# this will create settings file
def make_settings_file():
    settings_format = {
        "ntnu": {
            "username": ""
        },
        "driver_path": "",
        "room_settings": {
            "start_time": "08:00",
            "duration": "04:00",
            "days": 14,
            "area": "Gl\u00f8shaugen",
            "building": "Elektro E/F",
            "min_people": 0,
            "room_id": "E204",
            "description_text": "Studering"
        }
    }

    with open(json_path, 'w') as w:
        json.dump(settings_format, w)


# reads settings from settings.json
def get_settings():
    with open(json_path, "r") as fr:
        settings = json.load(fr)

    return settings


def write_room_settings(**kwargs):
    settings = get_settings()

    for key, value in kwargs.items():
        settings['room_settings'][key] = value

    with open(json_path, 'w') as fw:
        json.dump(settings, fw)


# configure username and password
def setup():
    system = input("which operation system are you running on? \n'w' for windows, 'l' for linux, 'm' for mac \n ->")
    username = input('username-> ')
    passwd = getpass("password-> ")

    settings = get_settings()

    if len(username) > 1:
        settings['ntnu']['username'] = username
        keyring.set_password(service_name='ntnu', username=username, password=passwd)

    if system in chrome_driver_paths.keys():
        settings['driver_path'] = chrome_driver_paths[system]

    with open(json_path, "w") as fw:
        json.dump(settings, fw)


class Config:
    settings = get_settings()
    username = settings['ntnu']['username']
    chromedriver = settings['driver_path']


if __name__ == '__main__':
    # if the file does not already exists make it
    if not os.path.isfile(json_path):
        make_settings_file()

    setup()
