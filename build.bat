pyinstaller --onefile  --icon=icon/uumail.ico uumail_notification.py --hidden-import pkg_resources --hidden-import infi.systray
cd setting
pyinstaller --noconsole --icon=../icon/uumail.ico setting.py
cd ..
rmdir build_uumail
mkdir build_uumail
mkdir build_uumail\setting
mkdir build_uumail\icon
mkdir build_uumail\toast
xcopy /y dist build_uumail
xcopy /y /E setting\dist\setting build_uumail\setting
xcopy /y toast build_uumail\toast
xcopy /y icon build_uumail\icon
xcopy /y setting\settings.png build_uumail\setting
xcopy /y setting\startup.vbs build_uumail\setting
