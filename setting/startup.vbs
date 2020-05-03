Set fso = CreateObject("Scripting.FileSystemObject")
Set ws = CreateObject("WScript.Shell")
startup = ws.SpecialFolders("Startup")
Set shortcut = ws.CreateShortcut(startup & "\uumail_notification.lnk")
current_folder = ws.CurrentDirectory
With shortcut
    .TargetPath = current_folder + "\uumail_notification.exe"
    .WorkingDirectory = current_folder + "\"
    .Save
End With