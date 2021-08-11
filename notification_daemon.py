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
import toast
import threading

def notification(content):
    toast.toast("uumail", content)

class Regularly_notify(threading.Thread):
    def __init__(self,uumail_id,uumail_pass,sync_interval):
        super(Regularly_notify, self).__init__()
        self.id = uumail_id
        self.passwd = uumail_pass
        self.interval = sync_interval
        self.DontNotify_NoMail = False
        self.url = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin"
        self.url_login = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/login_auth"
        self.url_logout = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/logout"
        self.login_data = {
            'login_page_lang': 'ja',
            'charset': 'UTF-8',
            'am_authid': self.id,
            'am_authpasswd': self.passwd,
            'language': 'auto',
            'ajax': 'on'
        }
        self.message = {
            "FAIL_ACSESS"   : "アクセスに失敗しました",
            "WRONG_DATA"    : "IDやパスワードが違う可能性があります",
            "FAIL_GET_INFO" : "情報の取得に失敗しました"
        }
        self.last_info = None
        self.setDaemon(True)
    def get(self):
        # セッションの作成
        session = requests.session()
        try:
            login = session.post(self.url_login, data=self.login_data, timeout=(3.0, 8))
            # ログイン後のソースを取得
            login_redirect_code = login.text

            # 取得したコードのJavascript内にある"self.location.href="のあとのURLを取得
            temp = re.search('self.location.href=\".*?\"', login_redirect_code)
            redirect_url = login_redirect_code[temp.start() + 20: temp.end() - 1]

            time.sleep(3)

            # リダイレクト
            session.get(redirect_url, timeout=(3.0, 8))
        except :
            self.obt_info = self.message["FAIL_ACSESS"]
            return False

        try:
            # urlからセッションIDを取得
            session_id = re.search("[0-9].*", redirect_url)
            session_id = session_id.group()
        except :
            self.obt_info = self.message["WRONG_DATA"]
            return False

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
            self.obt_info = self.message["FAIL_GET_INFO"] 
            return False

        try:
            # logout処理
            logout_url = self.url_logout + "?id=" + session_id
            time.sleep(5)
            logout = session.get(logout_url, timeout=(3.0, 8))
        except:
            self.obt_info = mail_info
            return True

        self.obt_info = mail_info
        return True

    def notify_uumail(self):
        i = 0
        nomail_info = "新着メールはありません"
        while i < 5:
            if self.get():
                print(bool(self.obt_info == nomail_info))
                if not ( ( self.DontNotify_NoMail and (self.obt_info==nomail_info) ) or (self.obt_info == self.last_info) ) :
                    notification(self.obt_info)
                    self.last_info = self.obt_info
                return True
            i += 1
            time.sleep(5)
        # 5回失敗
        notification(self.obt_info)
        return False

    def run(self):
        time_start = time.time()
        i = 0
        while True:
            timer = time.time()
            if timer >= time_start + self.interval * i:
                self.notify_uumail()
                i += 1
            time.sleep(10)

