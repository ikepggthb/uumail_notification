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

import win32event
import winerror
import pywintypes
import win32api
import sys
import win32.lib.win32con as win32con
import threading
import time #debug
import notification_daemon
import umn_systray

# 多重起動確認
UNIQUE_MUTEX_NAME = 'Global\\MyProgramIsAlreadyRunning'
handle = win32event.CreateMutex(None, pywintypes.FALSE, UNIQUE_MUTEX_NAME)
if not handle or win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    print('既に別のプロセスが実行中です。', file=sys.stderr)
    win32api.MessageBox(0, u"既に常駐しています", u"uumail notification - エラー", win32con.MB_OK | win32con.MB_ICONERROR)
    sys.exit(-1)

thread_notify = threading.Thread(target=notification_daemon.notify_daemon)
thread_notify.setDaemon(True)
thread_notify.start()

umn_systray.task_tray()