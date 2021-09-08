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
    current_settings = config.get_settings()
    printstr = ""
    for key, value in current_settings['room_settings'].items():
        printstr += f"  {key} --> {value} \n"
    click.echo(printstr)


@click.command()
def supported_rooms():
    json_formatted_str = json.dumps(valid_sett, indent=2)
    click.echo(f"Current supported rooms (on rooms lock at key, not value):\n{json_formatted_str}")


# this sets all the room paramteres
@click.command()
@click.option("--default/--no-default", '-d/-nd', default=False)
def set_room(default):
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
    config.setup()


@click.command()
def book():
    ntnu = NTNU()
    settings = config.get_settings()['room_settings']

    # debug?
    ntnu.login()
    ntnu.book_room(**settings)


@click.command()
@click.option('--time', '-t', prompt="You have to choose time: ")
def setup_auto(time):
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
    desicison = input("Are you sure? (y/n) defalut=y")
    if desicison == "n":
        return

    power.delete_task()


@click.command()
@click.option("--enable/--disable", '-e/-d')
def toogle_active(enable):
    if enable:
        power.toggle_activation(False)

    power.toggle_activation()


main.add_command(login)
main.add_command(get_settings)
main.add_command(set_room)
main.add_command(book)
main.add_command(supported_rooms)
main.add_command(setup_auto)
main.add_command(auto_delete)
main.add_command(toogle_active)

if __name__ == '__main__':
    main()
