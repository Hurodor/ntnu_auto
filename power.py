import subprocess
import config


def run(cmd, output=True):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)

    if output:
        if completed.returncode != 0:
            print("An error occured: {}".format(completed.stderr))

        print(completed.stdout.decode())

    return completed


def make_task(time):
    command = """
$action = New-ScheduledTaskAction -Execute "{}\\venv\\Scripts\\python.exe" -Argument "{}\\main.py"
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek @("Monday", "Tuesday", "Wednesday", "Thursday", "Friday") -At {}
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -DontStopOnIdleEnd -RunOnlyIfNetworkAvailable
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "ntnu_auto_booking" -Description "This will enable automaticly room booking at ntnu" -Settings $Settings
""".format(config.path_to_project_folder,
           config.path_to_project_folder,
           time)

    run(command)


def toggle_activation(disable=True):
    command = """{}-ScheduledTask -TaskName "ntnu_auto_booking" """.format("Disable" if disable else "Enable")

    run(command)


def delete_task():
    command = """Unregister-ScheduledTask -TaskName "ntnu_auto_booking" -Confirm:$false"""

    run(command)


def change_trigger(days: list, time):
    """takes in list of days to book on, and time and change task scheduler"""

    days_format = '''"{}", ''' * len(days)
    days_str = "@(" + days_format[:-2] + ")"
    day_str_finished = days_str.format(*days)

    command = """
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek {} -At {}
Set-ScheduledTask -TaskName ntnu_auto_booking" -Trigger $Trigger""
""".format(day_str_finished, time)

    run(command)


def check_if_task_exsists():
    command = """Get-ScheduledTask -TaskName "ntnu_auto_booking" """
    response = run(command, False)

    if response.returncode == 0:
        return True
    return False

def get_task_info():
    command = """Get-ScheduledTaskInfo -TaskName "ntnu_auto_booking" """
    run(command)