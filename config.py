import keyring
import json
from getpass import getpass
import pathlib

path_to_project_folder = pathlib.Path(__file__).parent.resolve()
json_path = str(path_to_project_folder) + "\settings.json"

chrome_driver_paths = {
    'w': str(path_to_project_folder) + '\drivers\chromedriver_windows.exe',
    'l': 'drivers/chromedriver_linux',
    'm': 'drivers/chromedriver_mac'
}


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
    setup()
