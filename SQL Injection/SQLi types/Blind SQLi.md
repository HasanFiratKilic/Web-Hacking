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
