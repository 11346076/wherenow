import requests

url = "http://127.0.0.1:8000/api/places/"

response = requests.get(url)

if response.status_code == 200:
    places = response.json()

    print("===== WhereNow Places API =====")

    for place in places:
        print(f"地點名稱: {place['name']}")
        print(f"地區: {place['area']}")
        print(f"地址: {place['address']}")
        print(f"預算: {place['budget']}")
        print("-------------------------")

else:
    print("API 讀取失敗")