# uumail notification

uumailが受信されたことをWindowsPCに通知します。

## Version

- v0.1 beta1 uumailを受信すると、Win10のトースト通知機能によって通知されます。

- v0.1.1 beta1 Pythonのライブラリに依存しない通知方法を使うことでビルド可能になりました。

- v0.1.2 beta1 サーバーへの負荷減少。同じ通知を繰り返さないようにする機能を実装。

- v0.2 設定画面、パスワードを保存機能を実装。

- v1.0 細かなバグを修正。動作速度が大幅に向上。

## Environment

- OS : Windows10のみ（Windows10以前では動きません。)
  - ※Mac,Android,iOSなどは非対応（Androidにはいずれ対応させます。）

## Note

- 利用するには、
<https://drive.google.com/drive/folders/1gcDD2wZ6LU6w51_D2wKEt_Q42xRsdvsG?usp=sharing>
へアクセスし、"uumail_notification_1.0.zip"をダウンロードして任意の場所に展開してください。
- 最初に設定を行ってください。
- 設定画面を表示するには、"setting.exe"を実行してください。
- "uumail_notification.exe"を起動すると新着メールの同期が行われます。
- 終了するには、"exit.exe"を実行してください。

### 注意

- ※pyinstallerの仕様上、反応が鈍いことがあります。
- ※uumail_notification.exeをスタートアップに設定すると、PC起動時に自動的にuumail_notification.exeが実行され、常に新着メール通知を確認できるのでとても便利です。
