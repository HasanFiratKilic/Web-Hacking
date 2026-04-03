# Lab: İnce farklılıklar gösteren yanıtlar aracılığıyla kullanıcı adı numaralandırması
Bu laboratuvar, kullanıcı adı numaralandırma ve parola kaba kuvvet saldırılarına karşı gizli bir şekilde savunmasızdır.

Çözüm için:
- Geçerli bir kullanıcı adını belirle.
- Bu kullanıcının şifresini kaba kuvvet yöntemiyle bul.
- Hesap sayfasına erişin.

Sayfanın giriş sayfası aşağıdaki şekilde.
![Username enumeration via subtly different responses ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20subtly%20different%20responses%20ilk.png?raw=true)

Kullanıcı adına `test` parolaya `test` değerlerini girerek sayfanın davranışına baktığımızda `Invalid username or password.` hata mesajını vermekte bu genel bir hata mesajıdır. Yine de bu mevcut kullanıcı adı girildiğinde de aynı şekilde bir hata mesajı verdiğini göstermemekte.
![Username enumeration via subtly different responses kontrol](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20subtly%20different%20responses%20kontrol.png?raw=true)

Verilen kullanıcı adlarını tek tek deneyip hepsine aynı hata mesajını verip vermediğini kontrol etmeliyiz. Bunu için ffuf programını kullanarak yapabiliriz. `ffuf -u "<hedef uç nokta url>" -w username.txt -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=FUZZ&password=12345" -fr "Invalid username or password\."` komutunu kullanılırda username.txt içerisindeki kullanıcı adlarını tek tek dener ve dönen yanıtın içerisinde `Invalid username or password.`  varsa ekranda görüntülemez ne zaman farklı bir yanıt gelirse o zaman ekranda kullanılan username görünür. `"Invalid username or password\."` burada `\` karakteri, regex’te özel anlamı olan nokta (.) karakterini sıradan bir nokta haline getirir, böylece `-fr` seçeneği tam olarak `"Invalid username or password."` cümlesini filtreler. Kodu uyguladığımızda `af` yükünün farklı bir mesaj aldığını göstermekte bu uygulamada `af` adlı bir kullanıcı olduğunu destekler.
![Username enumeration via subtly different responses username](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20subtly%20different%20responses%20username.png?raw=true)

Bulunan kullanıcı adını manuel olarak girdiğimizde sayfa bize `Invalid username or password` burada normalde olması gereken nokta(.) işateri yoktur.
![Username enumeration via subtly different responses udeneme](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20subtly%20different%20responses%20udeneme.png?raw=true)

Bulunan kullanıcı adını kullanarak labın vermiş olduğu parola listesi tek tek denenerek `af` kullanıcısını parolası bulunmaya çalışılır.  `ffuf -u "<hedef uç nokta url>" -w password.txt -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=af&password=FUZZ" -mc 302` konutunu çalıştırdığımızda doğru şifre girildiğinde ekrana girmiş olduğu şifreyi yazar çönkü sayfaya doğru kullanıcı adı ve parola verildeğinde 302 HTTP kodunu dönmekte. `-mc 302` kısmı sadece 302 kodunu dönen isteği ekrana yazdımakta. Parola `freedom` olarak bulunmuş olur.
![Username enumeration via subtly different responses pass](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20subtly%20different%20responses%20pass.png?raw=true)

Son olarak bulunan kullanıcı adı ve parola girilerek lab çözülümüş olur.

![Username enumeration via subtly different responses çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Username%20enumeration%20via%20subtly%20different%20responses%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Lab link:</br>
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses

