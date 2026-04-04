# Lab:  Yanıt zamanlaması yoluyla kullanıcı adı numaralandırması

Bu laboratuvar, yanıt süreleri kullanılarak kullanıcı adı numaralandırmasına karşı savunmasızdır.

Çözüm için:
- Kullanıcı adı numaralandırması ile kullanıcı adını bulunmalı.
- Bulunan kullanıcının parolasını brute force ile bul.
- Bulunan kullanıcı ile giriş yap.

Lab açılışı:
![Username enumeration via response timing ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20response%20timing%20ilk.png?raw=true)

Zamana gecikmeli enumeration için [bu kod](kod)  kullanılır. Bu kod dayasıyla aynı konumda kayıtlı username.txt dosyasındaki kullanıcıları tek tek dener ve 2 saniye geç gelen yanıtı potansiyel kullanıcı olarak ekranda gösterir. Lab bir kaç yanlış girişde ip engellemesi gerçekleştirir kod her denemede farklı bir ip ile sorgu gerçekleştirerek ip engellemesini atlatır. Kodu çalıştırdığımızda `ai` adlı kullanıcıyı bulmuş olduk.
![Username enumeration via response timing usname](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20response%20timing%20usname.png?raw=true)

Yine aynı kod kullanılarak bulmuş oluğumuz kullanıcı adı için brute force ile parolayı bulabiliriz. Kodu çalıştırdığımızda `michael` parolasını bulmuş olduk.
![Username enumeration via response timing pass](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20response%20timing%20pass.png?raw=true)

Son olarak labı çözmek için bulunan kullanıcı adı ve parola ile giriş yapılır.
![Username enumeration via response timing cozum](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20response%20timing%20cozum.png?raw=true)

Lab link:</br>
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing
