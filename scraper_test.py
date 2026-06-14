import requests

url = "https://gw.yad2.co.il/yad1/projects?limit=20&package=PREMIUM_LISTING,PRO_LISTING"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print(response.text[:1000])   # on affiche juste le début
