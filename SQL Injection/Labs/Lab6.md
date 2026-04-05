Bu laboratuvar çalışması, ürün kategorisi filtresinde bir SQL enjeksiyonu güvenlik açığı içermektedir. Enjekte edilen bir sorgudan sonuçları almak için UNION saldırısı kullanabilirsiniz.

Laboratuvar problemini çözmek için veritabanı sürüm dizesini görüntüleyin.

Lab bizi ilk açılışta şu şekilde karşılıyor:
![Lab6 ilk bakış](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab6%20ilk%20bak%C4%B1%C5%9F.png?raw=true)
Kategori kısmından bir kategoriye tıklatarak url'deki sorgu kısmını görebiliriz.
![Lab6 sorgu kısmı](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab6%20sorgu%20k%C4%B1sm%C4%B1.png?raw=true)
İlk adım url'de bir SQLi varmı kontrol etmek bunu `'` ekleyerek sorguyu bosmaya çalışarak kontrol edebiliriz. `'` işaretinin url'e koyum yolladığımızda sayfa hata vermekte bu bize url ksımında bir SQLi olduğunu göstermekte.
![Lab6 sqli kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab6%20sorgu%20k%C4%B1sm%C4%B1.png?raw=true)
İkinci adım olarak bu sayfada orjinal sorgunun kaç sütun döndüğünü öğrenmek bunu `ORDER BY` betiğini kullanarak bulabiliriz. `%27%20ORDER%20BY%203%23`(`' ORDER BY 3#` yükünün url encode edilmiş halidir. Encode işlemi için [CyberChef](https://cyberchef.io/) kullanabilirsiniz.) yükünü uyguladığımızda sayfanın hata vermesine neden olmakta yani orjinal sorgu bize 2 sütun dönmekte.
![Lab6 colon sayısı tespit](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab6%20colon%20say%C4%B1s%C4%B1%20tespit.png?raw=true)
Üçünçü adım bu sütunlardan hangisi veya hangileri string değer alabildiğini bulmak.
`%27%20UNION%20SELECT%20NULL%2CNULL%23`(`' UNION SELECT NULL,NULL#`) yükündeki null kısımlarına sırayla string değerler verilerek sayfanın davranışı gözlemlenir eğer sayfa normal çalışıyor ise o sütun string değer kubul etmektedir. Bu labda her iki sütunda string değeri kabul etmektedir. 
![lab6 string kabul](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/lab6%20string%20kabul.png?raw=true)
Çözüm için veritabanının versiyonunu yazdırmamız gerekmekte. `%27%20UNION%20SELECT%20NULL%2C%40%40version%23`(`' UNION SELECT NULL,@@version#`) yükü sayfaya veritabanının versiyonunu yazdırır.
`' UNION SELECT NULL,@@version#` sorgusunu incelemesi:
- `'` (Tek Tırnak): Mevcut SQL sorgusundaki veri girişini sonlandırır. Bu sayede veri tabanı, yazılımcının beklediği girdinin bittiğini sanır ve peşinden gelen komutlarımızı çalıştırmaya başlar.
- `UNION`: İki farklı `SELECT` sorgusunun sonuçlarını tek bir tabloda birleştirir. Orijinal sorgunun yanına kendi sorgumuzu "eklememizi" sağlar.
- `SELECT NULL, @@version`:
	- `NULL`: `UNION` operatörü kullanılırken, her iki sorgunun sütun sayıları eşit olmalıdır. Buradaki `NULL`, orijinal sorgudaki ilk sütunu karşılamak için yer tutucu olarak kullanılır. 
	- `@@version`: MySQL ve MariaDB'ye özgü bir sistem değişkenidir. Veri tabanının o anki sürüm numarasını ve işletim sistemi detaylarını döndürür.
* `#` (Diyez/Kare): MySQL'de yorum satırı anlamına gelir. Bu karakterden sonra gelen tüm kodlar veri tabanı tarafından yok sayılır. Bu, orijinal sorgunun sonunda kalan ve hataya sebep olabilecek fazlalık karakterleri (örneğin: `AND active=1`) etkisiz hale getirmek için kullanılır.
Aşağıdak labın çözülmüş hali görünmektedir. Yeşil kare içerisinde veritabanı versiyonu yazmakta.
![Lab6 çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/images/Lab6%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Aşağıdaki linkten labaratuvarı kendiniz çözebilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft
