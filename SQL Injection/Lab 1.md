Bu lab ürün kategorisi filtresinde bir SQLi açığı içermektedir. Uygulama aşağıdaki gibi bir SQL sorgusu gerçeklerştirir.
    SELECT * FROM products WHERE category = 'Gifts' AND released = 1

Laboratuvarı çözmek için, uygulamanın bir veya daha fazla yayınlanmamış ürünü görüntülemesine neden olan bir SQL enjeksiyon saldırısı gerçekleştirilmeli.

Lab bizi aşağıdaki gibi bir site ile karşılıyor.
![Lab1 ilk bakış]([lab1%20ilk%20bak%C4%B1%C5%9F]([https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab1%20ilk%20bak%C4%B1%C5%9F.png](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/images/Lab1%20ilk%20bak%C4%B1%C5%9F.png?raw=true)))
Sitenin kategorilerinde gezindiğimizde url şu şekilde oluyor.
![Lab1 url gözlem](Lab1%20url%20g%C3%B6zlem)
Kırmızı karenin içerisindeki alan sorguya gönderilen kısımdır. Bu sorgunun SQL karşılığı şudur:

    SELECT * FROM products WHERE category = 'Corporate gifts' AND released = 1

Şimdiki adım bir SQLi açığı olup doğrulamasının yapılması. Bu da sorgunun sonuna `'` koyarak SQL sorgusunu bozmaya çalışılır.
![Lab1 sqli kontrol](Lab1%20sqli%20kontrol)
Yukarıda göründüğü gibi sorgunun sonuna `'` konulduğunda sayfa eror vermekte bu da sayfada bir sqli açığı olduğu anlamına gelmektedir.(url deki sorguda %27 `'` işaretinin url encode edilmiş halidir.)

Şimdiki adım olarak piyasaya sürülmemiş ürünleri görüntüleyebilmek için sorguyu manüpile etmekte yani `released = 0` olan ürünleri de görüntüler. Bunu da `AND released = 1` kısmından önce yorum satırı işaretini koyarak gerçekleştirebiliriz. Yani url'nin sorgu kısmına `' --` ekleyerek gerçekleştirebiliriz	  
![Lab1 ilk çözük](Lab1%20ilk%20%C3%A7%C3%B6z%C3%BCm)
İkinci resim ile yukarıdaki resmi karşılaştırırsanız ikinci resimde 3 ürün yukarıdakinde ise 4 ürün görünmekte. Böylece piyasaya sürülmemiş ürünüde görüntülemiş olduk

Veritabanındaki tüm ürünleri kategori , piyasaya salınmışmı fark etmeksizi görüntülenebilir bunuda url'yi şu şekilde manipule ederek yapabiliriz:
`' OR 1=1--` bu şekilde veri tabanındaki tüm veriler ekrana basılacak.
![çözüm](%C3%A7%C3%B6z%C3%BCm)

Labaratuarı aşağıdaki linkten kendiniz çözebilirsiniz:
https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
 

