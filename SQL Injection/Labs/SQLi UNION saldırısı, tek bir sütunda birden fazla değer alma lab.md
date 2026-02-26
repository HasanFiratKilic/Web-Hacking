# Laboratuvar: SQL enjeksiyonu UNION saldırısı, tek bir sütunda birden fazla değer alma
Bu laboratuvar çalışması, ürün kategorisi filtresinde bir SQL enjeksiyonu güvenlik açığı içermektedir. Sorgunun sonuçları uygulamanın yanıtında döndürüldüğü için, diğer tablolardan veri almak üzere bir UNION saldırısı kullanabilirsiniz.
Veritabanında, `username` ve `password` adlı sütunlar içeren `users` adlı farklı bir tablo bulunmaktadır.
Laboratuvarı çözmek için, tüm kullanıcı adlarını ve parolaları alan bir SQL enjeksiyon UNION saldırısı gerçekleştirin ve bu bilgileri kullanarak yönetici kullanıcısı olarak oturum açın.

Lab ilk açılışta bizi aşağıdaki gibi karşılıyor:
![İlk bakış](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20ilk%20bak%C4%B1%C5%9F.png?raw=true)

Kategorilerden herhangi birine tıklayarak url'deki sorgu kısmını görmüş oluruz.
![Sorgu](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20Sorgu.png?raw=true)

`'` işaretini sorgu kısmının sonuna yerleştirerek url'de bir SQLi varmı onun konrolünü yapmış oluruz. Eğer yükü uyguladığımızda sayfanın çalışmasında bir farklılık varsa burada bir SQLi olduğunu söyleyebiliriz. Bu labda yükü uyguladığımızda sayfa hata vermekte.
![Kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20Kontrol.png?raw=true)

Kendi sorgumuzu onjinal sorgunun üzerine eklemeden önce orjinal sorgunun kaç sütun döndürdüğünü bulmalıyız. Bunu `ORDER BY` betiğini kullanarak gerçekleştiririz. Bu labda `' ORDER BY 3--` yükünü uyguladığımızda sayfa hata vermekte bu da bize orjinal sorgunun 2 sütun döndürdüğünü göstermekte.
![Sütun](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20Column.png?raw=true)

Sıra orjinal sorgunun döndürdüğü sütunları kaçının string değer kabul ettiğini bulmakta. `' UNION SELECT NULL,NULL--` yükündeki null değerlere sırayla string değerler vererek yükü yollarız eğer sayfa hata verirse o sütun string değer kabul etmediğini anlamış oluruz. Bu labda ilk sütun string kabul etmemekte ikinci sütun etmekte.
![String](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20String.png?raw=true)

Uygulamanın hangi veritabanını kullandığına göre sorgularda farklılıklar olabilmekte. Bu nedenden uygulamanın hangi veritabanını ve sürümünü kullandığını bulmalıyız. Her veritabanının kendine özgü bir versiyon sorgu betiği var. İnternetten bu sorgular bulunup herbiri tek tek denenerek uygulamanın hangi veritabanını kullandığı bulunabilir. Bu lab postgresql kullanmakta bunun için kullanılan sorgu `SELECT version()`. `' UNION SELECT NULL,version()--` yükünü kullanarak sayfaya veritabanı versiyonunu yazdırmış oluruz.
![Versiyon](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20Vdetection.png?raw=true)

Şimdi bu web uygulamasındaki tabloları yazdırmakta. Lab açıklamasında tablo ismi ve sütun isimleri verilmekte ama yinede kontol amaçlı tablo ve sütun adlarını yazdıralım. `' UNION SELECT NULL,TABLE_NAME FROM information_schema.tables--` yükü bize tablo isimlerini sayfaya yazılmasını sağlar. Aşağıdaki resimde user tablosunun var olduğu görünmekte.
![Tablo adları](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20Tname.png?raw=true)

Usur tablosunun olduğunu doğruladıktan sonra `username` ve `password` sütunlarını doğrulakta. `' UNION SELECT NULL,COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = 'users'--` yükü ile `user` tablosuna ait sütun adlarını yazdımış oluruz. Yükü uyguladığımızda `username` ve `password` sütunlarının olduğunu doğrulamış olduk.
![Sütun adları](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20Cname.png?raw=true)

Bulduğumuz bu bilgileri kullanarak son bir yük ile users tablosundaki kullanıcıları ve parolaları tek bir sütunda yazdırmakta. `' UNION SELECT NULL,username||' : '||password FROM users--` yükünü kullanarak `users` tablosundaki kullanıcı adlarını ve parolalarını tek bir sütunda yazdırmış oluruz. Yükün ayrıntılı anlatımı:
* `'` : Veritabanına sorgu bitti der.
* `UNION SELECT` : Orijinal sorgunun sonuçlarıyla bizim sorgumuzdan gelecek verileri birleştirir.
* `NULL` : `UNION` kuralı gereği, her iki sorgunun sütun sayısı aynı olmalıdır. Eğer orijinal sorgu 2 sütun döndürüyorsa, biz de 2 sütun döndürmeliyiz. Bizim asıl verimiz ikinci sütunda olduğu için ilkini `NULL` ile geçiştiriyoruz.
* `username||' : '||password` : Bu parça Oracle ve PostgreSQL gibi veritabanlarına özgü bir sözdizimidir. Birden fazla sütundaki veriyi (kullanıcı adı ve şifre) tek bir sütunmuş gibi tek seferde çekmeyi sağlar.
	* `||` Operatörü: İki veya daha fazla metni birbirine yapıştırır. 
	* `' : '` Ayırıcı: Kullanıcı adı ve şifre arasına iki nokta üst üste koyar (Örn: `admin : 123456`).
* `FROM users` : Verinin hangi tablodan çekileceğini belirtir.
* `--` : Sorgunun devamındaki tüm karakterleri yorum satırı yaparak devre dışı bırakır.

Yükün uygulanmuş hali:
![u&p](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20Cname.png?raw=true)

Son olarak bulduğumuz kullanıcı adını ve parolasını girerek labı çözüyoruz:
![çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20UNION%20attack,%20multiple%20values%20%20single%20column%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Linkden labı kendiniz çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column



