# Bozuk kaba kuvvet koruması, IP engelleme
Bu laboratuvar, parola kaba kuvvet saldırısı korumasındaki mantıksal bir hata nedeniyle güvenlik açığına sahiptir.

Çözüm için:
- `carlos` kullanıcısını parolasını brute force ile kır.
- `carlos` kullanıcısı ile giriş yar.

Lab açılışı:
![Broken brute-force protection, IP block ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Broken%20brute-force%20protection,%20IP%20block%20ilk.png?raw=true)

Giriş işleme 3 yanlık deneme sonrsı 1 dakika giriş işlemini kitlemekte ama 2 deneme sonrasında 1 doğru giriş işlemi gerçekleşirse deneme hakkı sıfırlanır. Bu işlemler dikkata alınarak bu işlemleri otomatik gerçekleştirecek [program](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/cods/ip_block_bf.py) yazılarak gerçekleştirilebilir. Bu kod her 2 denemeden sonra 1 başarılı giriş ilemi yaparak denemeyi sıfırlar ve doğru parola girildiğinde web uygulaması 302 kodu döndüğünde program girmiş olduğu parolayı ekranda yazar.
![Broken brute-force protection, IP block pass](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Broken%20brute-force%20protection,%20IP%20block%20pass.png?raw=true)

Son olarak bulunan parole ile giriş işlemi gerçekleştirilir.
![Broken brute-force protection, IP block cozum](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Broken%20brute-force%20protection,%20IP%20block%20cozum.png?raw=true)

Lab link:</br>
https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block
