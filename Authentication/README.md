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






