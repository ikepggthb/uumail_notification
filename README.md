# uumail notification

uumailが受信されたことをWindowsPCに通知します。

##Version<br>
  -0.1 beta1 uumailを受信すると、Win10のトースト通知機能によって通知されます。<br>
  -0.1.1 beta1 Pythonのライブラリに依存しない通知方法を使うことでビルド可能になりました。<br>


##Environment<br>
  OS : Windows10のみ（Windows10以前では動きません。)<br>
  ※Mac,Android,iOSなどは非対応（Androidにはいずれ対応させます。）<br>
  
##Note<br>
 利用するにはumn_win10をダウンロードしてuumail_notification.exeを実行してください。
 IDとパスワードを入力すると、uumailの監視が始まり新着メールが来たらお知らせします。
 1時間毎にメールの確認が行われます。（将来的にはメール確認の頻度を設定できるようにします。）
