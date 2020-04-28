# uumail notification

uumailが受信されたことをWindowsPCに通知します。

##Version<br>
  -v0.1 beta1 uumailを受信すると、Win10のトースト通知機能によって通知されます。<br>
  -v0.1.1 beta1 Pythonのライブラリに依存しない通知方法を使うことでビルド可能になりました。<br>
  -v0.1.2 beta1 サーバーへの負荷減少。同じ通知を繰り返さないようにする機能を実装。
  -v0.2 設定画面、パスワードを保存機能を実装。


##Environment<br>
  OS : Windows10のみ（Windows10以前では動きません。)<br>
  ※Mac,Android,iOSなどは非対応（Androidにはいずれ対応させます。）<br>

##Note<br>
利用するには、<br>
<br>
https://drive.google.com/drive/folders/1gcDD2wZ6LU6w51_D2wKEt_Q42xRsdvsG?usp=sharing
<br>
へアクセスし、"uumail_notification.zip"をダウンロードして任意の場所に展開してください。<br>
<br>
最初に設定を行ってください。<br>
設定画面を表示するには、"setting.exe"を実行してください。
<br>
"uumail_notification.exe"を起動すると新着メールの同期が行われます。<br>
終了するには、"exit.exe"を実行してください。<br>
<br>
（注）設定は"uumail_notification.exe"を終了させないと反映されません。<br>
（注）設定画面のアカウントの状態は、設定画面を再起動しないと反映されません（次のバージョンで対応します。）<br>
<br>
※アカウント情報の取得に失敗し、アカウントの設定をしたら再度起動してください<br>
※pyinstallerの仕様上、反応が鈍いことがあります。（特にアカウントの設定画面に起動など）<br>
※uumail_notification.exeをスタートアップに設定すると、PC起動時に自動的にuumail_notification.exeが実行され、常に新着メール通知を確認できるのでとても非常に便利です。<br>

