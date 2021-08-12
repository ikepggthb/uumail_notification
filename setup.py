# coding: utf-8
# セットアップファイル
 
import sys
from cx_Freeze import setup, Executable
 
base = None

includes = ["infi.systray","pkg_resources"]

# GUI=有効, CUI=無効 にする
if sys.platform == 'win32' : base = 'Win32GUI'
 
# exe にしたい python ファイルを指定
exe = Executable(script = 'uumail_notification.py',
                 base = base, icon='icon\\uumail.ico')
 
# セットアップ
setup(name = 'uumail_notification',
      version = '0.1',
      description = 'uumail_notification',
      options = {"build_exe": {"includes":includes}},
      executables = [exe])