import sys
import tkinter
import tkinter.ttk
import ctypes
import subprocess
from tkinter import messagebox
import re
import shutil
import time
import os

import umn_config
import passcrypt


# windowsのディスプレイ拡大率によるボケ防止
ctypes.windll.shcore.SetProcessDpiAwareness(1)

DIR_UMN = os.getcwd()
if DIR_UMN[-7:] == "setting":
    DIR_UMN = DIR_UMN[:-8]

# ID,PASS入力画面を2つ以上起動させないために
account_setting_open = False

change_account = False

def account_setting():

    global account_setting_open

    def collect_login_data(ID, PASSWD):
        passwd_in_twoalpha = bool(re.search(r'[a-zA-Z_].*[a-zA-Z_]', PASSWD))
        passwd_in_notalpha = bool(re.search(r'[^a-zA-Z]+', PASSWD))
        # エラーを避けるため、文字数の確認を先に行っている。
        collect = \
            len(ID) == 7 and \
            ID[0] == 't' and \
            str.isdecimal(ID[1:7]) and \
            len(PASSWD) >= 6 and \
            passwd_in_twoalpha and \
            passwd_in_notalpha
        return collect

    def write_data():
        global account_setting_open
        global change_account
        ID = input_id.get()
        PASSWD = input_passwd.get()
        if collect_login_data(ID, PASSWD):
            sub_win.destroy()
            account_setting_open = False
            passcrypt.write_data(ID, PASSWD)
            time.sleep(3)
            label_status_text.set("状態 : " + confirm_login_status())
            change_account = True
        else :
            sub_win.destroy()
            messagebox.showerror("uumail notification - エラー", "設定を変更できませんでした\n正しいIDとパスワードを入力してください")
            cancel()

    def cancel():
        global account_setting_open
        sub_win.destroy()
        account_setting_open = False

    sub_win = tkinter.Toplevel()
    sub_win.title(u"uumail notification - アカウントを変更する")
    sub_win.geometry("330x80")
    sub_win.resizable(0, 0)

    label_id = tkinter.Label(sub_win,text="ID")
    label_id.grid(row=2, column=1, padx=10,)

    input_id = tkinter.Entry(sub_win,width=40)
    input_id.grid(row=2, column=2)

    label_passwd = tkinter.Label(sub_win,text="パスワード")
    label_passwd.grid(row=3, column=1, padx=10,)

    input_passwd = tkinter.Entry(sub_win,show='*', width=40)
    input_passwd.grid(row=3, column=2)

    button_cancel = tkinter.Button(sub_win,text="キャンセル",command=cancel)
    button_cancel.place(x=220, y=50)

    button_save = tkinter.Button(sub_win,text="OK",width=5,command=write_data)
    button_save.place(x=280, y=50)

    account_setting_open = True

    sub_win.mainloop()

def running_umn():
    cmd = "tasklist"
    tasklist = subprocess.run(cmd, check=True, shell=False, stdout=subprocess.PIPE)
    run_umn = "uumail_notification" in str(tasklist)
    return run_umn

def restart_umn():
    subprocess.run(["taskkill", "/f", "/im", "uumail_notification.exe"])
    time.sleep(2)
    subprocess.Popen("uumail_notification.exe", shell=True)

def reflect_auto_startup():
    start_up = auto_startup.get()
    if start_up == True and startup_exist == False:
        subprocess.run(DIR_UMN + "\\startup.vbs", shell=True)
    elif start_up == False and startup_exist == True:
        subprocess.run(["del", umn_config.PARH_STARTUP], shell=True)

def save():
    new_config = {
        'sync_interval' :  sync_interval_option[cb_sync_interval.get()]
        }
    root.destroy()
    reflect_auto_startup()
    change_config = config != new_config or change_account
    if change_config :
        umn_config.write_config(new_config)
        if running_umn() :
            q = messagebox.askquestion(
            'uumail_notification - エラー',
            'uumail_notification が既に常駐しています。\nuumail_notification を再起動すると設定が適用されます。\n再起動しますか？'
            )
            if q == "yes":
                restart_umn()
    sys.exit(0)

def cancel():
    sys.exit(0)

def open_pass_set():
    if account_setting_open is False :
        account_setting()

def delete_account():
    if running_umn():
        q = messagebox.askquestion(
            'uumail_notification - アカウント情報削除',
            'uumail_notification が常駐しています。\nアカウントを削除するするには、終了する必要があります。\nuumail_notification を終了しますか？'
            )
        if q == "yes":
            subprocess.run(["taskkill", "/f", "/im", "uumail_notification.exe"])
        else:
            return
    shutil.rmtree(passcrypt.PATH_DIR)
    messagebox.showinfo("uumail_notification", "アカウント情報を削除しました")
    time.sleep(2)
    label_status_text.set("状態 : " + confirm_login_status())


sync_interval_option = {'30分毎': '30', '1時間毎': '60', '2時間毎': "120", '4時間毎': '240'}

def confirm_login_status():
    try:
        login_data = passcrypt.read_data()
        status = login_data[0] +' でログインします'
    except:
        status = 'アカウントが設定されていません'
    return status

# 設定ファイルの読み込み
config = umn_config.read_config()



font_header = ("メイリオ",12,"bold")
font_content = ("メイリオ", 10)

root = tkinter.Tk()
root.title(u"uumail notification - 設定")
x_root = 600
y_root = 550
root.geometry(str(x_root)+"x"+str(y_root))
root.configure(bg=None)
#root.attributes("-alpha",0.8)
root.resizable(0, 0)
root_icon = DIR_UMN + '\\icon\\uumail.ico'
root.iconbitmap(default=root_icon)

icon_settings = tkinter.PhotoImage(file=DIR_UMN + '\\setting\\settings.png')
icon_settings = icon_settings.subsample(14)
label_title = tkinter.Label(
    root,
     text=u' 設定',
      font=("メイリオ", 14, "bold"),
       bg=None,
       image=icon_settings,
       compound='left'
)
label_title.place(x=30, y=20)

bg_color = '#f9f9fa'
frame = tkinter.Frame(
    root,
    height=y_root - 150,
    width=x_root - 100,
    relief='raised',
    bg=bg_color,
    borderwidth=1
)
frame.place(x=50 , y=70)
x_header = 20

label_acount = tkinter.Label(frame,text=u'アカウント', font=font_header, bg=bg_color)
y_acount = 20
label_acount.place(x=x_header, y=y_acount)
label_status_text = tkinter.StringVar()
label_status_text.set("状態 : " + confirm_login_status())
label_status = tkinter.Label(frame,textvariable=label_status_text,font = font_content,bg=bg_color)
label_status.place(x=x_header+40, y=y_acount+40)

button_account_setting = tkinter.Button(frame,text=u'アカウントを設定する',font = font_content,bg=bg_color,command=open_pass_set)
button_account_setting.place(x=x_header + 40, y=y_acount + 80)

button_account_delete = tkinter.Button(frame,text=u'アカウント情報を削除する',font = font_content,bg=bg_color,command=delete_account)
button_account_delete.place(x=x_header+200, y=y_acount+80)

label_sync = tkinter.Label(frame,text=u'同期', font=font_header, bg=bg_color)
y_sync = 180
label_sync.place(x=x_header, y=y_sync)

label_sync_interval = tkinter.Label(frame,text=u'同期頻度　：',font = font_content,bg=bg_color)
label_sync_interval.place(x=x_header + 40, y=y_sync + 40)

cb_sync_interval = tkinter.ttk.Combobox(frame, state="readonly",font=font_content)
cb_sync_interval['values'] = list(sync_interval_option.keys())
sync_interval_option_values = list(sync_interval_option.values())
sync_interval = sync_interval_option_values.index(config['sync_interval'])
cb_sync_interval.current(sync_interval)
cb_sync_interval.place(x=x_header + 130, y=y_sync + 42)

y_auto_startup = 280
label_auto_startup = tkinter.Label(frame,text=u'自動起動',font = font_header,bg=bg_color)
label_auto_startup.place(x=x_header, y=y_auto_startup)

startup_exist = umn_config.exist_startup()
auto_startup = tkinter.BooleanVar()
auto_startup.set(startup_exist)
chk_startup = tkinter.Checkbutton(frame, variable=auto_startup, text='起動時に自動的に実行する。',font = font_content,bg=bg_color)
chk_startup.place(x=x_header + 40, y=y_auto_startup + 40)

button_cancel = tkinter.Button(root,text="キャンセル",font=font_content,width=10,command=cancel)
button_cancel.place(x=x_root - 210, y=y_root - 50)
button_save = tkinter.Button(root,text="OK",font=font_content,width=10,command=save)
button_save.place(x=x_root - 110, y=y_root - 50)

root.mainloop()