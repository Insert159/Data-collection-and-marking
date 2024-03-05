import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint

def set_key():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.spoonenv') 
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

set_key()

url = "https://api.spoonacular.com/recipes/complexSearch"

headers = {
    "accept": "application/json",
    "Authorization": os.getenv("SPOON_KEY")
}

params = {
    "query": "pasta",
    "apiKey": os.getenv("SPOON_KEY")
}
#print(params)
response = requests.get(url, params=params, headers=headers)
print(response.status_code)

if response.status_code == 200:
    jdata = response.json()
    pprint(jdata)
    for res in jdata['results']:
        id = res['id']
        print(f"ИД: {id}\t Название: {res['title']}")
        url = f"https://api.spoonacular.com/recipes/{id}/information"
        params = {
            "id": res['id'],
            "apiKey": os.getenv("SPOON_KEY")
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            recipe_data = response.json()
            print("Рецепт: ")
            print(recipe_data['instructions'])
        print('\n\n')
