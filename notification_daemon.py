# uumail notification
#
# © 2020 Ikkei Yamada All Rights Reserved.
# Twitter: @idkaeti
# Email  : ikeprg@gmail.com

#   Released under the GPLv3 license.
#
#   "uumail_notification" is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   "uumail_notification" is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with "uumail_notification".  If not, see <http://www.gnu.org/licenses/>.
import time
import threading

from PySide6 import QtCore, QtWidgets, QtGui

import get

# 設定、アカウント情報読み込み 
from setting import passcrypt
from setting import umn_config

class Regularly_notify(threading.Thread):
    def __init__(self,systray = None):
        super(Regularly_notify, self).__init__()
        self.systray = systray
        self.setDaemon(True)
    def read_config(self):
        try:
            ACCOUNT_DATA = passcrypt.read_data()
            CONFIG = umn_config.read_config()
            self.id = ACCOUNT_DATA[0]
            self.passwd = ACCOUNT_DATA[1]
            self.interval = 60 * int(CONFIG['sync_interval']) # 秒
            self.DontNotify_NoMail = bool(CONFIG['DontNotify_NoMail'])
            return True
        except:
            return False

    def notification(self,msg,title="uumail",info_type=QtWidgets.QSystemTrayIcon.Information):
        if self.systray is None:
            print(msg)
        else:
            self.systray.showMessage(title, msg,info_type)

    def run(self):
        # init
        uumail_info = get.Get_mail_recent()
        time_start = time.time()
        self.interval = 0
        i = 0

        while True:
            timer = time.time()
            if timer >= time_start + self.interval * i:
                while True:
                    if self.read_config():
                        break
                    time.sleep(3)
                uumail_info.authid = self.id
                uumail_info.password = self.passwd
                uumail_info.run()
                if not ( ( self.DontNotify_NoMail and uumail_info.is_nomail() ) or uumail_info.is_same_before() ) :
                    self.notification(uumail_info.info_mail_recent)
                i += 1
            time.sleep(10)

