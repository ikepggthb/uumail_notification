# uumail notification

uumailが受信されたことをWindowsPCに通知します。

## Version

- v0.1 beta1 uumailを受信すると、Win10のトースト通知機能によって通知されます。

- v0.1.1 beta1 Pythonのライブラリに依存しない通知方法を使うことでビルド可能になりました。

- v0.1.2 beta1 サーバーへの負荷減少。同じ通知を繰り返さないようにする機能を実装。

- v0.2 設定画面、パスワードを保存機能を実装。

- v1.0 細かなバグを修正。動作速度が大幅に向上。

- v1.1 アカウント情報入力画面が開かなくなるバグを修正。タスクトレイに常駐する機能を実装。

## Environment

- OS : Windows10のみ（Windows10以前では動きません。)
  - ※Mac,Android,iOSなどは非対応（Androidにはいずれ対応させます。）

## Note

- 利用するには、
<https://drive.google.com/drive/folders/1gcDD2wZ6LU6w51_D2wKEt_Q42xRsdvsG?usp=sharing>
へアクセスし、umn_1.1.zipをダウンロードし、解凍してください。
- INSTALL.EXEを実行するとインストールが開始されます。
- "uumail_notification"を起動すると新着メールの同期が行われます。
- ※pyinstallerの仕様上、反応が鈍いことがあります。
- ※uumail_notification.exeをスタートアップに設定すると、PC起動時に自動的にuumail_notification.exeが実行され、常に新着メール通知を確認できるのでとても便利です。


## Licence

- GPLv3の条項下で提供されます。