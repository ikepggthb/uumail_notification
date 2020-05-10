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
import requests
import time
import re
import datetime
import sys
import subprocess
import win32api
import win32.lib.win32con as win32con

import toast
from setting import passcrypt
from setting import umn_config

CONFIG = umn_config.read_config()

# アカウントデータ取得
try:
    ACCOUNT_DATA = passcrypt.read_data()
except:
    q = win32api.MessageBox(0, u"アカウント情報の取得に失敗しました\nアカウントを設定しますか", u"uumail notification - エラー", win32con.MB_YESNO | win32con.MB_ICONERROR)
    if q == win32con.IDYES:
        umn_config.open_setting()
    win32api.MessageBox(0, u"終了します。", u"uumail notification - エラー", win32con.MB_OK | win32con.MB_ICONERROR)
    sys.exit(1)

ID = ACCOUNT_DATA[0]
PASSWD = ACCOUNT_DATA[1]
SYNC_INTERVAL = 60 * int(CONFIG['sync_interval']) # 秒
URL = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin  "
URL_LOGIN = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/login_auth"
URL_LOGOUT = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/logout"
LOGIN_DATA = {
    'login_page_lang': 'ja',
    'charset': 'UTF-8',
    'am_authid': ID,
    'am_authpasswd': PASSWD,
    'language': 'auto',
    'ajax': 'on'
}

ERROR = {
    "FAIL_ACSESS"   : 1,
    "WRONG_DATA"    : 2,
    "FAIL_GET_INFO" : 3
}
MESSAGE_ERROR = (
    "正常終了",
    "アクセスに失敗しました",
    "IDやパスワードが違う可能性があります",
    "情報の取得に失敗しました"
)

def get_info():
    # セッションの作成
    session = requests.session()
    try:
        login = session.post(URL_LOGIN, data=LOGIN_DATA, timeout=(3.0, 8))
        # ログイン後のソースを取得
        login_redirect_code = login.text

        # 取得したコードのJavascript内にある"self.location.href="のあとのURLを取得
        temp = re.search('self.location.href=\".*?\"', login_redirect_code)
        redirect_url = login_redirect_code[temp.start() + 20: temp.end() - 1]

        time.sleep(3)

        # リダイレクト
        session.get(redirect_url, timeout=(3.0, 8))
    except :
        return ERROR["FAIL_ACSESS"]

    try:
        # urlからセッションIDを取得
        session_id = re.search("[0-9].*", redirect_url)
        session_id = session_id.group()
    except :
        return ERROR["WRONG_DATA"]

    try:
        # homeへアクセス
        time.sleep(3)
        page = session.get(redirect_url.replace("top", "home"))
        # 新着メール情報
        mail_info_code = re.search("<div class=\"mail_recent shadow\">(.|\s)*?</div>", page.text)
        mail_info_code = mail_info_code.group()
        mail_info_code = mail_info_code.replace("\n", "").replace(" ", "")
        mail_info = re.search("<li>.*?</li>", mail_info_code)
        mail_info = mail_info.group()[4:-5]
    except:
        return ERROR["FAIL_GET_INFO"]

    try:
        # logout処理
        logout_url = URL_LOGOUT + "?id=" + session_id
        time.sleep(5)
        logout = session.get(logout_url, timeout=(3.0, 8))
    except:
        return mail_info

    return mail_info

def notification(content):
    dt_now = datetime.datetime.now()
    dt_now_str = dt_now.strftime('%H:%M')
    dt_now_str_all = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    # print(dt_now_str_all, ":",content)
    toast.toast("uumail", content)


def notify_uumail(result_get_info_last):
    i = 0
    while i < 5:
        result_get_info = get_info()
        if type(result_get_info) is str:    # 取得成功したならば
            if result_get_info != result_get_info_last:
                notification(result_get_info)
            return result_get_info
        i += 1
        time.sleep(5)
    # print("5回失敗しました")
    notification(MESSAGE_ERROR[result_get_info])
    return result_get_info

def notify_daemon():
    time_start = time.time()
    i = 0
    last_info = None
    notification("タスクトレイに常駐します。")
    while True:
        timer = time.time()
        if timer >= time_start + SYNC_INTERVAL * i:
            last_info = notify_uumail(last_info)
            i += 1
        time.sleep(10)
notification("タスクトレイに常駐します。")

