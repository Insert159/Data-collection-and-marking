import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint

def set_key():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

set_key()
#print(os.getenv("API_KEY"))
print("Выберите категорию:")
print("1. кофейни")
print("2. музеи")
print("3. парки")
cathegory = int(input("категория: "))
#print(cathegory)
if cathegory == 1:
    cathegory_id = 13032 # кафе
elif cathegory == 2:
    cathegory_id = 10027 # музей
elif cathegory == 3:
    cathegory_id = 16032 # парк
else:
    print("Неизвестная категория")

url = "https://api.foursquare.com/v3/places/search"

headers = {
    "accept": "application/json",
    "Authorization": os.getenv("API_KEY")
}

params = {"categories": f"{cathegory_id}",
          "fields": "name,location,rating"
}
#print(params)
response = requests.get(url, params=params, headers=headers)
print(response.status_code)

if response.status_code == 200:
    jdata = response.json()
    #pprint(jdata)
    for place in jdata['results']:
        print('------------------------------------------------')
        #pprint(place)
        name = place['name']
        print('НАЗВАНИЕ: ', name)
        location = place['location']
        address = location['formatted_address']
        print('АДРЕС: ', address)
        rating = place['rating']
        print('РЕЙТИНГ: ', rating)

