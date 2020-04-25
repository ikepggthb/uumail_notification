# uumail notification

uumailを受信したことをWindowsPCに通知します。

Version
-0.1 beta1 UUmailを受信すると、win10のトースト通知機能によって通知されます。


環境
　os : windows10のみ（window10以前では動きません。)
※ mac,android,iosなどは非対応（いずれ対応させます。）

現在はソースコードのみ公開しています。（ビルドすると動作不安定なため）
不安定になるバグが解消されたらバイナリファイル(.exe)を公開します。
利用するにはpython3とソースコードで読み込まれているライブラリをpipなどでインストールしてください。

PyInstallerでビルドして実行ファイル（.exe）にできますが動作が不安定になります。
ビルドする場合は"--hidden-import plyer.platforms.win.notification"をつけてください。
