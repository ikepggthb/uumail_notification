# uumail notification

uumailを受信したことをWindowsPCに通知します。

##Version<br>
  -0.1 beta1 UUmailを受信すると、win10のトースト通知機能によって通知されます。<br>


##環境

OSwindows10のみ（window10以前では動きません。)<br>
mac,android,iosなどは非対応（いずれ対応させます。）<br>

##Requirement

現在はソースコードのみ公開しています。（ビルドすると動作不安定なため）<br>
不安定になるバグが解消されたらバイナリファイル(.exe)を公開します。<br>
利用するにはpython3とソースコードで読み込まれているライブラリをpipなどでインストールしてください。<br>
PyInstallerでビルドして実行ファイル（.exe）にできますが動作が不安定になります。
ビルドする場合は"--hidden-import plyer.platforms.win.notification"をつけてください。
