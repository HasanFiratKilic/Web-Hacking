## SQLi saldırılarında veritabanının incelenmesi
SQLi saldırılarında veritabanı hakkında bilgi toplamak önemlidir çünkü kullanılan sürüme veya hangi tür veritabanını kullanıldığına göre SQLi için kullanacağımız sorgularda değişmektedir. Bu bilgiler şunları içerir:
- Veritabanı türü ve sürümü.
- Veritabanın tabloları ve bu tablolardaki sütunlar.
## Veritabanı türü ve sürümünü sorgulama
Sağlayıcıya özgü sorgular ekleyerek veritabanı türünü ve sürümünü belirleyebilirsiniz; bu şekilde hangisinin çalıştığını görebilirsiniz.

Aşağıda, bazı popüler veritabanı türleri için veritabanı sürümünü belirlemeye yönelik bazı sorgular yer almaktadır:
|Veritabanı türü|Sorgu|
|--|--|
|Microsoft, MySQL| `SELECT @@version` |
|Oracle|`SELECT * FROM v$version`|
|PostgreSQL|`SELECT version()`|
For example, you could use a `UNION` attack with the following input:

    ' UNION SELECT @@version--
> [Oracle'da veritabanı türü ve sürümünü sorgulayan SQL enjeksiyon saldırısı.](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Lab5.md)

> [SQLi saldırısı, MySQL ve Microsoft veritabanlarında veritabanı türü ve sürümünü bulma lab.](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Lab6.md)
