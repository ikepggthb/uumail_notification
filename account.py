import sys
import tkinter
import tkinter.ttk
import ctypes
import passcrypt
from os.path import expanduser
import os
#windowsのディスプレイ拡大率によるボケ防止
ctypes.windll.shcore.SetProcessDpiAwareness(1)


def write_data():
    erc_key = 0
    erc_data = 1
    write_path = expanduser("~") + '\\AppData\\Local\\uumail_notification\\account'
    loginid = input_id.get()
    passwd = input_passwd.get()
    erc = passcrypt.encrypt(passwd)
    os.makedirs(write_path, exist_ok=True)
    os.makedirs("settings", exist_ok=True)
    passcrypt.write_bin('settings\\login.key', erc[erc_key])
    passcrypt.write_bin(write_path+"\\login.data", erc[erc_data])
    with open(write_path+"\\loginid.txt", mode='w') as f:
        f.write(loginid)
    sys.exit()


root = tkinter.Tk()
root.title(u"uumail notification - アカウントを変更する")
root.geometry("330x80")
root.resizable(0, 0)

# IDラベル
label_id = tkinter.Label(text="ID")
label_id.grid(row=2, column=1, padx=10,)

# ID入力欄の作成
input_id = tkinter.Entry(width=40)
input_id.grid(row=2, column=2)

# パスワードラベル
label_passwd = tkinter.Label(text="パスワード")
label_passwd.grid(row=3, column=1, padx=10,)

# パスワード入力欄の作成
input_passwd = tkinter.Entry(show='*', width=40)
input_passwd.grid(row=3, column=2)

#ボタンの作成
button_cancel = tkinter.Button(root,text="キャンセル",command=sys.exit)
button_cancel.place(x=220, y=50)
button_save = tkinter.Button(root,text="OK",width=5,command=write_data)
button_save.place(x=280, y=50)

root.mainloop()