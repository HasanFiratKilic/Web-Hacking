# Blind SQL injection
Bu bölümde, kör SQL enjeksiyonu güvenlik açıklarını bulma ve istismar etme tekniklerini açıklayacağız.

## Blind SQL injection Nedir?
Kör SQL enjeksiyonu (Blind SQL Injection), bir web uygulamasının veritabanından veri çekmek için yapılan SQL enjeksiyonu saldırısının bir türüdür. Normal SQL enjeksiyonundan farklı olarak, saldırganın sorgu sonuçlarını doğrudan göremediği durumlarda uygulanır.
Kör (Blind) SQL Enjeksiyonu'nun Koşullu Yanıtlar (Conditional Responses) üzerinden sömürülmesi, veritabanına "Evet" veya "Hayır" cevabı alabileceğiniz mantıksal sorular sormaya benzer. Ekranda hiçbir veri görmezsiniz, ancak sayfanın değişip değişmemesinden cevabı anlarsınız.

Süreci bir dedektiflik oyunu gibi adım adım inceleyelim:

----------

### 1. Zafiyetin Tespiti (Evet/Hayır Testi)

Önce sayfanın verdiğimiz mantıksal komutlara tepki verip vermediğini ölçeriz. Bir ürün sayfası düşünün: `site.com/urun.php?id=5`
-   **Soru 1 (Doğru):** `...id=5 AND 1=1`
    -   _Sonuç:_ Sayfa normal açıldı (Ürün bilgileri ekranda). **Bu bir "EVET" sinyalidir.**
        
-   **Soru 2 (Yanlış):** `...id=5 AND 1=2`
    
    -   _Sonuç:_ "Ürün bulunamadı" hatası veya boş sayfa. **Bu bir "HAYIR" sinyalidir.**
        

Eğer bu iki deneme farklı sonuç veriyorsa, veritabanını konuşturmaya başlayabiliriz.

----------

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
	-    Sayfa hata vermedi ilk harf 'c' bu şekilde tük katakterle denenir.
    
    -   Saldırganlar genellikle süreci hızlandırmak için "büyüktür/küçüktür" sorguları kullanır: `AND (SELECT ASCII(SUBSTR(username,1,1))) > 100`

> [Koşullu yanıtlarla Blind SQL enjeksiyonu](Ko%C5%9Fullu%20yan%C4%B1tlarla%20Blind%20SQL%20enjeksiyonu)

