# SQL injection
Bu bölümde şunları açıklanıyor

 - Sql injection nedir
 - Sql injection türlerin nelerdir
 - Sql injection nasıl tespit edilir
 
 ## SQL injection (SQLi) nedir?
 Sqli kötü niyetli kişinin hedef web uygulamasını sorgularına müdahale ederek istediği sonuçları dönürmesini sağladığı açık. Bu bir saldırganın normalde erişemeyeceği verilere erişmesini sağlar.
 ## SQL injection tespiti
 Veri tabanıyla etkişime giren noktaladaki değişiklik yaparak uygulamanın verdiği yanıtlar izlenir ve anomalilikler tespit edilmeye çalışılır.
 - **Tek/Çift Tırnak**:  `id=1'` veya `id=1"` yazdığınızda sayfada bir anormallik(hata,içerik kaybolması) var ise bu SQL söz dizimi hatasına neden olduğunu gösterir. Yani sql sorgusu manüpile edilebilir.
 - **Mantıksal Doğrulama**: `or and 1=1`(sayfa normal döner) ,`or and 1=2`(hata,farklı sonuç veya baoş sayfa döner)
 - **Zaman Tabanlı Tespit**: Sayfa hiçbir değişiklik vermiyor ise sayfayı beklemeye zorlayan zaman tabanlı yükler kullanılarak gecikme süreleri üzerinden tespit edilebilir.

## Sorgunun Farklı yerlerinde SQLİ
Yaygın SQLi açığı SELECT sorgusunun WHERE bölümünde çıkar. Ancak SQLi açığı songunun farklı yerlerinde ve farklı sorg türlerinde çıkabilir. SQLi ortaya çıktığı farklı yerler:
- `INSERT` ve `UPDATE` ile kayıt oluştururken veya güncelleme içeren sorgularda.
- `ORDER BY` ve `GROUP BY` yan tümleçlerinin içerisinde
-  `SELECT` tümlecinde, tablo veya sütun adı içerisinde
## SQLi Örnekleri
Bir çok SQLi güvenlik açığı, saldırısı ve tekniği varır. Yaygın olanlardan bazıları:

1.  **In-Band (Bant İçi) SQLi**
Bu yöntemde saldırgan, saldırıyı gerçekleştirdiği aynı iletişim kanalını kullanarak sonuçları doğrudan alır. En yaygın ve kolay tespit edilen türdür.
	- **Error-Based (Hata Tabanlı) SQLi:**
		*   Veritabanının döndürdüğü hata mesajlarını kullanarak veritabanı yapısı (tablo isimleri, kolonlar...) hakkında bilgi toplar.
	- **Union-Based SQLi:**
		- `UNION` operatörü kullanılarak, orijinal sorgunun sonucuna saldırganın istediği başka bir tablonun verileri eklenir.
2. **Inferential (Çıkarımsal / Blind) SQLi**
Saldırgan sonucu direk ekrande göremez sunucunun verdiği tepkilere göre çıkarım yapar.
	- **Boolean-Based Blind SQLi:**
		- Sorgunun sonucuna göre sayfanın verdiği tepki gözlemlernir.
	- **Time-Based Blind SQLi:**
		-	Veritabanı tepki vermiyorsa zamana bağlı yükler ile sayfanın tepkisi gözlemlenir.

> [SQL sorgusunda `WHERE` tümlecinde SQLi açığına örnek lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Lab1.md)

## SQLi ile kimlik doğrulama atlatma
Bir sitede kimlik doğrulama gerçekleştirmek için kullanıcı adınızı ve şifrenizi girdiğinizde uygulama arkada şuna benzer bir sorgu çalıştırır:

    SELECT * FROM users WHERE username = 'kullanıcı adı' AND password = 'parola' 
Eğer veritabanında bu kullanıcı adı ve şifreyle uyuşan bir kayıt var ise giriş gerçekleştirilir. Sorgunun kullanıcı adı kısmından sonrasını yorum satırı haline getiribilirsek uygulamaya sadece kullanıcı adını girerek giriş yapabiliriz. Bunu da formda kullanıcı adının sonuna `' --` ekleyerek yaparız. Bu işelem sonrasında sorgu şu hale gelir:

    SELECT * FROM users WHERE username = 'kullanıcı adı' -- ' AND password = ''
Sorguda `--` işaretinden sonrası yorum satırı olacağından uygulma bu kısmı yürütmez ve sadece kullanıcı adını bilerek giriş gerçekleştirilir.
> [SQLi kimlik doğrulama atlatma örnek lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Lab2.md)

## Diğer tablolardan veri alma
Uygulama slq sorgusunun sonuçlarını yanıt olarak verdiği durumlarda, saldırgan bir SQLi açığı kullanarak uygulamanın diğer tablolarından `UNION` betiğini kullanarak ek sorgularla veri alabilir. 

> [SQLi UNION saldırıları.](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/SQLi%20types/SQLi_UNION_attacks.md)

## Blind SQL injection vulnerabilities
SQL enjeksiyonunun birçok örneği Blind güvenlik açıklarıdır. Bu, uygulamanın SQL sorgusunun sonuçlarını veya veritabanı hatalarının ayrıntılarını yanıtlarında döndürmediği anlamına gelir. Blind güvenlik açıkları yine de yetkisiz verilere erişmek için kullanılabilir, ancak kullanılan teknikler genellikle daha karmaşık ve uygulanması daha zordur.

Aşağıdaki teknikler, güvenlik açığının niteliğine ve ilgili veritabanına bağlı olarak Blind SQL enjeksiyonu güvenlik açıklarından yararlanmak için kullanılabilir:
* Tek bir koşulun doğruluğuna bağlı olarak uygulamanın yanıtında algılanabilir bir fark tetiklemek için sorgunun mantığını değiştirebilirsiniz. Bu, bazı Boolean mantığına yeni bir koşul eklemeyi veya sıfıra bölme gibi bir hatayı koşullu olarak tetiklemeyi içerebilir.
* Sorgunun işlenmesinde koşullu olarak bir zaman gecikmesi tetikleyebilirsiniz. Bu, uygulamanın yanıt verme süresine bağlı olarak koşulun doğruluğunu çıkarmanızı sağlar.

> [Blind SQL injection]()
		





 

 

