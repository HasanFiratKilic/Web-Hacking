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

> [SQL sorgusunda `WHERE` tümlecinde SQLi açığına örnek lab](Lab1)


		





 

 

