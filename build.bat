pyinstaller --onefile --noconsole --icon=icon/uumail.ico exit.py
pyinstaller --onefile --noconsole --icon=icon/uumail.ico uumail_notification.py
cd setting
pyinstaller --noconsole --icon=../icon/uumail.ico setting.py
cd ..
rmdir build_uumail
mkdir build_uumail
mkdir build_uumail\setting
mkdir build_uumail\icon
mkdir build_uumail\toast
xcopy dist build_uumail
xcopy /E setting\dist\setting build_uumail\setting
xcopy toast build_uumail\toast
xcopy icon build_uumail\icon
xcopy setting\settings.png build_uumail\setting
xcopy setting\startup.vbs build_uumail\setting
