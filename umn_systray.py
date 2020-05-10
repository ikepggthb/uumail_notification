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

import win32.lib.win32con as win32con
import win32api
import subprocess
from infi.systray import SysTrayIcon

from setting import umn_config
import tkinter
import ctypes
import sys

#拡大によるボケ防止
ctypes.windll.shcore.SetProcessDpiAwareness(1)

VERSION = "1.1"

window_open = False

def show_about():
    global window_open
    font_content = ("メイリオ", 12)
    font_content_s = ("メイリオ",11)

    def on_close():
        global window_open
        root.destroy()
        window_open = False

    root = tkinter.Tk()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.title(u"uumail notification について")
    x_root = 600
    y_root = 400
    root.geometry(str(x_root)+"x"+str(y_root))
    root.configure(bg="white")
    #root.attributes("-alpha",0.8)
    root.resizable(0, 0)
    root_icon = 'icon\\uumail.ico'
    root.iconbitmap(default=root_icon)
    root_icon = 'icon\\uumail.png'
    icon_settings = tkinter.PhotoImage(file=root_icon)
    icon_settings = icon_settings.subsample(3)
    label_title = tkinter.Label(
        root,
        text=u' 　uumail notification',
        font=("游明朝", 30, "bold"),
        bg="white",
        image=icon_settings,
        compound='left'
    )
    label_title.place(x=0, y=0)

    bg_color = '#f9f9fa'
    frame = tkinter.Frame(
        root,
        height=y_root - 120,
        width=x_root,
        bg=bg_color,
        borderwidth=1
    )
    frame.place(x=0 , y=120)
    x_margin_frame = 40


    label_ver = tkinter.Label(frame,text='Version  :  '+VERSION,font = font_content,bg=bg_color)
    label_ver.place(x=x_margin_frame, y=30)

    LIC = "オープンソースソフトウェア(OSS)であり、GPLv3の条件で許諾されます。\nこのソフトウェアを使用、複製、配布、ソースコードを修正することが\nできます。"
    label_lic = tkinter.Label(frame,text=LIC,font = font_content_s,bg=bg_color, justify='left')
    label_lic.place(x=x_margin_frame, y=120)

    GITHUB = "Github : https://github.com/ikepggthb/uumail_notification"
    label_github = tkinter.Label(frame,text=GITHUB,font = font_content_s,bg=bg_color, justify='left')
    label_github.place(x=x_margin_frame, y=80)

    CPN = "© 2020 ikkei Yamada All Rights Reserved.		\nTwitter : @idkaeti , Email : ikeprg@gmail.com"

    label_cpn = tkinter.Label(frame,text=CPN,font = font_content_s,bg=bg_color)
    label_cpn.place(x=x_margin_frame, y=200)
    window_open = True
    root.mainloop()

def task_tray():
    def systray_exit(systray):
        win32api.MessageBox(0, u"終了します。", u"uumail_notification", win32con.MB_OK | win32con.MB_ICONQUESTION)
        sys.exit(0)
    def systray_open_setting(systray):
        umn_config.open_setting()
    def systray_about_unm(systray):
        if window_open == False:
            show_about()
    menu_options = (
        ("設定", None, systray_open_setting),
        ("uumail notificationについて", None, systray_about_unm),
    )
    systray = SysTrayIcon(umn_config.PATH_ICON, "uumail_notification", menu_options, on_quit=systray_exit)
    systray.start()