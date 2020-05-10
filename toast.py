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


