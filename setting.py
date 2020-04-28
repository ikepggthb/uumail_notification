import sys
import tkinter
import tkinter.ttk
import ctypes
import json
import os
import passcrypt
import subprocess

# windowsのディスプレイ拡大率によるボケ防止
ctypes.windll.shcore.SetProcessDpiAwareness(1)

def write_config():
    config = {"sync_interval": sync_interval_option[cb_sync_interval.get()]}
    os.makedirs("settings", exist_ok=True)
    with open('settings/config.json', 'w') as f:
        json.dump(config, f, indent=4)
    sys.exit()

def open_pass_set():
    cmd = "account.exe"
    subprocess.Popen(cmd, shell=True)

sync_interval_option = {'30分毎': '30', '1時間毎': '60', '2時間毎': "120", '4時間毎': '240'}

try:
    # 設定ファイルの読み込み
    with open('settings/config.json') as f:
        config = json.load(f)
except:
    # 初期設定
    config = {'sync_interval': '60'}

try:
    login_data = passcrypt.read_data()
    status_text = login_data[0] +' でログインします'
except:
    status_text = 'WARNING : アカウントが設定されていません'

#フォント設定
font_header = ("メイリオ",12,"bold")
font_content = ("メイリオ", 10)
# ウインドウ作成
root = tkinter.Tk()
root.title(u"uumail notification - 設定")
root.geometry("600x450")
root.configure(bg=None)
#root.attributes("-alpha",0.8)
root.resizable(0, 0)

icon = tkinter.PhotoImage(file='settings.png')
icon = icon.subsample(14)
label_title = tkinter.Label(root, text=u' 設定', font=("メイリオ", 14, "bold"), bg=None,image=icon,compound='left')
label_title.place(x=30, y=20)

bg_color = '#f9f9fa'
frame = tkinter.Frame(
    root,
    height=300,
    width=500,
    relief='raised',
    bg=bg_color,
    borderwidth=1
)
frame.place(x=50 , y=70)
x_header = 20


label_acount = tkinter.Label(frame,text=u'アカウント', font=font_header, bg=bg_color)
x_acount = x_header
y_acount = 20
label_acount.place(x=x_acount, y=y_acount)

label_status = tkinter.Label(frame,text=u'状態　：　'+status_text,font = font_content,bg=bg_color)
label_status.place(x=x_acount+40, y=y_acount+40)


button_password = tkinter.Button(frame,text=u'アカウントを変更する',font = font_content,bg=bg_color,command=open_pass_set)
button_password.place(x=x_acount+40, y=y_acount+80)

label_sync = tkinter.Label(frame,text=u'同期', font=font_header, bg=bg_color)
x_sync = x_header
y_sync = 180
label_sync.place(x=x_sync, y=y_sync)

label_sync_interval = tkinter.Label(frame,text=u'同期頻度　：',font = font_content,bg=bg_color)
label_sync_interval.place(x=x_sync + 40, y=y_sync + 40)

cb_sync_interval = tkinter.ttk.Combobox(frame, state="readonly",font=font_content)
cb_sync_interval['values'] = list(sync_interval_option.keys())
#値のセット
sync_interval_option_values = list(sync_interval_option.values())
sync_interval = sync_interval_option_values.index(config['sync_interval'])
cb_sync_interval.current(sync_interval)

cb_sync_interval.place(x=x_sync + 130, y=y_sync + 42)

#ボタン
button_cancel = tkinter.Button(root,text="キャンセル",font=font_content,width=10,command=sys.exit)
button_cancel.place(x=390, y=400)
button_save = tkinter.Button(root,text="OK",font=font_content,width=10,command=write_config)
button_save.place(x=490, y=400)


root.mainloop()