# uumail notification
# -*- coding: utf-8 -*-
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

class Get_mail_recent():
    """
    get()             : def メール情報の取得をする,
    run([回数])       : def メール情報の取得を複数回繰り返す,
    info_mail_recent  : str 取得したメール情報,
    """
    def __init__(self,authid="",password=""):
        super().__init__()
        self.url = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin"
        self.url_login = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/login_auth"
        self.url_logout = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/logout"
        self.fail_message = {
            "FAIL_ACSESS"   : "アクセスに失敗しました",
            "WRONG_DATA"    : "IDやパスワードが違う可能性があります",
            "FAIL_GET_INFO" : "情報の取得に失敗しました"
        }
        self.authid = authid
        self.password = password
        self.info_mail_recent = "メール情報の取得をしていません"
        self.info_mail_prev = ""
    def gen_login_deta(self):
        login_data = {
            'login_page_lang': 'ja',
            'charset': 'UTF-8',
            'am_authid': self.authid,
            'am_authpasswd': self.password,
            'language': 'auto',
            'ajax': 'on'
        }
        return login_data
    def get(self):
        """
        メール情報の取得をする,
        返り値:bool,
        変数info_mail_recentへ保存
        """
        # セッションの作成
        session = requests.session()
        try:
            login_data = self.gen_login_deta()
            login = session.post(self.url_login, data=login_data, timeout=(3.0, 8))
            # ログイン後のソースを取得
            login_redirect_code = login.text

            # 取得したコードのJavascript内にある"self.location.href="のあとのURLを取得
            temp = re.search('self.location.href=\".*?\"', login_redirect_code)
            redirect_url = login_redirect_code[temp.start() + 20: temp.end() - 1]

            # time.sleep(0.5)

            # リダイレクト
            session.get(redirect_url, timeout=(3.0, 8))
        except :
            self.info_mail_recent = self.fail_message["FAIL_ACSESS"]
            return False

        try:
            # urlからセッションIDを取得
            session_id = re.search("[0-9].*", redirect_url)
            session_id = session_id.group()
        except :
            self.info_mail_recent = self.fail_message["WRONG_DATA"]
            return False

        try:
            # homeへアクセス
            # time.sleep(0.5)
            page = session.get(redirect_url.replace("top", "home"))
            # 新着メール情報
            mail_info_code = re.search("<div class=\"mail_recent shadow\">(.|\s)*?</div>", page.text)
            mail_info_code = mail_info_code.group()
            mail_info_code = mail_info_code.replace("\n", "").replace(" ", "")
            mail_info = re.search("<li>.*?</li>", mail_info_code)
            mail_info = mail_info.group()[4:-5]
        except:
            self.info_mail_recent = self.fail_message["FAIL_GET_INFO"] 
            return False

        try:
            # logout処理
            logout_url = self.url_logout + "?id=" + session_id
            # time.sleep(0.5)
            logout = session.get(logout_url, timeout=(3.0, 8))
        except:
            self.info_mail_recent = mail_info
            return True

        self.info_mail_recent = mail_info
        return True

    def run(self,count = 5):
        """
        メール情報の取得が成功するまで複数回繰り返す,
        返り値:bool,
        変数"info_mail_recent"へ保存
        """
        self.info_mail_prev = self.info_mail_recent
        self.last_count = 0
        while self.last_count < 5:
            if self.get():
                return True
            self.last_count += 1
            time.sleep(5)
        return False

    def is_same_before(self):
        return  self.info_mail_prev == self.info_mail_recent
    def is_nomail(self):
        return self.info_mail_recent == "新着メールはありません"