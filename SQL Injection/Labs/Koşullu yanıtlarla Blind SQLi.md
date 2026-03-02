# Laboratuvar: Koşullu yanıtlarla Blind SQL enjeksiyonu
Bu laboratuvar, kör SQL enjeksiyon güvenlik açığı içerir. Uygulama, analiz için bir izleme çerezi kullanır ve gönderilen çerezin değerini içeren bir SQL sorgusu gerçekleştirir.

SQL sorgusunun sonuçları döndürülmez ve hata mesajı görüntülenmez. Ancak, sorgu herhangi bir satır döndürürse uygulama sayfaya `Welcome back` mesajı ekler.

Veritabanında, `username` ve `password` adlı sütunlara sahip, `users` adlı farklı bir tablo bulunur. `administrator` kullanıcının şifresini bulmak için kör SQL enjeksiyon güvenlik açığını kullanmanız gerekir.

Lab'ı çözmek için yönetici kullanıcısı olarak oturum açın.

Lab bizi aşağıdaki gibi karşılıyor:
![Blind SQL injection with conditional responses ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20ilk.png?raw=true)

Web uygulamasının izleme için kullandığı çereze bir göz atalım. Ben bunun için firefox da Cookie-Editor([indirme link'i](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)) eklentisini kullandım. 
![Blind SQL injection with conditional responses cookie](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20cookie.png?raw=true)

TrackingId cookie'sinde değişiklik yapıp gözlemlediğimizde `Welcome back` yazısının görünmediğini görüyoruz.
![Blind SQL injection with conditional responses konrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20konrol.png?raw=true)

Bazı mantıksal yükler kullanarak sayfanın nasıl davrandığını gözlemleyelim. İlk olarak `' and 1=1--` yükünü uyguladığımızda  `Welcome back` yazısı görünür olmakta.
![Blind SQL injection with conditional responses bkonrol1](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20bkonrol1.png?raw=true)

İkincil olarak mantıksal olarak yanlış olan bir yük ile sayfayı gözlemleyelim. `' and 1=2--` yükünü sayfada uyguladığımızda `Welcome back` görünmüyor. Bu bize bazı mantıksal yükleri kullanarak veritabanında erşememiz gereken bilgilere erişebiliceğimizi gösterir.
![Blind SQL injection with conditional responses bkonrol2](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20bkonrol2.png?raw=true)

Sayfanın veri tabanını bulmaya çalışalım. `' AND (SELECT 'A' FROM version()) = 'A` yükünü uyguladığımızda sayfada `Welcome back` yazısı görünür olmakta bu bize uygulamada postgresql kullanıldığını gösterir. Yükün incelenmesi:
- `'` : Orijinal sorgudaki veri girişini kapatır. Sorguyu bozmadan yanına yeni bir mantıksal koşul (`AND`) ekleyebilmek için zemin hazırlar.
- `AND` : `Sorgu A AND Sorgu B` ifadesinde, sonucun "Doğru" dönebilmesi için her iki tarafın da doğru olması gerekir. Eğer eklediğimiz ikinci kısım (Sorgu B) doğruysa sayfa normal açılır. Eğer yanlışsa sayfa hata verir veya içerik değişir. Bu fark, saldırgana veritabanı hakkında bilgi sızdırır.
- `(SELECT 'A' FROM version())` : Bu parça, hedef sistemin PostgreSQL olup olmadığını test eder. Bu kısım veri tabanına göre değişmekte diğer sistemlerin versiyonunu gösteren betikler sırayla deneni ve sayfanın çalıma durumu gözlemlerip gözlemlere göre tespit yapılır.
	- `version()` Fonksiyonu: PostgreSQL'e özgü bir fonksiyondur (MySQL'de `@@version` veya sadece `version()` kullanılır ancak `FROM` takısı farklılık gösterir). 
	- `SELECT 'A'`: Eğer `version()` fonksiyonu başarıyla çalışırsa (yani veritabanı PostgreSQL ise), bu alt sorgu bize sadece `'A'` harfini döndürür.
- `= 'A` : Eğer `version()` fonksiyonu mevcutsa, denklem `'A' = 'A'` haline gelir ki bu her zaman doğrudur.
- 
Bu yükün sonunda neden `--` (yorum satırı) olmadığını veya neden eksik göründüğünü merak edebilirsin. Genellikle bu tür yükler, orijinal sorgunun sonundaki tırnağı kapatmak için bilerek tırnak işaretiyle bitirilir.

Veri tabanı tespiti için kullanılacak yükler:
| **Veritabanı** | **Test Sorgusu (Boolean)** |
|--|--|
|**PostgreSQL**  | `AND (SELECT 'A' FROM version())='A'` |
|**MySQL**|`AND (SELECT 1 FROM (SELECT version()) AS t)=1`|
|**Oracle**|`AND (SELECT 'A' FROM dual)='A'`|
|**MS SQL Server**|`AND (SELECT @@version) LIKE '%SQL%'`|
Yükün uygulanmış hali:
![Blind SQL injection with conditional responses vdetect](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20vdetect.png?raw=true)

Veri tabanını PostgreSQL olduğunu bulduğumuza göre `user` tablosunun var olup olmadığının kontrolünu yapmalıyız. `' AND (SELECT 'A' FROM user LIMIT 1) = 'A` yükünü uyguladığımızda sayfada `Welcome back` yazısı görünmekte bu `users` tablosunun olduğunu gösterir.
- `(SELECT 'A' FROM user LIMIT 1)` : Bu parça, veritabanında `user` isminde bir tablo olup olmadığını anlamasını sağlar.
	- `SELECT 'A'` : Tablonun içindeki gerçek verilerle (şifre vs.) ilgilenmez, sadece statik bir 'A' harfi döndürmeye çalışır. 
	- `FROM user` : Hedef tabloyu belirtir. Eğer veritabanında `user` adında bir tablo yoksa, bu sorgu hata verecek ve sayfa farklı çıktı verecek.
	- `LIMIT 1` : Sadece tek bir satır getirilmesini zorunlu kılar. Bazı veritabanları `AND` karşılaştırmasında alt sorgudan birden fazla satır gelirse hata verir. `LIMIT 1` bu riski ortadan kaldırarak temiz bir sonuç sağlar.

Yükün uygulanmış hali:
![Blind SQL injection with conditional responses tkontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20tkontrol.png?raw=true)

Şimdi `users` tablosunda `administrator` kullanıcısının olup olmadığını konrol etmeliyiz. `' AND (SELECT 'A' FROM users WHERE username = 'administrator') = 'A` yükünü uyguladığımızda sayfada  `Welcome back`  yazısını gömüş oluruz yani `administrator` kullanıcısı `users` tablosunda mevcut.
![Blind SQL injection with conditional responses ukontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20ukontrol.png?raw=true)

administrator kullacınısının parolasını bulmadan önce parola uzunluğunu bulmalıyız. `' and (SELECT LENGTH(password) FROM users WHERE username = 'administrator') > number--` yükünü kullanarak parola uzunluğunu evet ,hayır sorusuyla bulmaya çalışıyotuz.
Yükün inccelenmesi:
- `SELECT LENGTH(password)` : `password` sütunundaki verinin kaç karakterden oluştuğunu hesaplar.
- `FROM users WHERE username = 'administrator'` : Sorguyu tüm tablo yerine sadece `administrator` kullanıcısına odaklar.
- `> number` : Buradaki `number` yerine farklı sayılar denenir (Örn: `> 1`, `> 10`, `> 20`).
	- Sorgu 1 (`> 19` yazıldığında sayfada `Welcome back` yazısı görünür): Parola 10 karakterden uzundur.
	- Sorgu 2 (`> 20` yazıldığında sayfada `Welcome back` yazısı görünmez): Parola 20 karakter uzunluğundadır.

İlk başta yükteki number kısmına 10 yazıyoruz. Sayfayı gözlemlediğimizde `Welcome back`  yazısını sayfada görebiliyoruz. Bu parolanın 10 den büyük olduğunu gösterir. 
![Blind SQL injection with conditional responses Lpassword](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20Lpassword.png?raw=true)

Bu şekilde number sayısını arttıp azaltarak parolanın uzunluğunu bulmaya çalışıyoruz. En son tahmini bir sayı bulduğumuzda yükteki `>` işaretini `=` ile değiştirerek tahminimizden emin oluyoruz. Bu labda parola uzunluğu 20 olmatadır.
![Blind SQL injection with conditional responses Lpassword2](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20Lpassword2.png?raw=true)

Bul bilgileri kullanarak parolayı bulma için kullanacağımız yük `' AND (SELECT  SUBSTRING(password,number,1) FROM users WHERE username = 'administrator') > 'char`
yükünü kullanarak paroladaki karakterleri tek tek bulmaya çalışılır. Yükün incelenmesi:
- `SUBSTRING(password, number, 1)` : Bu fonksiyon, hedef metnin içinden belirli bir parçayı kesip alır.
	- `password`: Kaynak sütun. 
	- `number`: Kaçıncı karakterden başlanacağı (Burayı `1`, sonra `2`, sonra `3` yaparak ilerlenir).
	- `1` : Kaç karakter alınacağı (Her seferinde tek bir harf test edilir).
- `FROM users WHERE username = 'administrator'` : Sorgunun kapsama alanını daraltır. Sadece `administrator` kullanıcısının parolasını hedef alır.
- `> 'char'` : Bu kısım, sızdırma işleminin "motoru"dur. Saldırgan buradaki `'char'` yerine harfler veya ASCII değerleri koyar.
	-   Sorgu 1: `SUBSTRING(password,1,1) > '5'` : Sayfada `Welcome back` göründü. Demek ki 1. karakter 4-10 arasında.
	-   Sorgu 2: `SUBSTRING(password,1,1) > '7'` : Sayfada `Welcome back` görünmedi. Demek ki 1. karakter 4-8 arasında
	-   Sorgu 3: `SUBSTRING(password,1,1) = '6'` : Sayfada `Welcome back` göründü. Demek ki 1. karakter 6.
    -   Cevap: Doğru! İlk harfi bulduk: 'h'.

Bu işlem 20 karakter uzunluğunda parola için uzun olacağından [link](python)'deki python kodunu kullanarak tüm karakterler bulunur. Kod yükteki number ve char kısımlarına belirli değerler girer(number 1-20 kadar sayılar, char qwertyuıopasdfghjklzxcvbnm123467890 karakterlerini tek tek) ve sayfaya yollar sayfanın verdiği cevabın boyutunu(byte) alır ve kayıt eder. Eğer gönderilen char belirlenen konumda ise sayfanın cevabı `Welcome back` yazısını içerir buda sayfanın boyutunu büyütür. En son alınan tüm yanıtları büyükten küçüğe doğru yollanan yük değerleri ile birlikte sıralar. Bu şekilde parolayı bulmuş oluruz.
![Blind SQL injection with conditional responses pbulma](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20pbulma.png?raw=true)

Son olarak bulduğumuz parolayı kullanarak labı çözüyoruz.
![Blind SQL injection with conditional responses çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Blind%20SQL%20injection%20with%20conditional%20responses%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Linkden labı kendiniz çezebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses










