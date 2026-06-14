import requests
import json

url = "https://gw.yad2.co.il/recommendations/items/realestate?type=home&count=20&categoryId=2&roomValues=2,2.5&propertyValues=1&cityValues=3000&subCategoriesIds=2"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.yad2.co.il/realestate/rent/jerusalem-area?maxPrice=4000&minRooms=2&maxRooms=2.5&property=1&area=7&city=3000"
}

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print(response.text[:5000])
