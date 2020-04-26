import subprocess
import os
path = os.getcwd() + "\\toast"
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
    <audio silent="true"/>
</toast>"""

def toast(title,content):
    xml_f = xml_template1+title+xml_template2+content+xml_template3
    with open('toast\\test.xml', mode='w', encoding='shift-jis') as f:
        f.write(xml_f)
    cmdresult = "toast\\ps_launcher.vbs toast\\toaster.ps1 toast\\toast.xml"
    subprocess.Popen(cmdresult, shell=True)
    return 0
