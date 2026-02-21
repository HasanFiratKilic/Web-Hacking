Bu laboratuvar çalışması, ürün kategorisi filtresinde bir SQL enjeksiyonu güvenlik açığı içermektedir. Enjekte edilen bir sorgudan sonuçları almak için UNION saldırısı kullanabilirsiniz.

Laboratuvar problemini çözmek için veritabanı sürüm dizesini görüntüleyin.

Laboratuvar bizi şu şekilde karşılıyor:
![lab5 ilk bakış](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab5%20ilk%20bak%C4%B1%C5%9F.png?raw=true)
Sonrasında kategori kısmından bir kategoriye tıklayarak url'de sorgu kısmını görmeye çalşıyoruz:
![lab5 sorgu kısmı](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab5%20sorgu%20k%C4%B1sm%C4%B1.png?raw=true)
İlk adım bir SQLi açığı varmı onun kontrolünü yapmalıyız. Bunu url'de gördüğümüz sorhunun sonuna bir `'`  koyarak SQL sorgusunu bozmaya çalışarak yaparız. Bu sayfanın normanden faklı çalışmasınan neden olursa bir SQLi olduğu söylenebilir. Url'e `'` yükünü yolladığımızda sayfa hata verir bu da bize burada bir SQLi olduğunu gösterir:
![lab5 sqli kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/lab5%20sqli%20kontrol.png?raw=true)
İkinci adımımız orjinal sorguda kaç sütun olduğunu bulmalıyız. `ORDER BY` betiğini kullanarak orjinal sutunlarda sıralama yaparız eğer olmayan bir sütunun sıralamaya çalışırsak bu hataya neden olur buda sıralamaya çalıştığımız sütunun olmadığını gösterir. `ORDER BY 3` yükünü yolladığımızda sayfa hata vermekte bu bize orjinal sorguda 2 sütun olduğunu göstermekte:
![lab5 sütun kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/lab5%20s%C3%BCtun%20say%C4%B1s%C4%B1%20kontrol.png?raw=true)
Üçüncü adım bu sütunların hangileri string değeri almakata bunun kontrolü yapılmalı. `' UNION SELECT NULL,NULL FROM DUAL--` yükünü yollayıp bu yükteki null kısımlara sırayla bir string değer yollayıp sayfanın durumunu kontrol etmek ve bu yollanan string değer sayfanın harhangi bir yerinde basılmışmı kontrol etmek. Yükteki `FROM DUAL` kısmının kullanılmasının sebebi oracle veritabanında `SELECT` betiğinden sonra bir tablo kullanılması orunludur. DUAL oracle veritabanında varsayılan olarak olan bir tablodur. Yükteki null kısımlara tek tek string değerler koyduğumuzda sayfa normal çalışmakta yani iki sütunda string değet kabul etmektedir.
![Lab5 sütun string kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab5%20s%C3%BCtun%20string%20kontrol.png?raw=true)
String değer alan sütünları bulduğumuza göre veritabanının versiyonunu `UNION` betiği ile sayfada yazdırabiliriz. Bunun için `' UNION SELECT BANNER,NULL FROM V$VERSION--` yükünü kulanacağız.
`' UNION SELECT BANNER,NULL FROM V$VERSION--` parçalara ayıralım:
* `'` (Tek Tırnak): Bu karakter, orijinal SQL sorgusunun dizisini (string) kapatmak için kullanılır.
* `UNION`: SQL'de iki farklı `SELECT` sorgusunun sonucunu tek bir sonuç kümesinde birleştirmek için kullanılır. Orijinal sorgunun yanına kendi sorgumuzu eklememizi sağlar.
* `SELECT BANNER, NULL`:  `BANNER`  Oracle veri tabanlarında sürüm bilgisini tutan sütun adıdır.
* `FROM V$VERSION`: Bu, Oracle veri tabanlarına özgü bir sistem tablosudur. Veri tabanının tam sürüm numarasını, işletim sistemi bilgilerini ve yama seviyelerini içerir.

![Lab5 çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/lab5%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)
Yukarıda görüldüğü gibi yük uygulandıktan sonra sayfada veritabanının versiyonu yazdırılmıştır(yeşil kare içerisinde işaretlenmiştir).

Aşağıdaki link'e tıklayarak labı çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle

