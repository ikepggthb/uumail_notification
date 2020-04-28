import os
from tkinter import messagebox
import tkinter
root = tkinter.Tk()
root.withdraw()
a = os.system("taskkill /f /im  uumail_notification.exe")
print(a)
if a == 0:
    messagebox.showinfo('uumail notification - exit', "終了しました")
else:
    messagebox.showinfo('uumail notification - exit', "uumail_notificationは起動していません。")
