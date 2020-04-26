import requests
import time
import re
import datetime
from getpass import getpass
import toast

# -*- coding: utf-8 -*-

ID = input('Input your ID: ')
PASSWD = getpass('Input your Password: ')
URL = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin  "
URL_LOGIN = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/login_auth"
URL_LOGOUT = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/logout"
OFTEN = 60 * 60 * 1 # 通知を確認する頻度(秒)
LOGIN_DATA = {
    'login_page_lang': 'ja',
    'charset': 'UTF-8',
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
    try:
        response = session.get(URL, timeout=(3.0, 8))
        # ログインurlにdataをPOST
        login = session.post(URL_LOGIN, data=LOGIN_DATA, timeout=(3.0, 8))
        # ログイン後のソースを取得
        login_redirect_code = login.text

        # 取得したコードのJavascript内にある"self.location.href="のあとのURLを取得
        temp = re.search('self.location.href=\".*?\"', login_redirect_code)
        redirect_url = login_redirect_code[temp.start() + 20: temp.end() - 1]

        # リダイレクト
        session.get(redirect_url, timeout=(3.0, 8))
    except :
        return FAIL_ACSESS

    try:
        # urlからセッションIDを取得
        session_id = re.search("[0-9].*", redirect_url)
        session_id = session_id.group()
    except :
        return WRONG_DATA

    try:
        # homeへアクセス
        page = session.get(redirect_url.replace("top", "home"))
        # 新着メール情報
        mail_info_code = re.search("<div class=\"mail_recent shadow\">(.|\s)*?</div>", page.text)
        mail_info_code = mail_info_code.group()
        mail_info_code = mail_info_code.replace("\n", "")
        mail_info_code = mail_info_code.replace(" ", "")
        mail_info = re.search("<li>.*?</li>", mail_info_code)
        mail_info = mail_info.group()[4:-5]
    except:
        return FAIL_GET_INFO

    # logout処理
    logout_url = URL_LOGOUT + "?id=" + session_id
    logout = session.get(logout_url, timeout=(3.0, 8))

    return mail_info

def uumail():
    i = 0
    while i < 5:
        result_get_info = get_info()
        dt_now = datetime.datetime.now()
        dt_now_str = dt_now.strftime('%H:%M')
        dt_now_str_all = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')

        if type(result_get_info) is str: # もし、get_info関数がエラーならば、その返り値は整数型
            print(dt_now_str_all, ":",result_get_info)
            toast.toast("uumail",result_get_info)
            return
        else : # get_info関数がエラー
            print(dt_now_str_all, ":",MESSAGE_ERROR[result_get_info])
            toast.toast("uumail",MESSAGE_ERROR[result_get_info])
        i += 1
        time.sleep(3)
    print("5回失敗しました")

time_start = time.time()
i = 0
while True:
    timer = time.time()
    if timer >= time_start + OFTEN * i:
        uumail()
        i += 1
    time.sleep(10)
