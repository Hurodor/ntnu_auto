import click
import config
import json

from ntnu import NTNU
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
def g_settings():
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

    # maybe add better debug
    try:
        ntnu.login()
        ntnu.book_room(**settings)
    except Exception:
        click.echo("\nsomething went wrong, \nplease check your settings. ")

    click.echo("Booking complete!")


main.add_command(login)
main.add_command(g_settings)
main.add_command(set_room)
main.add_command(book)
main.add_command(supported_rooms)

if __name__ == '__main__':
    main()
