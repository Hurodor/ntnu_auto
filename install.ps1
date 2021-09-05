pip3 install virtualenv
virtualenv venv
.\venv\Scripts\activate.ps1
pip3 install click, keyring, selenium

$current_path = Get-Location
if (test-path $profile)
{

    Add-Content $profile ("function ntb($args) {
    $current_path\venv\Scripts\python.exe .\$current_path\commands.py $args
}")
}else {
    new-item -path $profile -itemtype file -force

    Add-Content $profile ("function ntb($args) {
    $current_path\venv\Scripts\python.exe .\$current_path\commands.py $args
}")

}