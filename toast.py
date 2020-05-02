import subprocess
import os
from os.path import expanduser

path = os.getcwd() + "\\toast"
dir_xml = expanduser("~") + '\\AppData\\Roaming\\uumail_notification\\toast'
path_xml = dir_xml + "\\toast.xml"

os.makedirs(dir_xml, exist_ok=True)

xml_template1 ="""<toast scenario="reminder">
    <visual>
        <binding template="ToastGeneric">
            <text>"""
xml_template2 ="""</text>
	        <text>"""
xml_template3 ="""</text>
	        <image placement="appLogoOverride" hint-crop="circle" src=\""""+path+"""\\uumail.ico"/>
        </binding>
    </visual>
</toast>"""

def toast(title,content):
    xml_f = xml_template1+title+xml_template2+content+xml_template3
    with open(path_xml, mode='w', encoding='shift-jis') as f:
        f.write(xml_f)
    cmdresult = "toast\\ps_launcher.vbs toast\\toaster.ps1 " + path_xml
    subprocess.Popen(cmdresult, shell=True)
    return 0


