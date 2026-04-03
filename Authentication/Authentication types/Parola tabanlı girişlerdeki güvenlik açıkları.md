# Parola tabanlı girişlerdeki güvenlik açıkları
## Parola Tabanlı Kimlik Doğrulama Zafiyetleri

Parola tabanlı giriş sürecini kullanan web sitelerinde, kullanıcılar ya kendileri bir hesap oluşturur ya da bir yönetici (administrator) tarafından kendilerine bir hesap atanır. Bu hesap, kullanıcının kimliğini doğrulamak için giriş formuna girdiği **benzersiz bir kullanıcı adı** ve **gizli bir paroladan** oluşur.

### Temel Risk: Parolanın Tek Kanıt Olması

Bu yapıda sistem, gizli parolayı bilmeyi kullanıcının _gerçek kimliğinin yeterli bir kanıtı_ olarak kabul eder.

İşte asıl tehlike burada başlar: Eğer bir saldırgan, başka bir kullanıcıya ait giriş bilgilerini (credentials) bir şekilde **elde etmeyi** veya **tahmin etmeyi** başarırsa, web sitesinin güvenliği tamamen aşılmış (compromised) olur.

### İnceleyeceğimiz Saldırı Yüzeyleri

Saldırganlar bu giriş bilgilerini ele geçirmek için çeşitli yollara başvurabilirler. Reponun ilerleyen bölümlerinde şu konuları derinlemesine inceleyeceğiz:

-   **Kaba Kuvvet (Brute-Force) Saldırıları:** Saldırganların parola tahmin süreçlerini nasıl otomatize ettikleri.
    
-   🛡️ **Brute-Force Korumalarındaki Kusurlar:** Alınan güvenlik önlemlerinin neden ve nasıl yetersiz kalabileceği veya atlatılabileceği.
    
-   **HTTP Temel Kimlik Doğrulama (Basic Auth) Zafiyetleri:** Eski bir standart olan HTTP Basic Authentication mekanizmasının barındırdığı güvenlik açıkları.
## Kaba Kuvvet (Brute-Force) Saldırıları

**Kaba kuvvet saldırısı**, bir saldırganın geçerli kullanıcı giriş bilgilerini (credentials) tahmin etmek için sistemli bir **deneme-yanılma** yöntemi kullanmasıdır.

Bu saldırıların temel özellikleri ve çalışma mantığı şu şekildedir:

-   **Otomasyon ve Kelime Listeleri (Wordlists):** Bu saldırılar genellikle potansiyel kullanıcı adları ve sık kullanılan parolalardan oluşan geniş kelime listeleri kullanılarak otomatikleştirilir. Sürecin özel yazılım ve araçlar aracılığıyla otomatikleştirilmesi, saldırganın çok yüksek hızlarda ve devasa sayılarda giriş denemesi yapmasına olanak tanır.
    
-   **Akıllı ve İsabetli Tahminler (Educated Guesses):** Brute-force saldırıları her zaman klavyede tamamen rastgele tuşlara basmak veya rastgele tahminler yapmak anlamına gelmez. Saldırganlar; temel mantığı, hedef uygulamanın yapısını veya herkese açık bilgileri kullanarak kaba kuvvet saldırılarını çok daha **isabetli tahminler** yapacak şekilde optimize edebilirler (fine-tuning). Bu yaklaşım, saldırıların başarı oranını ve verimliliğini ciddi şekilde artırır.
    

> ⚠️ **Kritik Zayıflık** Kullanıcıların kimliğini doğrulamak için **tek yöntem** olarak parola tabanlı girişe dayanan (örneğin iki adımlı doğrulama / 2FA kullanmayan) web siteleri, sistemlerinde yeterli kaba kuvvet koruma mekanizmalarını uygulamadıkları takdirde bu saldırılara karşı son derece savunmasız kalırlar.

## Kullanıcı Adlarını Tespit Etmek (Username Brute-Forcing & Enumeration)

Bir sisteme kaba kuvvet saldırısı yaparken, geçerli bir kullanıcı adını bilmek saldırının yarısını başarmak demektir. Kullanıcı adları genellikle belirli kalıplara uydukları veya sistemler tarafından dışarı sızdırıldıkları için tahmin edilmeleri sandığınızdan çok daha kolaydır.

### 1. Tahmin Edilebilir Kalıplar ve Standart İsimler

-   **E-posta Formatları (Kurumsal Kalıplar):** Çoğu kurumsal sistem, kullanıcı adı olarak çalışanların e-posta adreslerini kullanır. Bu adresler genellikle standart, şirket çapında bir formata sahiptir.
    
    -   _Örnek Kalıp:_ `isim.soyisim@sirket.com`
        
    -   _Örnek Tahmin:_ Şirkette "Ahmet Yılmaz" adında birinin çalıştığını LinkedIn'den öğrenen bir saldırgan, kullanıcı adının `ahmet.yilmaz@sirket.com` veya `ayilmaz@sirket.com` olduğunu kolayca tahmin edebilir.
        
-   **Varsayılan (Default) ve Yüksek Yetkili Hesaplar:** Belirli bir isim-soyisim kalıbı olmasa bile, yetkili hesaplar kurulum aşamasında genellikle çok tahmin edilebilir isimlerle açılır.
    
    -   _Sık Karşılaşılan Örnekler:_ `admin`, `administrator`, `root`, `sysadmin`, `test`, `moderator`.
        

### 2. Güvenlik Testlerinde Bilgi Toplama (Sızıntıları Bulmak)

Güvenlik testleri (auditing) sırasında, web sitesinin pasif olarak kullanıcı adlarını sızdırıp sızdırmadığı kontrol edilmelidir. İşte saldırganların kullanıcı adlarını toplamak (enumeration) için baktıkları yerler:

-   **Açık Kullanıcı Profilleri ve URL Yapıları:** Sisteme giriş yapmadan (login olmadan) diğer kullanıcıların profillerine erişim var mı? Profildeki özel bilgiler gizlenmiş olsa bile, profilin adresi (URL) kullanıcı adını ele verebilir.
    
    -   _Örnek:_ Tarayıcıda `https://ornekhedef.com/profil/carlos123` adresine gidildiğinde boş bir profil sayfası bile açılıyorsa (404 hatası vermiyorsa), `carlos123` sistemde kayıtlı geçerli bir kullanıcı adıdır!
        
-   **HTTP Yanıtları, Kaynak Kodlar ve Hata Mesajları:** Bazen sunucunun döndürdüğü HTTP yanıtları, e-posta adreslerini veya sistem kullanıcılarını kazara açığa çıkarır. Özellikle yönetici veya IT destek ekiplerine ait yüksek yetkili hesaplar bu yolla sızabilir.
    
    -   _Örnek (HTML Yorum Satırı Sızıntısı):_ Geliştirici kaynak kodda şöyle bir not bırakmış olabilir: `backend_admin`
        
    -   _Örnek (Hata Mesajı Sızıntısı):_ Sayfa çöktüğünde ekrana yansıyan hata mesajında `Database connection failed for user: db_admin` yazması.
## Parolalara Yönelik Kaba Kuvvet (Brute-Force) ve İnsan Faktörü

Kullanıcı adlarının aksine, parolaların kaba kuvvet saldırısıyla kırılıp kırılamayacağı tamamen **parolanın gücüne (karmaşıklığına)** bağlıdır. Birçok web sitesi, parolaların teorik olarak kaba kuvvetle kırılmasını zorlaştırmak (yüksek entropi sağlamak) için katı **parola politikaları** uygular.

Standart bir parola politikası genellikle şunları zorunlu kılar:

-   Minimum karakter uzunluğu (örn. en az 8 karakter)
    
-   Büyük ve küçük harflerin bir arada kullanımı
    
-   En az bir rakam ve özel karakter (`!`, `?`, `@`, `$`)
    

### Zafiyetin Kaynağı: İnsan Psikolojisi ve "Kurallara Uydurma"

Teoride, `qT8$vP2!` gibi tamamen rastgele oluşturulmuş yüksek entropili bir parolanın bilgisayarlar tarafından tahmin edilmesi çok zordur. Ancak işin içine **insan davranışı** girdiğinde bu sistem çöker.

İnsanlar rastgele karakterleri ezberlemekte zorlanırlar. Bu yüzden güçlü ve yeni bir parola oluşturmak yerine, akıllarında tuttukları basit bir kelimeyi alıp **parola politikasının kurallarına zorla uydurmaya (crowbar) çalışırlar.**

Saldırganlar bu insan davranışını çok iyi bilir ve saldırılarını bu yönde optimize ederler.

-   **Örnek 1: Temel Kelimeyi Kurallara Uydurma**
    
    -   _Kullanıcının aklındaki:_ `galatasaray` (Sistem bunu çok zayıf bulup reddeder)
        
    -   _Kullanıcının sisteme beğendirdiği (ve saldırganın ilk deneyeceği):_ `Galatasaray1!` veya `Galatasaray1905.`
        
-   **Örnek 2: Harf Değiştirme (Leetspeak / Substitution)**
    
    -   Kullanıcılar bazı harfleri görsel olarak benzeyen rakam veya sembollerle değiştirir.
        
    -   _Zayıf:_ `password`
        
    -   _Kurallara Uydurulmuş:_ `P4ssw0rd!` veya `P@ssw0rd123`
        

### Düzenli Şifre Değiştirme Zorunluluğunun Oluşturduğu Tehlike

Bazı kurumlar ve sistemler, güvenlik amacıyla kullanıcıları "Her 90 günde bir şifrenizi değiştirin" şeklinde zorlar. Kullanıcılar yine yeni bir şifre ezberlemekle uğraşmak istemezler ve mevcut şifrelerinin üzerinde **tahmin edilebilir, ardışık küçük değişiklikler** yaparlar.

-   **Örnek (Ardışık Artış):**
    
    -   1.  Çeyrek: `Sirketim1!`
            
    -   2.  Çeyrek: `Sirketim2!`
            
    -   3.  Çeyrek: `Sirketim3!` veya `Sirketim3?`
            
-   **Örnek (Mevsime/Yıla Göre Değişim):**
    
    -   Sonbaharda atanan şifre: `Autumn2025!`
        
    -   Kışın güncellenen şifre: `Winter2025!` veya `Winter2026!`
        

### Akıllı Kaba Kuvvet (Smart Brute-Forcing)

Kullanıcıların bu kadar tahmin edilebilir davrandığını bilen saldırganlar, `aaaaa`, `aaaab` gibi sırayla tüm harf kombinasyonlarını denemekle zaman kaybetmezler.

Bunun yerine, bilinen kelime listelerini (wordlists) alır ve onlara **mutasyon kuralları** uygularlar. Yani yazılımlarına "Listemdeki kelimelerin ilk harfini büyük yap, sonuna 1'den 100'e kadar sayı koy ve ! ekle" talimatını verirler. Bu durum, kaba kuvvet saldırılarını basit bir tahmin oyunu olmaktan çıkarıp, **çok daha sofistike, hızlı ve etkili** bir silaha dönüştürür.
## Kullanıcı Adı Tespiti (Username Enumeration) Nedir?

**Kullanıcı Adı Tespiti (Enumeration)**, bir saldırganın web sitesinin verdiği tepkilerdeki (davranışlarındaki) ufak değişiklikleri gözlemleyerek, denediği bir kullanıcı adının sistemde **gerçekten kayıtlı olup olmadığını** anlama sürecidir.

Kaba kuvvet (brute-force) saldırılarında rastgele milyonlarca kullanıcı adı denemek yerine, saldırganlar önce bu zafiyeti kullanarak geçerli kullanıcı adlarından oluşan kısa bir liste (shortlist) çıkarırlar. Sadece doğru isimlere odaklanmak, saldırının süresini günlerden dakikalara indirebilir.

### Tespit Nerelerde Yapılır?

Genellikle iki ana noktada tespit yapılır:

1.  **Kayıt Formları (Registration):** Saldırgan bir kullanıcı adını veya e-postayı kayıt formuna yazar. Sistem _"Bu e-posta adresi zaten kullanımda"_ hatası verirse, saldırgan o e-postanın sistemde kayıtlı geçerli bir kullanıcı olduğunu onaylamış olur.
    
2.  **Giriş Sayfaları (Login):** Geçerli bir kullanıcı adı ancak yanlış bir parola girildiğinde sistemin verdiği tepkiler incelenir.
    

### Kaba Kuvvet Sırasında Nelere Dikkat Edilir? (3 Temel İpucu)

Bir giriş sayfasına kaba kuvvet saldırısı yaparken (veya güvenlik testi gerçekleştirirken), sistemin geçerli ve geçersiz kullanıcı adlarına verdiği tepkiler arasındaki şu **3 temel farka** odaklanılır:

#### 1. HTTP Durum Kodları (Status Codes) Farklılıkları

Otomatik bir araçla binlerce deneme yapıldığını düşünün. Denediğiniz isimlerin çoğu yanlıştır ve sistem varsayılan olarak `401 Unauthorized` (Yetkisiz) durum kodu döndürür.

-   **Zafiyet Anı:** Eğer denemelerden biri aniden farklı bir kod (örneğin `200 OK` veya `302 Found` yönlendirmesi) döndürürse, bu durum o kullanıcı adının sistemde var olduğuna dair çok güçlü bir işarettir.
    
-   _Doğru Yaklaşım:_ Sistemin, sonuç ne olursa olsun her zaman aynı durum kodunu döndürmesi gerekir.
    

#### 2. Hata Mesajlarındaki (Error Messages) Sapmalar

Geliştiricilerin en sık yaptığı hatalardan biridir. Sistem kayıtlı olmayan kullanıcıya ve kayıtlı olup yanlış şifre girene farklı tepkiler verir.

-   **Kötü Tasarım (Açık Zafiyet):** 
	-  "Böyle bir kullanıcı bulunamadı." (Saldırgan anlar: Kullanıcı adı yanlış)
    
    -   "Girdiğiniz parola hatalı." (Saldırgan anlar: **Kullanıcı adı doğru!** Artık sadece parolayı kırmaya odaklanabilir)
        
-   **İnce Hatalar (Typo Sızıntıları):** Modern sistemler her iki durumda da _"Kullanıcı adı veya parola hatalı"_ gibi genel (generic) bir mesaj verir. Ancak bazen kodlama sırasında ufak hatalar sızar. Örneğin, arka planda oluşturulan iki farklı hata mesajından birinin sonunda görünmez bir boşluk (`"Kullanıcı adı veya parola hatalı "`) veya fazladan bir nokta olabilir. Ekranda gözle görülmese bile, saldırganın kullandığı otomatik yazılımlar bayt (byte) boyutundaki bu farklılığı hemen yakalar.
    

#### 3. Yanıt Sürelerindeki (Response Times) Gecikmeler

En sinsi ve tespiti zor olan yöntemdir. Sistem her iki durumda da aynı durum kodunu ve tamamen aynı hata mesajını verse bile, **işlem süresi** kullanıcı adını ele verebilir.

-   **Nasıl Çalışır?** Birçok web sitesi, eğer kullanıcı adı veritabanında yoksa parola kontrolü yapmaz ve anında reddeder (örneğin 50 milisaniye sürer). Ancak kullanıcı adı geçerliyse, sistem veritabanından şifrelenmiş (hash'lenmiş) parolayı çeker ve gelen parolayla eşleştirmek için ağır bir matematiksel işlem (bcrypt vb.) yapar. Bu ekstra adım, yanıt süresini uzatır (örneğin 300 milisaniye sürer).
    
-   **Zafiyeti Sömürmek:** Saldırgan, bu gecikmeyi daha da belirginleştirmek için parola kısmına **kasten çok uzun (örneğin 5000 karakterlik)** bir metin girer. Eğer kullanıcı adı doğruysa, sistem bu devasa metni hash'lemeye çalışırken çok daha fazla zorlanır ve yanıt süresi saniyelere çıkar. Eğer kullanıcı adı yanlışsa, sistem parolayı hiç kontrol etmediği için yine 50 milisaniyede yanıt verir. Aradaki bu devasa süre farkı, kullanıcının gerçek olduğunu kanıtlar.

>  [Farklı yanıtlar aracılığıyla kullanıcı adı numaralandırması lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/labs/Farkl%C4%B1%20yan%C4%B1tlar%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1.md)</br>
> [İnce farklılıklar gösteren yanıtlar aracılığıyla kullanıcı adı numaralandırması lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/labs/%C4%B0nce%20farkl%C4%B1l%C4%B1klar%20g%C3%B6steren%20yan%C4%B1tlar%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1.md)
        


