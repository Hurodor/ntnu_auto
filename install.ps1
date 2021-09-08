pip3 install virtualenv
virtualenv venv
.\venv\Scripts\activate.ps1
pip3 install click, keyring, selenium

$current_path = Get-Location
$path_to_profile_ntnu_script = "$home\Documents\WindowsPowerShell\Scripts\ntnu_auto.ps1"
if (test-path $profile)
{
    Add-Content $path_to_profile_ntnu_script "$current_path\venv\Scripts\python.exe $current_path\commands.py $args"
    Add-Content $profile "Set-Alias ntb $path_to_profile_ntnu_script"
}else {
    new-item -path $profile -itemtype file -force

    Add-Content $path_to_profile_ntnu_script "$current_path\venv\Scripts\python.exe $current_path\commands.py $args"
    Add-Content $profile "Set-Alias ntb $path_to_profile_ntnu_script"
}

