import click
import config
import json

from ntnu import NTNU
import power
from supported_settings import default_room_settings as df_sett
from supported_settings import valid_room_settings as valid_sett


def take_input(text):
    value = input(text)
    if len(value) < 1:
        return None

    return value


# this is used in setting room paramteres
def room_settings_walkthrough():
    click.echo("Please choose settings, press enter to skip setting. \n")

    settings = config.get_settings()['room_settings']
    for key, value in settings.items():
        click.echo(f"\nCurrent {key} = {value}")
        inpt = take_input(f"new {key}: ")
        if inpt:
            settings[key] = inpt

    return settings


@click.group()
def main():
    pass


# Prints out current settings
@click.command()
def get_settings():
    """Print out current settings for choosing room"""
    current_settings = config.get_settings()
    printstr = ""
    for key, value in current_settings['room_settings'].items():
        printstr += f"  {key} --> {value} \n"
    click.echo(printstr)


@click.command()
def supported_rooms():
    """Print out what rooms that is currently implemented """
    message = ""
    for i in valid_sett:
        # loop trough areas
        for area, buildings in i.items():
            message += area + ":\n    "
            # loop trough buildings
            for building, rooms in buildings.items():
                message += building + "\n       "
                # loop trough rooms
                for room, data in rooms.items():
                    message += room + "\n       "
    message = message[:-4]

    # prints formated string
    click.echo(f"{message}")


# this sets all the room paramteres
@click.command()
@click.option("--default/--no-default", '-d/-nd', default=False)
def set_room(default):
    """Change room settings"""
    if default:
        settings = df_sett
    else:
        settings = room_settings_walkthrough()
        confirmation = input(f"\nYou have selected:  "
                             f"{settings} \n"
                             f"Are you sure? (y/n): \n")

        if confirmation == "n":
            click.echo("\nAborted! ")
            return
    config.write_room_settings(**settings)


# configure chromedriver, and login info
@click.command()
def login():
    """provide login information to log in to NTNU,
        has to be done in order for program to work"""

    config.setup()


@click.command()
@click.option("--debug/--no-debug", "-d/-nd", default=False)
def book(debug):
    """This will try book your room based on given room-settings"""
    ntnu = NTNU()
    settings = config.get_settings()['room_settings']

    # Has to be opposite of debug because of how login function is designed
    ntnu.login(not debug)
    try:
        ntnu.book_room(**settings)
    except Exception:
        ntnu.driver.quit()


@click.command()
@click.option('--time', '-t', prompt="You have to choose time: ")
def setup_auto(time):
    """Set up auto booking, if the auto booking is already initialized you can change days and time to auto book on"""
    if power.check_if_task_exsists():

        # prompt for choosing days
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        print("Spesify with days you want to auto book on (y/n) (default = yes): \n")
        for day in days:
            decision = take_input(day + ": ")
            if not decision or decision == "y":
                continue
            days.remove(day)

        # this updates the schedualed task
        power.change_trigger(days=days, time=time)
        return

    # Create task if there is no allready exsisting
    power.make_task(time)


@click.command()
def auto_delete():
    """deletes the auto booking from system"""
    desicison = input("Are you sure? (y/n) defalut=y")
    if desicison == "n":
        return

    power.delete_task()


@click.command()
@click.option("--enable/--disable", '-e/-d')
def auto_activation(enable):
    """enable or disable auto booking (--enable/--disable) (-e/-d)"""
    if enable:
        power.toggle_activation(False)
        return

    power.toggle_activation()

@click.command()
def auto_info():
    """Gives info of auto booking task, mostly used to debug"""
    if power.check_if_task_exsists():

        power.get_task_info()
        return

    print("There has not been made a task yet")



main.add_command(login)
main.add_command(get_settings)
main.add_command(set_room)
main.add_command(book)
main.add_command(supported_rooms)
main.add_command(setup_auto)
main.add_command(auto_delete)
main.add_command(auto_activation)
main.add_command(auto_info)

if __name__ == '__main__':
    main()
