# uumail notification

uumailを受信したことをWindowsPCに通知します。

##Version<br>
  -0.1 beta1 uumailを受信すると、Win10のトースト通知機能によって通知されます。<br>


##environment<br>
  OS : Windows10のみ（Windows10以前では動きません。)<br>
  ※Mac,Android,iOSなどは非対応（Androidにはいずれ対応させます。）<br>
  
##Note<br>
現在はソースコードのみ公開しています。（ビルドすると動作不安定なため）<br>
不安定になるバグが解消されたらバイナリファイル(.exe)も公開します。<br>
利用するにはPython3とソースコードで読み込まれているライブラリをpipなどでインストールしてください。<br>
PyInstallerでビルドしてバイナリファイル（.exe）にできますが動作が不安定になります。<br>
もし、ビルドする場合は"--hidden-import plyer.platforms.win.notification"オプションをつけてください。<br>
