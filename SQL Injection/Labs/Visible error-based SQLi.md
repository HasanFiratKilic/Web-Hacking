## Görünür hata tabanlı SQL enjeksiyonu


Bu lab, **görünür hata tabanlı SQL enjeksiyonu** açığını içermektedir.
Uygulama:

-   `TrackingId` adlı bir çerezi analiz amacıyla kullanır.
    
-   Bu çerezin değerini içeren bir SQL sorgusu çalıştırır.
    
-   Sorgu sonucu ekrana basılmaz.
    
-   Eğer SQL sorgusu hata üretirse uygulama **ayrıltılı hata mesajı** döndürür.

Veritabanında:

-   `users` adlı tablo
    
-   `username` ve `password` sütunları bulunur.
    

Amaç:  
`administrator` kullanıcısının parolasını bulup giriş yapmaktır.

--------------------------------------------
Lab açılışı aşağıdaki şekildedir:
![Visible error-based SQL injection ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Visible%20error-based%20SQL%20injection%20ilk.png?raw=true)

Öncelikle bahsedilen cookie değerinin sonun `'` işareti konularak sayfanın davranışına bakıldığında sayfada ayrıntılı bir hata mesajı görünmekte. Bu sayfada bir SQLi olduğunu göstermekte.
![Visible error-based SQL injection kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Visible%20error-based%20SQL%20injection%20kontrol.png?raw=true)

Daha sonrasında hangi veri tabanının kullanılğınını bulalım. Önceki labların birinde versiyon tespiti için kullanılan yükleri tek tek denediğimizde `' and (select version()) = a'` yükünü kullandığımızda sayfa normal çalışmasına devam etmkete. Bu bize burada postgresql kullanıldığını göstermekte.
![Visible error-based SQL injection vdetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Visible%20error-based%20SQL%20injection%20vdetect.png?raw=true)

Şimdi veri tabanından istediğimiz bilgileri çıkarabiliriz. `' and select cast(select password from users limit 1)=1--` yükünü kullandığımızda sayfada ayrıntılı bir hata mesajı görünmekte. Bu mesajı incelersek bizim yolladığımız yükü uygulama `user` kısmından bitirmekte. Yani burada bir karakter sınırlaması olduğunu göstermekte.
![Visible error-based SQL injection limited](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Visible%20error-based%20SQL%20injection%20limited.png?raw=true)

Karakter sınırlamasını atlatmak için cookie değerini silmeli ve yükdeki kısaltmalıyız. `' 1=cast((select username from users limit 1)as int)--` yükünü kullanarak uygulamanın ayrıtılı bir hata mesajı vermesini sağlarız. Bu yük `users` tablosundaki en üst kısmındaki kullanıcının `username`'ini integer değere çavirmeye çalışır bu bize bu çevrilmeye çalışılan string değeri içeren bir hata mesajı döndürür. Böylece kullanıcı adını almış oluruz.
![Visible error-based SQL injection udetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Visible%20error-based%20SQL%20injection%20udetect.png?raw=true)

Kullanıcı adını bulmak için kullandığımız yükte `usersname`  yerine `password` kullanarak uyguladığımızda sayfa bu sefer parolanın içerdiği ayrıntılı bir hata mesajı dönmüş oluyor. Böylece hem kullanıcı adını hem de parolayı bulmuş oluruz.
![Visible error-based SQL injection pdetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Visible%20error-based%20SQL%20injection%20pdetect.png?raw=true)

Son olarak labı çözmek için bulmuş olduğumuz kullanıcı adı ve parolayı kullanarak labı çözüyoruz.
![Visible error-based SQL injection çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Visible%20error-based%20SQL%20injection%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Linkden labı kendiniz çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based
