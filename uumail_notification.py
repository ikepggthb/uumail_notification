import requests
import time
import re
import datetime
import toast
import passcrypt
import tkinter
from tkinter import messagebox
import sys
import json
import subprocess

# -*- coding: utf-8 -*-

root = tkinter.Tk()
root.withdraw()
try:
    data = passcrypt.read_data()
except:
    q = messagebox.askquestion('uumail_notification - エラー', 'アカウント情報の取得に失敗しました\nアカウントを設定しますか')
    if q == "yes":
        cmd = "account.exe"
        subprocess.Popen(cmd, shell=True)
    messagebox.showinfo('uumail_notification - エラー',  '終了します')
    sys.exit()
try:
    # 設定ファイルの読み込み
    with open('settings/config.json') as f:
        config = json.load(f)
except:
    # 初期設定
    config = {'sync_interval': '60'}

ID = data[0]
PASSWD = data[1]
sync_interval = 60 * int(config['sync_interval']) # 通知を確認する頻度(秒)

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
        time.sleep(3)
        login = session.post(URL_LOGIN, data=LOGIN_DATA, timeout=(3.0, 8))
        # ログイン後のソースを取得
        login_redirect_code = login.text

        # 取得したコードのJavascript内にある"self.location.href="のあとのURLを取得
        temp = re.search('self.location.href=\".*?\"', login_redirect_code)
        redirect_url = login_redirect_code[temp.start() + 20: temp.end() - 1]

        time.sleep(5)

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
        time.sleep(5)
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
    print(dt_now_str_all, ":",content)
    toast.toast("uumail", content)


def uumail(result_get_info_last):
    i = 0
    while i < 5:
        result_get_info = get_info()
        if type(result_get_info) is str:    #　取得成功したならば
            if result_get_info != result_get_info_last:
                notification(result_get_info)
            return result_get_info
        i += 1
        time.sleep(5)
    print("5回失敗しました")
    notification(MESSAGE_ERROR[result_get_info])
    return result_get_info



time_start = time.time()
i = 0
last_info = None
notification("メールの監視を開始します")
while True:
    timer = time.time()
    if timer >= time_start + sync_interval * i:
        last_info = uumail(last_info)
        i += 1
    time.sleep(10)
