import click
import config
from ntnu import NTNU

"""
"room_settings": {
    "start_time": "08:00",
    "duration": "04:00",
    "days": 14,
    "area": "Gl\u00c3\u00b8shaugen",


    "building": "Elektro E/F",
    "min_people": 0,
    "room_id": "E204", "description_text": "Studering"}}
"""


# need some more testing
@click.group()
@click.option('-t', '--test')
def main(test):
    click.echo(test)

# choose start time of booking, and duration, duration should be default 4 hours
@click.command()
@click.option('-t', "time", default="08:00")
@click.option('-d', "duration", default="04:00")
def set_time(time, duration):
    config.write_room_settings(start_time=time, duration=duration)


# configure chromedriver, and login info
@click.command()
def setup():
    config.setup()

# todo: choose room and building to lock on if area is invalid, echo valid rooms and promt user to choose
@click.command()
def room():
    pass



main.add_command(room)
main.add_command(setup)
main.add_command(set_time)

if __name__ == '__main__':
    main()












