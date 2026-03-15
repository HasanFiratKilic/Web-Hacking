# Blind SQL injection
Bu bölümde, kör SQL enjeksiyonu güvenlik açıklarını bulma ve istismar etme tekniklerini açıklayacağız.

## Blind SQL injection Nedir?
Kör SQL enjeksiyonu (Blind SQL Injection), bir web uygulamasının veritabanından veri çekmek için yapılan SQL enjeksiyonu saldırısının bir türüdür. Normal SQL enjeksiyonundan farklı olarak, saldırganın sorgu sonuçlarını doğrudan göremediği durumlarda uygulanır.
Kör (Blind) SQL Enjeksiyonu'nun Koşullu Yanıtlar (Conditional Responses) üzerinden sömürülmesi, veritabanına "Evet" veya "Hayır" cevabı alabileceğiniz mantıksal sorular sormaya benzer. Ekranda hiçbir veri görmezsiniz, ancak sayfanın değişip değişmemesinden cevabı anlarsınız.

Süreci bir dedektiflik oyunu gibi adım adım inceleyelim:
### 1. Zafiyetin Tespiti (Evet/Hayır Testi)

Önce sayfanın verdiğimiz mantıksal komutlara tepki verip vermediğini ölçeriz. Bir ürün sayfası düşünün: `site.com/urun.php?id=5`
-   **Soru 1 (Doğru):** `...id=5 AND 1=1`
    -   _Sonuç:_ Sayfa normal açıldı (Ürün bilgileri ekranda). **Bu bir "EVET" sinyalidir.**
        
-   **Soru 2 (Yanlış):** `...id=5 AND 1=2`
    
    -   _Sonuç:_ "Ürün bulunamadı" hatası veya boş sayfa. **Bu bir "HAYIR" sinyalidir.**
        

Eğer bu iki deneme farklı sonuç veriyorsa, veritabanını konuşturmaya başlayabiliriz.

### 2. Veri Çekme Stratejisi

Veritabanındaki bir tablo ismini veya şifreyi öğrenmek için karakter karakter ilerlememiz gerekir. Bunun için `SUBSTR()` (metni parçala) ve `ASCII()` (harfi sayıya çevir) fonksiyonlarını kullanırız.

#### Adım A: Uzunluğu Bulma

Önce aradığımız verinin kaç karakter olduğunu bulmalıyız.

-   `AND (SELECT LENGTH(username) FROM users WHERE id=1) = 4`
    
    -   Sayfa hata verirse: Kullanıcı adı 4 harfli değil.
        
-   `AND (SELECT LENGTH(username) FROM users WHERE id=1) = 5`
    
    -   Sayfa normal yüklenirse: **Bulduk! Kullanıcı adı 5 karakterli.**
        

### Adım B: Karakterleri Tahmin Etme (Brute Force)

Şimdi 5 karakterin her birini tek tek deniyoruz:

-   **1. Harf için:** `AND (SELECT SUBSTR(username,1,1) FROM users WHERE id=1) = 'a'`
    
    -   Sayfa hata verdi -> İlk harf 'a' değil.
        
-   **1. Harf için:** `AND (SELECT SUBSTR(username,1,1) FROM users WHERE id=1) = 'b'` 
	-   Sayfa hata verdi -> İlk harf 'b' değil.
    
-   **1. Harf için:** `AND (SELECT SUBSTR(username,1,1) FROM users WHERE id=1) = 'c'`
	-    Sayfa hata vermedi ilk harf 'c' bu şekilde tüm katakterle denenir.
    

> [Koşullu yanıtlarla Blind SQL enjeksiyonu Lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Ko%C5%9Fullu%20yan%C4%B1tlarla%20Blind%20SQLi.md)

## Hata Tabanlı SQL Enjeksiyonu (Error-based SQL Injection)
Hata tabanlı SQL Enjeksiyonu (Error-based SQL Injection), veritabanından dönen hata mesajlarını kullanarak hassas verileri çıkardığınız veya tahmin ettiğiniz bir siber saldırı yöntemidir. Bu yöntem, uygulamanın normalde veri döndürmediği "kör" (blind) durumlarda bile oldukça etkilidir.

### Koşullu Hataları Tetikleyerek Kör SQL Enjeksiyonunu İstismar Etme
Normal bir Blind SQL Injection'da sayfa içeriğine bakarsın. Ancak sayfa hiç değişmiyorsa, sunucunun HTTP 500 (Internal Server Error) döndürüp döndürmediğine bakarsın.

Buradaki sihirli değneğimiz Mantıksal Bomba yerleştirmektir. Genellikle matematiksel olarak imkansız olan `1/0` (sıfıra bölme hatası) kullanılır.

1.  `xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a`
    
2.  `xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a`
    

Bu girişler, bir koşulu test etmek için `CASE` anahtar kelimesini kullanır ve koşulun doğru olup olmamasına göre farklı bir ifade döndürür:

-   **İlk girişte:** `CASE` ifadesi `'a'` değerini döndürür, bu da herhangi bir hataya neden olmaz.
    
-   **İkinci girişte:** İfade `1/0` değerini döndürür, bu da **sıfıra bölünme (divide-by-zero)** hatasına yol açar.

Eğer bu hata, uygulamanın HTTP yanıtında bir değişikliğe (örneğin 500 Internal Server Error) neden oluyorsa, enjekte edilen koşulun doğru olup olmadığını belirleyebilirsiniz.
### Örnek Senaryo:

Bir web sitesine şu soruyu sorduğunu hayal et: _"Eğer adminin şifresinin ilk harfi 'A' ise kendini imha et (hata ver), değilse normal davran."_

-   **Durum A (Yanlış tahmin):** Şifre 'B' ile başlıyorsa, bomba tetiklenmez. Sayfa normal açılır (HTTP 200).
    
-   **Durum B (Doğru tahmin):** Şifre 'A' ile başlıyorsa, `1/0` işlemi çalışır. Veritabanı "Hata!" der ve web sitesi çöker veya hata mesajı verir (HTTP 500).


> [Koşullu hatalarla kör SQL enjeksiyonu lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Ko%C5%9Fullu%20hatalarla%20k%C3%B6r%20SQL%20enjeksiyonu.md)


### Ayrıntılı SQL hata mesajları aracılığıyla hassas verilerin çıkarılması
Hata Tabanlı SQL Enjeksiyonu (Error-Based SQLi), saldırganın veritabanı sunucusunu kasıtlı olarak geçersiz sorgular göndermeye zorladığı ve veritabanından dönen ayrıntılı hata mesajlarını kullanarak içerideki verileri (tablo adları, kullanıcı bilgileri, versiyonlar vb.) dışarı sızdırdığı bir yöntemdir.

Bu yöntem, "Kör (Blind) SQLi" yönteminden çok daha hızlıdır çünkü veriyi saniye saniye tahmin etmek yerine, doğrudan hata mesajının içinde bir metin olarak okumanıza olanak tanır.

Modern programlama dillerinde "Try-Catch" blokları hatayı yakalar; ancak düzgün yapılandırılmamış sistemlerde veritabanı hatayı doğrudan ekrana yansıtır. Saldırgan, sorgunun içine öyle bir fonksiyon yerleştirir ki, veritabanı hata verirken "Hata: 'admin_parolası' geçerli bir tam sayı değildir" gibi bir çıktı üretir.

#### Teknik Örnek (MSSQL):

Saldırgan, bir sayı bekleyen parametreye veritabanı versiyonunu döndüren bir fonksiyon ekler: `' AND 1=CONVERT(int, (SELECT @@version))`

**Sonuç:** Veritabanı, versiyon bilgisini (string) bir tam sayıya (int) dönüştüremez ve şu hatayı döndürür:

> _Conversion failed when converting the varchar value 'Microsoft SQL Server 2019...' to data type int._

Saldırgan burada aradığı bilgiyi (versiyonu) hata mesajının içinde açıkça görmüş olur.

> [Görünür hata tabanlı SQL enjeksiyonu Lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Visible%20error-based%20SQLi.md)

## Zaman gecikmelerini tetikleyerek Blind SQL enjeksiyonundan yararlanma
Normal SQL enjeksiyonunda veriler sayfada basılır; "Boolean" tabanlı SQL enjeksiyonunda sayfa yapısındaki değişikliklere (True/False) bakılır. Ancak Zaman Gecikmeli SQLi'de sunucu hiçbir farklı yanıt vermez.

Buradaki tek gösterge yanıt süresidir. Saldırgan, veritabanına "Eğer bu bilgi doğruysa 5 saniye bekle" komutu gönderir. Eğer yanıt 5 saniye geç gelirse, saldırgan sorduğu sorunun cevabının "Evet" olduğunu anlar.
 
 Zaman gecikmesini tetikleme teknikleri veri tabanı türüne göre değişmekte. Aşağıdaki yük ile zaman geçikmesi tetiklenebilir.

     '; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--      
Bu sorguyu şu parçalara bölebiliriz:

1.  **`SUBSTRING(Password, 1, 1)`**: Şifrenin 1. karakterini al.
    
2.  **`> 'm'`**: Bu karakter 'm' harfinden sonra mı geliyor? (Örn: n, o, p...)
    
3.  **`IF (...) WAITFOR DELAY '0:0:10'`**: Eğer bu şart doğruysa, veritabanına "10 saniye boyunca hiçbir şey yapmadan dur" talimatı verilir.

Örnek senaryo:
| Gönderilen Sorgu (Şart Kısmı) | Sunucu Tepkisi |Sonuç|
|--|--|--|
| `...SUBSTRING(Pass, 1, 1) > 'm'` | 10 Saniye Gecikme |Harf 'm'den büyük (n-z arası). |
|`...SUBSTRING(Pass, 1, 1) > 't'`|Hemen Yanıt|Harf 't'den büyük değil (n-t arası).|
|`...SUBSTRING(Pass, 1, 1) = 's'`|10 Saniye Gecikme|Buldun! İlk harf 's'.|

Aynı işlem 2. karakter, 3. karakter diye devam eder. Şifre 10 karakterliyse ve her karakter için ortalama 5-6 soru sorulursa, tüm şifre sessizce ele geçirilir.

>  [Zaman gecikmeleri ve bilgi alma ile Blind SQL enjeksiyonu lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/BSQLi%20with%20time%20delays%20and%20information%20retrieval.md)
