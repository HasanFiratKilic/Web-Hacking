Bu laboratuvar , oturum açma işlevinde bir SQLi açıği içermekte.
Laboratuvarı çözmek için, `administrator` kullanıcısı ile oturum açılmalı.

Sayfanın giriş paneli aşağıdaki gibi:
![Lab2 giriş paneli](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab2%20giri%C5%9F%20panel.png?raw=true)
ilk adım olarak from kısmında bir SQLi varmı bunu kontrol edilim. Bunu kullanıcı adını yazdıktan sonra `'` işareti bırakarak konrol edebiliriz.
![Lab2 sqli kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab2%20sqli%20kontrol.png?raw=true)
Yukarda görüldüğü gibi kullanıcı adına `administrator'`, parolayada rasgele bir değer ile giriş yapmaya çalışınca SQL sorgusunu bozduk ve site hata verdi. Yani burada bir SQLi açığı mevcut olduğunu öğrendik.
Şimdiki adım kullanıcı adı kısmına `administrator' --` yükünü verip parolayı bilmeden administrator hesabına giriş yapmakta:
![Lab2 çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab2%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)
Yükü yolladıktan sonra giriş başarıyla gerçekleştirilmiştir.
Labaratuarı aşağıdaki linkten kendiniz çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/lab-login-bypass

