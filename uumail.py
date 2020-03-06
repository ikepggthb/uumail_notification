import requests
import time
import re
import datetime
#import threading
#import wx

# -*- coding: utf-8 -*-

ID = ""
PASSWD = ""
URL = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin  "
URL_LOGIN = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/login_auth"
URL_LOGOUT = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/logout"
OFTEN = 60 * 60 * 1
LOGIN_DATA = {
    'login_page_lang': 'ja',
    'charset': 'UTF-8',
    'http_user_agent': 'value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"',
    'am_authid': ID,
    'am_authpasswd': PASSWD,
    'language': 'auto',
    'ajax': 'on'
}
FAIL_ACSESS = 1
WRONG_DATA = 2
FAIL_GET_INFO = 3
MESSAGE_ERROR = (
    "正常終了",
    "アクセスに失敗しました",
    "IDやパスワードが違う可能性があります",
    "情報の取得に失敗しました"
)


def get_info():
    # セッションの作成
    session = requests.session()
    response = session.get(URL)

    # ログインurlにdataをPOST
    login = session.post(URL_LOGIN, data=LOGIN_DATA)
    if login.status_code != 200:
        return FAIL_ACSESS

    # ログイン後のソースを取得
    login_redirect_code = login.text

    # 取得したコードのJavascript内にある"self.location.href="のあとのURLを取得
    temp = re.search('self.location.href=\".*?\"', login_redirect_code)
    if temp is None:
        return FAIL_ACSESS
    redirect_url = login_redirect_code[temp.start() + 20: temp.end() - 1]

    # リダイレクト
    session.get(redirect_url)

    # urlからセッションIDを取得
    session_id = re.search("[0-9].*", redirect_url)
    if session_id is None:
        return WRONG_DATA  # ここで間違った場合、IDやパスワードが間違っている事が多い
    session_id = session_id.group()

    time.sleep(1)

    # homeへアクセス
    page = session.get(redirect_url.replace("top", "home"))
    if page.status_code != 200:
        return FAIL_GET_INFO

    # 新着メール情報
    mail_info_code = re.search("<div class=\"mail_recent shadow\">(.|\s)*?</div>", page.text)
    if mail_info_code is None:
        return FAIL_GET_INFO
    mail_info_code = mail_info_code.group()
    mail_info_code = mail_info_code.replace("\n", "")
    mail_info_code = mail_info_code.replace(" ", "")
    mail_info = re.search("<li>.*?</li>", mail_info_code)
    if mail_info is None:
        return FAIL_GET_INFO
    mail_info = mail_info.group()[4:-5]

    time.sleep(1)

    # logout処理
    logout_url = URL_LOGOUT + "?id=" + session_id
    logout = session.get(logout_url)

    return mail_info

def uumail():
    i = 0
    while True:
        result_get_info = get_info()
        dt_now = datetime.datetime.now()

        print(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'), ":", end="")

        success_get_info = type(result_get_info) is str
        if success_get_info:
            print(result_get_info)
            break

        MESSAGE_ERROR[result_get_info]

        i += 1
        if i >= 5:
            print("5回失敗しました")
            break

        time.sleep(3)

i = 0
time_start = time.time()
while True:
    timer = time.time()
    if timer >= time_start + OFTEN * i:
        uumail()
        i += 1
    time.sleep(10)
