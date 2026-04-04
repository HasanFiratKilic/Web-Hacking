# Authentication Güvenlik Açıkları
## Authentication Nedir?

**Authentication**, bir sisteme erişmeye çalışan kullanıcının veya istemcinin _gerçekten iddia ettiği kişi olup olmadığını_ doğrulama sürecidir.

İnternete bağlı web siteleri ve uygulamalar potansiyel olarak tüm dünyaya açıktır. Bu durum, sistemi kötü niyetli kişilerden korumak ve veri güvenliğini sağlamak için **güçlü kimlik doğrulama mekanizmalarını** web güvenliğinin en kritik parçası haline getirir.

### Temel Kimlik Doğrulama Faktörleri

Kimlik doğrulama mekanizmaları, kullanıcıyı doğrulamak için çeşitli teknolojiler kullanır ve genel olarak üç temel kategoriye (faktöre) dayanır:

-    **Bildiğiniz bir şey (Bilgi Faktörü - Knowledge):** Sadece kullanıcının bildiği gizli verilerdir.
    
    -   _Örnek:_ Parolalar, PIN kodları veya güvenlik sorularının cevapları.
        
-    **Sahip olduğunuz bir şey (Sahiplik Faktörü - Possession):** Kullanıcının fiziksel olarak elinde bulundurduğu bir nesnedir.
    
    -   _Örnek:_ Cep telefonu (SMS veya doğrulama uygulamaları), donanımsal güvenlik anahtarları (USB token) veya akıllı kartlar.
        
-    **Olduğunuz veya yaptığınız bir şey (Kalıtsal Faktör - Inherence):** Kullanıcıya özgü benzersiz fiziksel veya davranışsal özelliklerdir.
    
    -   _Örnek:_ Biyometrik veriler (parmak izi, yüz veya retina taraması) ve davranışsal kalıplar (klavyede yazma hızı vb.).
        

> **Not:** Günümüz modern web güvenliğinde, sistemleri daha iyi korumak adına bu faktörlerin en az ikisi bir arada kullanılır. Buna **Çok Faktörlü Kimlik Doğrulama (MFA - Multi-Factor Authentication)** denir.

##  (Authentication) ve (Authorization) Arasındaki Fark Nedir?

Bu iki terim genellikle birbirinin yerine kullanılsa da, bilgi güvenliğinde tamamen farklı iki süreci ifade ederler:

-   **Authentication:** Bir kullanıcının _iddia ettiği kişi olup olmadığını_ doğrulama sürecidir. Sistemin **"Sen kimsin?"** sorusuna verdiği cevaptır.
    
-   **Authorization:** Kimliği doğrulanmış bir kullanıcının sistem içinde _neler yapabileceğini_ ve _nerelere erişebileceğini_ belirleme sürecidir. Sistemin **"Bunu yapmaya iznin var mı?"** sorusuna verdiği cevaptır.
    

### Örnek Senaryo: Carlos123

Bu iki kavramın nasıl birlikte çalıştığını bir örnek üzerinden inceleyelim:

1.  **Authentication Aşaması:** Birisi "Carlos123" kullanıcı adıyla bir web sitesine giriş yapmaya çalışır. Sistem, girilen parolanın (veya diğer faktörlerin) doğruluğunu kontrol ederek bu kişinin hesabı oluşturan asıl Carlos123 olup olmadığını teyit eder.
    
2.  **Authorization Aşaması:** Carlos123 başarıyla giriş yaptıktan (kimliği doğrulandıktan) sonra, sistemdeki izinleri devreye girer. Carlos123 sıradan bir kullanıcı mı yoksa bir yönetici (admin) mi? Diğer kullanıcıların kişisel bilgilerini görebilir mi? Başka bir kullanıcının hesabını silebilir mi? Sistemde yapabileceği işlemleri belirleyen şey onun yetkileridir.

  **Özet**:
|Özellik|Authentication  |Authorization |
|--|--|--|
| **Temel Soru** | Sen kimsin? |Neler yapabilirsin? |
|**İşlev**|Kullanıcının kimliğini kanıtlar.|Kullanıcının erişim haklarını ve izinlerini kontrol eder.|
|**İşlem Sırası**|Her zaman **ilk** adımdır.|Her zaman kimlik doğrulamadan **sonra** gerçekleşir.|
|**Ne İle Yapılır?**|Parolalar, biyometrik veriler, SMS kodları vb.|Roller (Admin, User), İzin Listeleri (ACL) vb.|

## Kimlik Doğrulama Zafiyetleri Nasıl Ortaya Çıkar?

Kimlik doğrulama mekanizmalarındaki güvenlik açıkları (zafiyetler), genellikle iki temel senaryoda ortaya çıkar:

-   **Zayıf Koruma Mekanizmaları (Kaba Kuvvet / Brute-Force Eğilimi):** Sistemin, deneme-yanılma saldırılarına karşı yetersiz kalmasıdır. Hız sınırlaması (rate limiting) veya çoklu hatalı girişte hesabı kilitleme gibi önlemlerin olmaması, saldırganların doğru parolayı bulana kadar sürekli deneme yapmasına olanak tanır.
    
-    **Mantıksal Hatalar ve Kötü Kodlama (Atlatma / Bypass):** Uygulamanın arka planındaki kodlama kusurları, saldırganın kimlik doğrulama sürecini tamamen atlatmasına izin verir. Bilgi güvenliğinde bu durum genellikle **"Bozuk Kimlik Doğrulama" (Broken Authentication)** olarak adlandırılır.
    

>  **Neden Çok Kritik?** Web geliştirme süreçlerinin herhangi bir aşamasında yapılan mantık hataları, sitenin sadece beklenmedik veya tuhaf davranmasına neden olabilir; bu her zaman doğrudan bir güvenlik riski yaratmaz. Ancak, **kimlik doğrulama** sistemin en önemli savunma hattı olduğundan, buradaki hatalı bir mantık veya kötü bir kodlama web sitesini çok ciddi güvenlik ihlallerine maruz bırakır.

Aşağıdaki alanlarda en sık karşılaşılan güvenlik açıklarından bazıları:
-   [Parola tabanlı girişlerdeki güvenlik açıkları](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/Authentication%20types/Parola%20tabanl%C4%B1%20giri%C5%9Flerdeki%20g%C3%BCvenlik%20a%C3%A7%C4%B1klar%C4%B1.md) 
-   [Çok faktörlü kimlik doğrulamada güvenlik açıkları]() 
-   [Diğer kimlik doğrulama mekanizmalarındaki güvenlik açıkları]() 

## Kusurlu Kaba Kuvvet (Brute-Force) Korumaları

Kaba kuvvet saldırıları, doğası gereği başarıya ulaşmadan önce binlerce, hatta milyonlarca "başarısız" deneme yapılmasını gerektirir. Bu nedenle savunma mekanizmaları, süreci otomatikleştirmeyi zorlaştırmak ve saldırganın deneme hızını yavaşlatmak (veya tamamen durdurmak) üzerine kuruludur.

Bu saldırıları önlemek için kullanılan en yaygın iki yöntem şunlardır:

1.   **Hesap Kilitleme (Account Lockout):** Belirli bir hesaba art arda çok sayıda başarısız giriş yapıldığında, o hesabın geçici olarak (örneğin 15 dakikalığına) kilitlenmesi.
    
2.   **IP Engelleme (IP Blocking / Rate Limiting):** Aynı IP adresinden kısa süre içinde çok sayıda başarısız giriş denemesi gelirse, sunucunun o IP adresinden gelen istekleri engellemesi (banlaması).
    

Her iki yaklaşım da belirli bir seviyede koruma sağlar; ancak arka plandaki yazılım mantığı kusurluysa (flawed logic) bu önlemler kolayca atlatılabilir.

### Atlatma Senaryosu: IP Engelleme Sayacının Sıfırlanması Zafiyeti

Uygulamalarda sıkça karşılaşılan büyük bir mantık hatası şudur: Sistem, IP engelleme sayacını _"Aynı IP'den 5 başarısız deneme gelirse IP'yi engelle"_ şeklinde kurar. Ancak normal kullanıcıların yanlışlıkla IP'lerini banlatmasını engellemek için kodun içine şu kuralı ekler: _"Eğer o IP adresinden **başarılı bir giriş** yapılırsa, hata sayacını sıfırla."_

Saldırganlar bu iyi niyetli mantık hatasını çok basit bir yöntemle sömürür: Sistemde **kendilerine ait, şifresini bildikleri geçerli bir hesap** (`saldirgan_hesap`) açarlar. Ardından, otomatik saldırı araçlarındaki kelime listesinin (wordlist) arasına kendi doğru giriş bilgilerini serpiştirirler.

**Adım Adım Atlatma (Bypass) Akışı:**

Hedef hesabın (`carlos123`) parolasını bulmaya çalışan bir saldırganın istek sırası şöyle görünür:

-   **Deneme 1:** Hedef `carlos123` - Hatalı Parola ❌ _(IP Hata Sayacı: 1)_
    
-   **Deneme 2:** Hedef `carlos123` - Hatalı Parola ❌ _(IP Hata Sayacı: 2)_
    
-   **Deneme 3:** Hedef `carlos123` - Hatalı Parola ❌ _(IP Hata Sayacı: 3)_
    
-   **Deneme 4:** Hedef `carlos123` - Hatalı Parola ❌ _(IP Hata Sayacı: 4)_ ⚠️ _IP Engellenmeye çok yakın!_
    
-   **Deneme 5:** **Saldırganın Kendi Hesabı (`saldirgan_hesap`) - Doğru Parola** ✅ _(BAŞARILI GİRİŞ! IP Hata Sayacı sıfırlanır: 0)_
    
-   **Deneme 6:** Hedef `carlos123` - Hatalı Parola ❌ _(IP Hata Sayacı: 1)_
    
-   **Deneme 7:** Hedef `carlos123` - Hatalı Parola ❌ _(IP Hata Sayacı: 2)_
    

Saldırgan, kullandığı listede her 4 hatalı denemeden sonra kendi hesabına başarılı bir giriş yaparak sayacı sürekli sıfırlar. Bu basit numara sayesinde IP adresi hiçbir zaman engelleme sınırına ulaşmaz ve kaba kuvvet savunması tamamen işlevsiz hale gelir.
 

> [Bozuk kaba kuvvet koruması, IP engelleme lab](lab)





