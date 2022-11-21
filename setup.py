# uumail notification 
# version : 2.1
# setup.py
#
# © 2020 Ikkei Yamada All Rights Reserved.
# Twitter : @idkaeti
# Email   : ikeprg@gmail.com

# setup file

import sys
from cx_Freeze import setup, Executable
 
base = None

includefiles = ['icon/', ('setting/startup.vbs','setting/startup.vbs'),'COPYING']
includes = []
upgrade_code = "{06b635d3-7f04-4f9d-a18a-8417ece45119}"

if sys.platform == 'win32' : base = 'Win32GUI'
 
exe = Executable(script = 'main.py',
                 base = base, icon='icon\\uumail.ico')

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "uumail notification",    # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]\\uumail_notification.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",              # WkDir
     ),
      ("StartMenuShortcut",        # Shortcut
       "StartMenuFolder",          # Directory_
       "uumail notification",    # Name
       "TARGETDIR",              # Component_
       "[TARGETDIR]\\uumail_notification.exe",# Target
       None,                     # Arguments
       None,                     # Description
       None,                     # Hotkey
       None,                     # Icon
       None,                     # IconIndex
       None,                     # ShowCmd
       "TARGETDIR",              # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

build_exe_options =  {"includes":includes,'include_files':includefiles} 
bdist_msi_options = {
    'add_to_path': True,
    'all_users' : True,
    'data' : msi_data,
    'upgrade_code': upgrade_code
    }

 
# セットアップ
setup(name = 'uumail notification',
      version = '2.1',
      description = 'uumail_notification',
      options = {"build_exe":build_exe_options,'bdist_msi': bdist_msi_options},
      executables = [exe])