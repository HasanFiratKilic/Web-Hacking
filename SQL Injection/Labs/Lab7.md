Bu laboratuvar, ürün kategorisi filtresinde bir SQL enjeksiyon güvenlik açığı içerir. Sorgunun sonuçları uygulamanın yanıtında döndürülür, böylece UNION saldırısı kullanarak diğer tablolardan veri alabilirsiniz.

Uygulamanın bir oturum açma işlevi vardır ve veritabanında kullanıcı adlarını ve şifreleri içeren bir tablo bulunur. Bu tablonun adını ve içerdiği sütunları belirlemeniz, ardından tablonun içeriğini alıp tüm kullanıcıların kullanıcı adlarını ve şifrelerini elde etmeniz gerekir.

Lab'ı çözmek için yönetici kullanıcısı olarak oturum açın.

Lab bizi şu şekilde karşılıyor:
![Lab7 ilk bakış](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20ilk%20bak%C4%B1%C5%9F.png?raw=true)

Kategorilerden herhangi birine tıklayarak url'de sorgu kısmını görebiliyoruz.
![Lab7 sorgu](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20sorgu.png?raw=true)

İlk olarak urldeki sorgu kısmında bir SQLi varmı kontrol edelim. Bunu sorgu kısmının sonuna `'` koyarak sorguyu bozmaya çalışırız eğer sayfa anormal çalışırsa SQLi olduğunu anlamış oluruz.
`'` yükünü yolladığımızda sayfa hata vermekte yani kategori kısmında bir SQLi olduğu anlaşılmakta.
![Lab7 sqli kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20sqli%20kontrol.png?raw=true)

Şimdi orjinal sorgunun kaç sütun döndürdüğünü bulmalıyız bunu `ORDER BY` betiğini kullanarak bulabiliriz. `' ORDER BY 1` ve `' ORDER BY 2` yüklerini yolladığımızda sayfa normal şekilde çalışmakta ama `' ORDER BY 3` yükünü yolladığımızda sayfa hata vermekte. Bu orjinal sorgunun 2 sütun döndüğünü göstermekte.
![Lab7 sütun sayısı](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20s%C3%BCtun%20say%C4%B1s%C4%B1.png?raw=true)

Sütun sayısını bulduktan sonra bu sütunlardan hangileri string değer kabul ettiğini bulmalıyız. `' SELECT NULL,NULL--` yükündeki null değerler yerine sırayla string değerler yollayarak kontrol ederiz. Sayfa hata verirse o sütun string kabul etmediğini öğrenmiş oluruz. Bu labda 2 sütunda string değer kabul etmekte. Aşağıdaki resimde iki sütuna da yolladığımız stringi sayfada basılmış görebilmekteyiz.
![Lab7 string](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20string.png?raw=true)

Veritabanına göre sorgularda farklılıklar olduğundan dolayı hangi veritabanı ve versiyonunu bulmalıyız. Bunu aşağıdaki yükleri kullanarak deneyebiliriz:
| Veritabanları | Betikler |
|---------------|------------|
| Oracle    		| `SELECT banner FROM v$version` veya `SELECT version FROM v$instance`|
| Microsoft    	| ` SELECT @@version` 																								 |
| PostgreSQL    | `SELECT version()`    																							 |
|MySQL					| `SELECT @@version`																										 |

Yukarıdaki yükler sırayla denenir ve sayfanın durumu incelenir. Aşağıda görüldüğü gibi bu lab PostgreSQL dir.
![Lab7 veritabanı kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20veritaban%C4%B1%20kontrol.png?raw=true)

Veritabanını öğrendiğimize göre sırada hangi tablolar olduğunu bulmakta. `' UNION SELECT TABLE_NAME,NULL FROM information_schema.tables--` yükü ile tablo adlarını çekeriz.`' UNION SELECT TABLE_NAME FROM information_schema.tables--` incelemesi:
- `'` : Veritabanına  gönderilen orijinal veriyi bitirir.
- `UNION` : Orijinal sorgunun yanına kendi sorgumuzu eklememizi sağlar. 
- `SELECT TABLE_NAME` : `information_schema.tables` tablosundaki `TABLE_NAME` sütununu getirir. Tüm tablo adlarını listelemiş olur.
- `NULL` : SQL'de `UNION` kullanırken, saldırganın sorgusu ile orijinal sorgunun sütun sayıları birebir eşleşmelidir.  `COLUMN_NAME` birinci sütunu doldurur, `NULL` ise ikinci sütunu doldurarak hata alınmasını engeller.
- `FROM information_schema.tables` : `information_schema.tables` adlı özel tabloya erişir. Bu tablo, o veritabanındaki tüm tabloların listesini barındırır.
- `--` : Kendisinden sonra gelen tüm kodları (orijinal sorgunun devamındaki tırnaklar veya parantezler gibi) devre dışı bırakır.
Aşağıda yükü uyguladıktan sonra tablo isimlerinin sayfada basılmış olduğu görünmekte. Resimde sayfanın sadece bir kısmı görünmekte çıktı resimdekinden daha uzun.

![Lab7 tablo names](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20tablo%20names.png?raw=true)
Tablo adında users geçen tablo adını kaydediyoruz bu labda bu tablo adı users_hstxsl. Bu tablodaki colon isimlerini almalıyız bunu `' UNION SELECT COLUMN_NAME,NULL FROM information_schema.columns WHERE TABLE_NAME = 'users_hstxsl'--` yükü ile yaparız. Yükün ayrıntılı incelenmesi:
- `SELECT COLUMN_NAME` : Tablonun sütunu çeker. Sütun isimlerini almış oluruz.
-  `FROM information_schema.column` : `information_schema.column` adlı özel tabloya erişir. Bu tablo, o veritabanındaki tüm colunların listesini barındırır.
- `WHERE TABLE_NAME = 'users_hstxsl'` : Veritabanındaki tüm sütun adlarını getirilmesinin yerine sadece users_hstxsl adlı tablonun sütun adlarını getirmeyi sağlar.

Aşağıda yükün uygulanmış hali görünmekte:
![Lab7 colon names](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20tablo%20names.png?raw=true) 

Sütun adlarınıda aldığımıza göre tablodaki kullanıcı adlarını ve şifreleri listeleyecek sorguyu yazabiliriz. `' UNION SELECT password_rictrr,username_vmludp FROM users_hstxsl--` bu yükünü uyguladıktan sonra administrator kullanıcısının ifresinin tpjzsj2e7681ia8fyxn1 olduğunu bulduk.
![Lab7 username and password](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20username%20and%20password.png?raw=true)

Son olarak kullanıc adı ve şifre ile giriş yapmak. Bulduğumuz şifre ile giriş yapmaya çalıştığımızda giriş işlemi başarıyla gerçekleşir ve lab çözülmüş olur.
![Lab7 çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab7%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Linkden sizde labaratuvarı çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables




