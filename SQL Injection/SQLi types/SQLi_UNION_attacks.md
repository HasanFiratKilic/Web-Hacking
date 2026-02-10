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

> [Sütun sayısı tespiti örnek lab](Lab3)

