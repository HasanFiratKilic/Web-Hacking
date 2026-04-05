# Hesap kilidi aracılığıyla kullanıcı adı numaralandırması
Bu laboratuvar, kullanıcı adı numaralandırmasına karşı savunmasızdır. Hesap kilitleme kullanır, ancak bu mantıksal bir hata içerir.

Çözüm için:
- Geçerli bir kullanıcı adını belirle.
- Bulunan kullanıcının şifresini brute force ile kır.

Lab açılışı:
![Hesap kilidi aracılığıyla kullanıcı adı numaralandırması ilk](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Hesap%20kilidi%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20ilk.png?raw=true)

Lab açıklamasında hesap kilitleme ile brute force engellemesi yapıldığı yazmakta ilk olark kayıtlı olma ihtimali olmayan bir kullanıcı adı ile peş peşe yanlış denemeler yaptım ama sadece `Invalid username or password.` uyasını vermekte bu da kitleme işlemini sadece kayıtlı kullanıcının şifresi ard arda yanlış girilirse gerçekleşmekte. Bu işlemi otomatik hale getirecek bir [kod](kod) ile çözülebilir. Bu kod verilen listedeki kullanıcı adlarını tek tek birden fazla deneme yapacak ve gelen yanıtta `Invalid username or password.` mesajı dışında bir mesaj var ise bu kullanıcının kayıtlı olduğunu bulmuş olucak.
![Hesap kilidi aracılığıyla kullanıcı adı numaralandırması uname](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Hesap%20kilidi%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20uname.png?raw=true)

Aynı kodu kullanarak bulunan kullanıcı şifresini brute force ile kırılabilir. Kod verilen parola listesini tek tek dener eğer yanıtta `Invalid username or password.` dışında bir hata var ise 30 saniye bekler sonrasında parola denemeye devam eder. Yanıtta 302 yönlendirme kodunu gördüğünde denemiş olduğu parolayı ekrana yazar.
![Hesap kilidi aracılığıyla kullanıcı adı numaralandırması pass](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Hesap%20kilidi%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20pass.png?raw=true)

Bulunan bilgilerle giriş işlemi yapılarak lab çözülür.
![Hesap kilidi aracılığıyla kullanıcı adı numaralandırması çözüm](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/Authentication/images/Hesap%20kilidi%20arac%C4%B1l%C4%B1%C4%9F%C4%B1yla%20kullan%C4%B1c%C4%B1%20ad%C4%B1%20numaraland%C4%B1rmas%C4%B1%20%C3%A7%C3%B6z%C3%BCm.png?raw=true)

Lab link:</br>
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock
