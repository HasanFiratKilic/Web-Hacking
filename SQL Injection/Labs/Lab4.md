Bu laboratuvar, ürün kategorisi filtresinde bir SQL enjeksiyon güvenlik açığı içerir. Sorgunun sonuçları uygulamanın yanıtında döndürülür, bu nedenle UNION saldırısı kullanarak diğer tablolardan veri alabilirsiniz. Böyle bir saldırı oluşturmak için önce sorgunun döndürdüğü sütun sayısını belirlemeniz gerekir. Bir sonraki adım, string verileriyle uyumlu bir sütun belirlemektir. 
Laboratuvar, sorgu sonuçlarında görünmesi gereken rastgele bir değer sağlayacaktır. Laboratuvarı çözmek için, sağlanan değeri içeren ek bir satır döndüren bir SQL enjeksiyon UNION saldırısı gerçekleştirin. Bu teknik, hangi sütunların string verileriyle uyumlu olduğunu belirlemenize yardımcı olur.

Lab açılışta şu şekilde karşılıyor:
![Lab4 ilk bakış](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab4%20ilk%20bakis.png?raw=true)
İlk olarak kategori filtrelerinden birine tıklıyoruz ve sorgu kısmını(kırmızı kare içerisinde) urlde görüyoruz.
![Lab4 sorgu bakış](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab4%20sorgu%20kismi.png?raw=true)
İkinci adım SQLi açığının olup olmadığını tespit etmekte bunuda sorgu kısmının sonına `'` koyarak yaparız. eğerki hata verirse bu SQL sorgusunun bozulduğunu gösterir ve bir SQLi olduğunu gösterir.
![Lab4 SQLi kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab4%20SQLi%20konrto.png?raw=true)
Üçüncü adım olarak orjinal sorgunun kaç sütun döndürdüğüdür. Geçmişte gösterilen iki yöntemden biri ile bulabiliriz. Bu labda `ORDER BY` betiğini kullanarak belirliyeceğiz.
Birinci sütundan başlayarak sütun index'ini artırarak sırayla ORDER BY ile sütünları sıralarsak dördüncü index'de hata verir buda bize orjinel sorguda üç sütun olduğunu gösterir.
![Lab4 sütun sayısı tespit](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab4%20sutun%20sayisi%20tespiti.png?raw=true)
Dördüncü adım hangi sütunlar string değer kabul ediceğini bulmakta bunu SELECT `UNION null,null,null--` yükündeki null değerlerinin yerine sırayla `'a'` yükünu koyarak yapıyoruz eğerki string değeri koyduğumuz sütun sayfada hataya neden oluyorsa o sütun string kabul etmediğini gösterir. Hata vermez ve verdiğimiz yükü orjiinal yükün bir yerinde sayfada basılı görürsek o sütun string kabul ettiğini tespit etmiş oluruz.
Uygulamaya birinci ve ikinci sütuna string değer yolladığımızda sayfada hata görünmekte ama ikinci sütuna gönderirsek sayfa çalışır ve yolladığımız yükü sayfada görürüz.
![Lab4 çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab4%20cozum.png?raw=true)

Aşağıdaki linkten labaratuvarı kendiniz de çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

