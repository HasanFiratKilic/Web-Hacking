# Laboratuvar: SQL enjeksiyon saldırısı, Oracle'da veritabanı içeriğini listeleme
Bu laboratuvar, ürün kategorisi filtresinde bir SQL enjeksiyon güvenlik açığı içerir. Sorgunun sonuçları uygulamanın yanıtında döndürülür, böylece UNION saldırısı kullanarak diğer tablolardan veri alabilirsiniz.
Uygulamanın bir oturum açma işlevi vardır ve veritabanında kullanıcı adlarını ve şifreleri içeren bir tablo bulunur. Bu tablonun adını ve içerdiği sütunları belirlemeniz, ardından tablonun içeriğini alıp tüm kullanıcıların kullanıcı adlarını ve şifrelerini elde etmeniz gerekir.
Lab'ı çözmek için `administrator` kullanıcısı olarak oturum açın.

Lab ilk açılışı aşağıdaki şekilde:
![SQLi Oracle database list ilk bakis](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20ilk%20bakis.png?raw=true)

Kategori kısmında herhangi birisine tıklandığında url'de sorgu kısmı görünmekte.
![SQLi Oracle database list sorgu](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20sorgu.png?raw=true)

Öncelikle url'de bir SQLi varmı onun konrolünü yapmalıyız. Sorgu kısmının sonuna `'` işareti konularak orjinal sorguyu bozmaya çalışırız. Eğer sayfanın çalışmasında farklılık varsa url'de bir SQLi varlığı söylenebilir. Bu labı kontrol ettiğimizde sayfa hata vermekte yani SQLi olduğunu doğrulamış olduk.
![SQLi Oracle database list kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20kontrol.png?raw=true)

Database'nin Oracle olduğunu labın açıklamasından bildiğimizden bu adımı atlayıp sütun sayısını tespit etmeye geçiyoruz. `ORDER BY` betiğini kullanarak sayfanın çalışmasındaki farklılıkları gözlemleyerek sütun sayısını bulmayacalışıyoruz. `' ORDER BY 3--` yükünü kullandığımızda safanın hata verdiği görülmekte. Bu orjinal sorgunun iki sütun döndürdüğünü göstermekte.
![SQLi Oracle database list sütun](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20s%C3%BCtun.png?raw=true)

Sütun sayısı bulunduktan sonra bu sütunların kaçı string değer aldığını bulmakta. `' SELECT UNION NULL,NULL FROM DUAL--` yükündeki null değerlere sırayla string değer yollayıp sayfayı gözlemleyerek  bulunabilir. Bu labda iki sütununda string değerleri aldığını aşağıda görebiliriz.
![SQLi Oracle database list String](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20String.png?raw=true)

Şimdi veri tabanında hangi tabloların olduğunu bulmalıyız. `' UNION SELECT TABLE_NAME,NULL FROM all_tables--` yükünü yollayarak bulabiliriz. Yükün ayrıntılı anlatımı:
- `'` :  Uygulamanın SQL sorgusundaki veri giriş alanını kapatır.
- `UNION` : Orijinal sorgunun sonuçlarının altına, bizim kendi sorgumuzdan gelen sonuçları ekler.
- `TABLE_NAME, NULL` : 
	- `TABLE_NAME`: Oracle'ın sistem tablolarında tablo isimlerinin tutulduğu sütun adıdır. 
	- `NULL`: Bu bir "dolgu" (padding) malzemesidir.Sütun sayısını orjinal sorgununkine eşitlemeye yarar.
- `FROM all_tables` : Oracle Veritabanı yönetim sisteminde, kullanıcının erişebildiği tüm tabloların listesini tutan sistem tablosudur.
- `--` : SQL motoruna "Buradan sonrası yorumdur, dikkate alma" talimatı verir.

Yükün sayfaya uygulanmış hali:
![SQLi Oracle database list tname](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20tname.png?raw=true)

Tablo adları asından içerisinde users kelimesi geçen tablo adı `USERS_JIEYOM` olduğu görülmekte. Şimdi bu tablonun sütun adşarını bulmakta. `' UNION SELECT COLUMN_NAME,NULL FROM all_tab_columns WHERE TABLE_NAME = 'USERS_JIEYOM'--` yükünü kullanarak `USERS_JIEYOM` tablosunun sütun adlarını listeleliz. Yükün ayrıntılı incelemesi:
- `COLUMN_NAME`: `all_tab_columns` tablosundaki sütun isimlerini barındıran kolonun adıdır.
- `FROM all_tab_columns` : Veritabanındaki tüm tabloların içindeki tüm sütun isimlerini, veri tiplerini ve özelliklerini burada saklar.
- `WHERE TABLE_NAME = 'USERS_JIEYOM'` : Sadece ismi `USERS_JIEYOM` olan tabloya ait sütunları getirmesini söyler.

Yükün sayfaya uygulanmış hali:
![SQLi Oracle database list cname](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20cname.png?raw=true)

`USERS_JIEYOM` tablosunun sütun adlarında işimize yarayanlar `USERS_JIEYOM`,`PASSWORD_MGREUM`  adlı colonlar. Şimdi tüm bu bilgileri kullanarak yollayacağımız yük ile web uygulamasındali kullanıcı adlarını ve parolalarını çekmekte. `' UNION SELECT USERNAME_QSFXYI,PASSWORD_MGREUM FROM USERS_JIEYOM--` yükünü kullanarak `USERS_JIEYOM` tablosundaki tüm kullanıcı adlarını ve parolalarını sayfaya yazdırmayı sağlar.
Yükün uygulanmı hali(yeşil kare içerisinde `administrator` kullanıcısının bilgileri var. ):
![SQLi Oracle database list Uname&p](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20Uname&p.png?raw=true)

Son olarak labın çözme koşulu olan `administrator` kullanıcısı ile giriş yapmakta bir önceki adımda `administrator` kullanıcısının şifresini `qrtjnj3idoacjm0bcplh` olarak bulduk.
Bulduğumuz kullanıcı adını ve şifresini girdikten sonra giriş başarıyla gerçekleşti ve lab çözülmüş oldu.
![SQLi Oracle database list çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20Oracle%20database%20list%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Aşağıdaki linkten labı kendiniz çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle






