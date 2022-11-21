import json
import os
from os.path import expanduser
import subprocess

import win32com.client
ws_shell = win32com.client.Dispatch("Wscript.Shell")

DIR_UMN = os.getcwd()
if DIR_UMN[-7:] == "setting":
    os.chdir('..')
    DIR_UMN = os.getcwd()

DIR_CONFIG =  os.getenv('APPDATA') + '\\uumail_notification\\settings'
PATH_CONFIG = DIR_CONFIG + '\\config.json'
DIR_STARTUP = ws_shell.SpecialFolders("Startup")
PARH_STARTUP = DIR_STARTUP + "\\uumail_notification.lnk"
PATH_ICON = "icon\\uumail.ico"
icon = "icon\\uumail.ico"

default_config = {'sync_interval': '60','DontNotify_NoMail' : 'True'}

os.makedirs(DIR_CONFIG, exist_ok=True)


def write_config(config):
    with open(PATH_CONFIG, 'w') as f:
        json.dump(config, f, indent=4)

def read_config():
    try:
        with open(PATH_CONFIG) as f:
            config = json.load(f)
        # キーが存在しなければ、エラーを吐いて、except文へ（設定ファイル作り直し）
        config['sync_interval']
        config['DontNotify_NoMail']
    except:
            config = default_config
            write_config(config)
    return config

def exist_startup():
    return os.path.exists(PARH_STARTUP)

def make_startup():
    subprocess.run(DIR_UMN + "\\setting\\startup.vbs", shell=True)

def del_startup():
    subprocess.run(["del", PARH_STARTUP], shell=True)