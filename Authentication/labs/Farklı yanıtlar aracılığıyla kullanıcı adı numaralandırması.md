# Farklı yanıtlar aracılığıyla kullanıcı adı numaralandırması
Bu laboratuvar, kullanıcı adı numaralandırma ve parola kaba kuvvet saldırılarına karşı savunmasızdır.
Çözüm için:
- Geçerli bir kullanıcı adı belirle.
- Bu kullanıcının şifresini kaba kuvvet yöntemiyle kır.
- Hesap sayfasına erişin.

Lab giriş kısmı aşağıdaki şekilde:
![Farklı yanıtlar aracılığıyla kullanıcı adı numaralandırması ilk](Farkl%C4%B1%20yan%C4%B1tlar%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20ilk)

Öncelikle kullanıcı adı: `test` parola: `test` girdileri ile denem tapıldığında sayfada `Invalid username` uyarı görünmekte bu mesaj genel bir mesaj olmadığından kayıtlı kullanıcı adı girildiğinde farklı bir hata mesajı verebileceğini çıkarırız.
![Farklı yanıtlar aracılığıyla kullanıcı adı numaralandırması kontrol](Farkl%C4%B1%20yan%C4%B1tlar%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20kontrol)

Labın açıklamasındaki kullanıcı adılarını tek tek deneyip sayfanın hata mesajlarına göre kullanıcı adı numaralandırması yapmalıyız. `ffuf -u "<url adresi>" -w <kelime listesi yolu> -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=FUZZ&password=test" -fr "Invalid username"` kullanırasak `ffuf` komutu verdiğimiz login kısmındaki url adresindeki form kısmına kelime listesindeki kullanıcı adlaını tek tek deneyecek gönen yanıtın içerisinde `Invalid username` hata mesajı varsa yükü göstermeyecek ne zaman yanıtta `Invalid username` olmazsa kullanmış olduğu kullanıcı adını ekranda gösterecek. Komutun incelenmesi:
- `ffuf` : Web uygulama fuzzing aracı. Kelime listesindeki girdileri hedef URL’e gönderir.
-  `-u "<url adresi>"` :  Buraya fuzzing yapılacak endpoint yazılır.
-  `-w <kelime listesi yolu>` : Kelime listesi dosyasının yolu. `FUZZ` anahtar kelimesi bu listedeki her satırla değiştirilir.
-  `-X POST` : HTTP metodunu belirtir.
- `-H "Content-Type: application/x-www-form-urlencoded"` : Gönderilen verinin türünü belirtir. Form verilerinin `key=value&key2=value2` formatında olduğunu söyler.
-  `-d "username=FUZZ&password=test"` :  POST gövdesinde gönderilecek veri.`FUZZ`, kelime listesindeki her bir kelime ile değişir.
-  `-fr "Invalid username"` : Cevapların içinde `"Invalid username"` yazıyorsa bu cevapları filtrele (gösterme).
Programı çalıştırdığımızda kullanıcı adı olarak `appserver` adlı bir kullanıcı adı bulmuş oldum.
![Farklı yanıtlar aracılığıyla kullanıcı adı numaralandırması username](Farkl%C4%B1%20yan%C4%B1tlar%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20username)

Şimdi bulunan kullanıcı adına labın açıklamasındaki parolalar ile brute force yaparak doğru parolayı bulmaya çalışılır. Kullanıcı adını numaralandırmak için kullanılan komut üzerinde bazı değişiklikler ile parola bulunabilir. Yapılacak değişiklikler:
- `-d "username=appserve&password=FUZZ"` : appserver kullanıcısı için tüm parolaları tek tek FUZZ kısmına terleştirilerek denenir.
- `-mc 302` : Bu dönen yanıtlardan HTTP kodu 302 olan yanıtları ekranda gösterir. Sayfa doğru kullanıcı adı ve parola verildiğinda sayfa 302 kodu ile yönlendirme yapar.
Komutu çalıştırıldığında parola olarak `qazwsx` ekranda görünmekte.
![Farklı yanıtlar aracılığıyla kullanıcı adı numaralandırması pass](Farkl%C4%B1%20yan%C4%B1tlar%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20pass)

Çözüm için bulunan kullanıcı adı ve parola girilir ve lab çözülmüş olur.
![Farklı yanıtlar aracılığıyla kullanıcı adı numaralandırması çözüm](Farkl%C4%B1%20yan%C4%B1tlar%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20%C3%A7%C3%B6z%C3%BCm)
 
 Lab link:</br>
 https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses
 	
