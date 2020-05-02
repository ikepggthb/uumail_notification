import subprocess
from tkinter import messagebox
import tkinter
import sys


root = tkinter.Tk()
root.withdraw()
a = subprocess.run(["taskkill" ,"/f","/im","uumail_notification.exe"])
if a.returncode == 0:
    messagebox.showinfo('uumail notification - exit', "終了しました")
else:
    messagebox.showinfo('uumail notification - exit', "uumail_notification は起動していません。")

sys.exit(0)

