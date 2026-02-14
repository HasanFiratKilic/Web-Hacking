# SQL injection UNION attacks
Eğer bir uygulamada SQLi varsa ve SQL sorgusunu yanıtları ile dönüyor ise bir saldırdan `UNION` betiği ile diğer tablolardan veri çekebilir. Bu tür ataklara UNION attacks denir.
Normalde bir sayfa belirli bir veriyi(örnek: ürünler) göstermek için tasarlanmıştır ama bu atak sayesinde saldırgan kullanıcı bilgileri, sistem bilgileri gibi verileri içeren tablolardan verileri alabilir.
## SQL UNION operatörü
`UNION` iki veya daha fazla `SELECT` betiğinin sonuç kümesini birleştirmeye yarar. `UNION` operatörü , sonuç kümesinden yenilenen satırları otomatik olarak kaldırır.

Bir UNION betiğinin çalıştırılması için bazı gereksinimler vardır:
- Birleşecek tabloların aynı sayıda sütüna ihtiyacı vardır.
- Sütünlar benzer veri türlerine sahip olmalıdır

SQLi UNION saldırısı gerçekleştirmeden önce şu iki gereksimi karşıladığından emin olun:
- Saldırıyı gerçekleştireceğiniz uygulamanın sorgusunun kaç sütun döndürdüğünü tespit edin.
- Uygulamanın döndürdüğü sütun ile sizin birleştirdiğiniz sutundan almak istediğiniz sütunun veri tiplerinin uyumluluğunu kontrol edin.

## Sütun sayısını belirleme
Orjinal sorgunun kaç sütun döndürdüğünü belirlemenin iki etkili yöntemi var.
Yötemlerden biri `ORDER BY` betiğini kullanarak sütunları çıktıda farklılık(hata, boş sayfa, ...) görene kadar arttımaktır. `ORDER BY` betiği verdiğiniz sütunun içerisindeki değerlere göre sıralama işlemi yapar. Eğerki olmayan sütuna göre sıralama yapmaya çalışırsanız hata alırsınız.
-   `' ORDER BY 1--`: (Hata yoksa: "Tamam, en az 1 sütun var.")
-   `' ORDER BY 2--`: (Hata yoksa: "Güzel, en az 2 sütun var.")
-   `' ORDER BY 3--`: (Hata yoksa: "Tamam, 3 de var.")
-   `' ORDER BY 4--`: **HATA ALINDI!** (Sonuç: "Demek ki orijinal sorguda tam 3 sütun var.")

Bir diğer yöntem farklı sayıda null değeri göndermek. Null geğerlerin sayısı orjinal sorgunun sütün sayısına eşitlendiğinde sayfa normal çıktısını verir.
- `' UNION SELECT null--` : (Hata varsa: "1 den fazla sütun var")
- `' UNION SELECT null,null--` : (Hata varsa: "2 den fazla sütun var")
- `' UNION SELECT null,null,null--` :(Hata yok sayfa normal çalışıyor:"O zaman orjinal sorguda 3 sütun var.)

> [Sütun sayısı tespiti örnek lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Lab3.md)
## Faydalı veri türüne sahip sütunları bulma
Genelde uygulamanın diğer tablolarından almak istediğimiz sütunlar string türünde olur. Bunu başarabilmemiz için orjine sorgunun hangi sütunlarının string değeri kabul ettiğini bulmamız gerekir.
Örneğin öncesinde orjinel sorgusunda 4 sütun olduğunu tespit ettiğimiz web uygulamasının veritabanının hangi sütunlarının string değerler aldığını sırayla şu yükler ile  buluruz.

    ' UNION SELECT 'a',null,null,null--
    ' UNION SELECT null,'a',null,null--
    ' UNION SELECT null,null,'a',null--
    ' UNION SELECT null,null,null,'a'--
Sütunun veri türü ile string( a ) uyuşmuyor ise uygulama hata verir. Eğer oluşmaz ve uygulama yanıtında enjekte edilen string( a ) değerini barındırıyorsa ilgili sütun string değerleri almakta uygundur.

> [SQLi UNION saldırısı uygun sütun örnek lab](Lab4)

