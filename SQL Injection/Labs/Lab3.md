Bu laboratuvar, ürün kategorisi filtresinde bir SQL enjeksiyon güvenlik açığı içerir. Sorgunun sonuçları uygulamanın yanıtında döndürülür, bu nedenle UNION saldırısı kullanarak diğer tablolardan veri alabilirsiniz. Bu tür bir saldırının ilk adımı, sorgu tarafından döndürülen sütun sayısını belirlemektir. 
Lab'ı çözmek için, null değerleri içeren ek bir satır döndüren SQL enjeksiyon UNION saldırısı gerçekleştirerek sorgu tarafından döndürülen sütun sayısını belirleyin.

Lab bizi aşağıdaki gibi karşılıyor.
![Lab3 iilk bakış](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab3%20ilk%20bak%C4%B1%C5%9F.png?raw=true)

İlk olarak bir kategoriye tıklıyoruz ve url kısmında sorgu(Kırmızı kare içerisinde) kısmını görüyoruz.
![Lab3 sorgu kısmı tam](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab3%20sorgu%20k%C4%B1sm%C4%B1%20tam.png?raw=true)

Sonrasında sayfada bir SQLi açığı olup olmadığının kontrolünü yapıyoruz. Bunu sorgu kısmının sonuna `'` koyarak yapabiliriz.
![Lab3 sqli kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab3%20sqli%20kontrol.png)
Yukarıda görüldüğü gibi hata mesajı ile karşılaştık. Bu bize bu sitenin kategori filtresinde bir SQLi açığının olduğunu gösterir.

Labaratuvarı çözme için orjinal sorgunun sütun sayısı bulunmalı. `ORDER BY` yöntemini kullanırsa 4. sütuna göre sıralamak istersek sayfa hata veriyor bu da bize orjinal sorguda 3 sütun olduğunu gösterir.
![Lab3 ilk çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab3%20ilk%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

`UNION SELECT` yöntemi ile çözmek istersek orjinal sorgudaki sütun sayısı ile yükteki null sayısı eşitlenene kadar null ekliyoruz sayfa normal çalışıyor ise o an yolladığımız null sayısı kadar orjinal sorguda sütun vardır. 3 tane null yükü yolladığımızda sayfa normal çalışmasını sürdürmektedir buda bize orjinal sorguda 3 sütun olduğunu gösterir.
![Lab3 ikici çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab3%20ikinci%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Labaratuarı aşağıdaki linkten kendiniz çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns
