import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

import notification_daemon


# 多重起動確認
import win32event
import winerror
import pywintypes
import win32api
import sys
import win32.lib.win32con as win32con
UNIQUE_MUTEX_NAME = 'Global\\UmnIsAlreadyRunning'
handle = win32event.CreateMutex(None, pywintypes.FALSE, UNIQUE_MUTEX_NAME)
if not handle or win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    print('既に別のプロセスが実行中です。', file=sys.stderr)
    win32api.MessageBox(0, u"既に常駐しています", u"uumail notification - エラー", win32con.MB_OK | win32con.MB_ICONERROR)
    sys.exit(-1)



# 設定、アカウント情報読み込み 
from setting import passcrypt
from setting import umn_config
CONFIG = umn_config.read_config()
try:
    ACCOUNT_DATA = passcrypt.read_data()
except:
    q = win32api.MessageBox(0, u"アカウント情報の取得に失敗しました\nアカウントを設定しますか", u"uumail notification - エラー", win32con.MB_YESNO | win32con.MB_ICONERROR)
    if q == win32con.IDYES:
        umn_config.open_setting()
    win32api.MessageBox(0, u"終了します。", u"uumail notification - エラー", win32con.MB_OK | win32con.MB_ICONERROR)
    sys.exit(1)
ID = ACCOUNT_DATA[0]
PASSWD = ACCOUNT_DATA[1]
SYNC_INTERVAL = 60 * int(CONFIG['sync_interval']) # 秒

class about_window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("uumail notification について")
        self.setFixedSize(600,370)
        self.setWindowFlags(QtCore.Qt.Dialog|QtCore.Qt.WindowStaysOnTopHint)
        self.label = QtWidgets.QLabel(self)
        self.label_style = """QLabel {
            font-size: 43px;               /* 文字サイズ */
            padding: 0px 40px;
        }"""
        self.font = QtGui.QFont()
        self.font.setPointSize(13)
        self.label.setStyleSheet(self.label_style)
        self.label.setText("uumail notification")
        self.label.setGeometry(QtCore.QRect(120,0,480,120))
        self.umnlogo_image = QtGui.QImage('icon\\uumail.png')
        self.umnlogo_pixmap = QtGui.QPixmap.fromImage(self.umnlogo_image.scaledToHeight(120))
        self.umnlogo_label = QtWidgets.QLabel(self)
        self.umnlogo_label.setPixmap(self.umnlogo_pixmap)
        self.umnlogo_label.setGeometry(QtCore.QRect(0,0,120,120))
        self.varsion_txt = QtWidgets.QLabel(self)
        self.varsion_txt.setText("Version  :  2.0")
        self.varsion_txt.setFont(self.font)
        self.varsion_txt.setGeometry(QtCore.QRect(40,150,500,30))
        self.github_txt = QtWidgets.QLabel(self)
        self.github_txt.setText("Github : https://github.com/ikepggthb/uumail_notification")
        self.github_txt.setFont(self.font)
        self.github_txt.setGeometry(QtCore.QRect(40,190,500,30))
        self.licence_txt = QtWidgets.QLabel(self)
        self.licence_txt.setText("オープンソースソフトウェア(OSS)であり、GPLv3の条件で許諾されます。\nこのソフトウェアを使用、複製、配布、ソースコードを修正することができます。")
        self.licence_txt.setFont(self.font)
        self.licence_txt.setGeometry(QtCore.QRect(40,230,500,45))
        self.cpn_txt = QtWidgets.QLabel(self)
        self.cpn_txt.setText( "© 2020 ikkei Yamada All Rights Reserved.\n	Twitter : @idkaeti , Email : ikeprg@gmail.com")
        self.cpn_txt.setFont(self.font)
        self.cpn_txt.setGeometry(QtCore.QRect(40,290,500,45))
    # closeEventをオーバーライド ウィンドウを閉じたとき、アプリが終了しないようにするため
    def closeEvent(self, event):
        self.hide()
        event.ignore()


class MyWidget(QtWidgets.QWidget):
    def __init__(self,systray):
        super().__init__()

        self.systray = systray

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
    
    def magic(self):
        txt = random.choice(self.hello)
        self.text.setText(txt)
        self.systray.showMessage("uumail", txt,QtWidgets.QSystemTrayIcon.Critical)

class MySystray(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.icon = QtGui.QIcon(umn_config.PATH_ICON)
        self.setIcon(self.icon)
        self.setVisible(True)
        # self.tray.showMessage("title", "msg",QtWidgets.QSystemTrayIcon.Critical)
        self.init_menu()
        
    def init_menu(self):
        # メニューの作成
        self.menu = QtWidgets.QMenu()
        # 項目 : 設定
        self.show_setting_action = QtGui.QAction('設定', self.menu)
        self.show_setting_action.setObjectName('setting')
        self.show_setting_action.triggered.connect(self.show_setting)
        self.menu.addAction(self.show_setting_action)
        self.setContextMenu(self.menu)
        # 項目 : バージョン情報
        self.show_about_action = QtGui.QAction('uumail notificationについて', self.menu)
        self.show_about_action.setObjectName('about')
        self.show_about_action.triggered.connect(self.show_about)
        self.menu.addAction(self.show_about_action)
        self.setContextMenu(self.menu)
        self.about_wg = about_window()
        # 項目 : Quit
        self.exit_action = QtGui.QAction('Quit', self.menu)
        self.exit_action.setObjectName('exit')
        self.exit_action.triggered.connect(self.quit_)
        self.menu.addAction(self.exit_action)
        self.setContextMenu(self.menu)
    def show_setting(self):
        umn_config.open_setting()
    def show_about(self):
        self.about_wg.show()
    def quit_(self):
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    systray = MySystray()

    widget = MyWidget(systray)

    reg_notify = notification_daemon.Regularly_notify(ACCOUNT_DATA[0],ACCOUNT_DATA[1],SYNC_INTERVAL,systray)
    reg_notify.DontNotify_NoMail = bool(CONFIG['DontNotify_NoMail'])
    reg_notify.start()

    sys.exit(app.exec())