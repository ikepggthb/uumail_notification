# uumail notification

uumailに新着メールが届いているかをWindowsPCに通知します。

## Version

- v0.1 beta1 test

- v0.1.1 beta1 Pythonのライブラリに依存しない通知方法を使うことでビルド可能になりました。

- v0.1.2 beta1 サーバーへの負荷減少。同じ通知を繰り返さないようにする機能を実装。

- v0.2 設定画面、パスワードを保存機能を実装。

- v1.0 細かなバグを修正。動作速度が大幅に向上。

- v1.1 アカウント情報入力画面が開かなくなるバグを修正。タスクトレイに常駐する機能を実装。

- v2.0 https://github.com/ikepggthb/uumail_notification/pull/6#issue-718408899

- v2.1 インストーラーが全ユーザー共通の［スタートアップ］フォルダにショートカットを作成してしまうのを修正。

## Environment

- OS : Microsoft Windows 10（Windows10以外のWindowsでは動作未確認)
- ※Mac,Android,iOSなどは非対応

## Note

- v2.0 以前のバージョンからアップデートする場合、以前のバージョンの"uumail notification"をアンインストールしてから、新しいバージョンをインストールしてください。
- 利用するには、以下のリンク先から、"uumail.notification-2.1-win64.msi"をダウンロードしてください。
<https://github.com/ikepggthb/uumail_notification/releases/download/2.1/uumail.notification-2.1-win64.msi>
（クリックするとダウンロードが始まります。）

- 実行するとインストールが開始されます。
- "uumail_notification"を起動すると新着メールの同期が行われます。
- ※uumail_notification.exeをスタートアップに設定すると、PC起動時に自動的にuumail_notification.exeが実行され、常に新着メール通知を確認できるのでとても便利です。


## Licence

- GPLv3の条項下で提供されます。
