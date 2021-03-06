import json
import os
from os.path import expanduser
import subprocess

DIR_HOME = expanduser("~")
DIR_CONFIG =  DIR_HOME + '\\AppData\\Roaming\\uumail_notification\\settings'
PATH_CONFIG = DIR_CONFIG + '\\config.json'
PARH_STARTUP = DIR_HOME + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\uumail_notification.lnk"
PATH_SETTING = "setting\\setting.exe"
PATH_ICON = "icon\\uumail.ico"

default_config = {'sync_interval': '60'}

os.makedirs(DIR_CONFIG, exist_ok=True)


def write_config(config):
    with open(PATH_CONFIG, 'w') as f:
        json.dump(config, f, indent=4)

def read_config():
    try:
        with open(PATH_CONFIG) as f:
            config = json.load(f)
    except:
            config = default_config
            write_config(config)
    return config

def exist_startup():
    return os.path.exists(PARH_STARTUP)

icon = "icon\\uumail.ico"

def open_setting():
    cmd = PATH_SETTING
    subprocess.Popen(cmd, shell=True)