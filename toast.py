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
    cmdresult = "toast\\powershellLauncher.vbs toast\\toaster.ps1 toast\\test.xml"
    subprocess.Popen(cmdresult, shell=True)
    return 0







# from xml.dom.minidom import parseString

# xml_template ="""<toast scenario="reminder">
#         <visual>
#             <binding template="ToastGeneric">
#                 <text>title</text>
# 	            <text>content</text>
# 	            <image placement="appLogoOverride" hint-crop="circle" src="C:\\Users\\ikkei\VSCode\\python\\uumail.ico"/>
#             </binding>
#         </visual>
#         <audio silent="true"/>
#     </toast>"""

# dom = parseString(xml_template)

# binding = dom.getElementsByTagName("binding")[0]

# # ????????
# title = dom.createElement('text')
# title.appendChild(dom.createTextNode("???????"))
# binding.appendChild(title)
# contents = dom.createElement('text')
# contents.appendChild(dom.createTextNode("???????"))
# binding.appendChild(contents)

# # dom?xml???????
# print (dom.toprettyxml())


# import xml.etree.ElementTree as ET

# toast = ET.Element('toast', {'scenario':'reminder'})
# visual = ET.SubElement(toast, 'visual')
# binding = ET.SubElement(visual, 'binding', {'template': 'ToastGeneric'})
# title = ET.SubElement(binding, 'text')
# tt = ET.tostring(title,encoding='shift_jis')
# title.text = 'あああ'
# contents = ET.SubElement(binding, 'text')
# contents.text = 'あああ'
# image = ET.SubElement(binding, 'image', {'placement':'appLogoOverride','hint-crop':'circle','src': 'C:\\Users\\ikkei\\VSCode\\python\\uumail.ico'})
# audio = ET.SubElement(toast,'audio',{'silent':'true'})
# ET.dump(toast)

# tree = ET.ElementTree(toast)
# tree.write('sample.xml',encoding='shift_jis')