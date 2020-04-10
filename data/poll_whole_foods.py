import requests
import urllib3
from mongoengine import connect

from logic.models.food_item import FoodItem

connection = connect("meal_planner_db")
urllib3.disable_warnings()


"""
    for each known category (produce, meat, cheese, etc)
        while results poll this url, on each iteration add skip by 20
            for each:
                add it to raw whole foods data db
                (later) structure the data how I wanna


"""
#TODO: add subcategories and other methods to get all foods
# right now this only has 200 items per category for a total of 2400 items, enough for now, but we will want more
CATEGORIES = ["produce",
              "dairy-eggs",
              "cheese",
              "frozen-foods",
              "beverages",
              "snacks-chips-salsas-dips",
              "pantry-essentials",
              "breads-rolls-bakery",
              "breakfast",
              "beef-poultry-pork",
              "seafood",
              "prepared-foods",
              ]
DEFAULT_STORE = "10145"

def create_url(store, skip, category):
    return f'https://products.wholefoodsmarket.com/api/search?sort=relevance&store={store}&skip={skip}&filters=%5B%7B%22ns%22%3A%22category%22%2C%22key%22%3A%22{category}%22%2C%22value%22%3A%22{category}%22%7D%5D'

def create_product_url(slug, store):
    return f'https://products.wholefoodsmarket.com/api/Product/{slug}?store={store}'

def poll_wf():
    for category in CATEGORIES:
        finished = False
        skip = 0
        while not finished:
            r = requests.get(url=create_url(DEFAULT_STORE, skip, category), verify=False)
            print("Just fetched ", category, " and skipped ", skip)
            data = r.json()
            for item in data["list"]:
                product = requests.get(url=create_product_url(item["slug"], DEFAULT_STORE), verify=False)
                p = product.json()
                price = p["store"]["basePrice"]
                diets = list(map(lambda d: d["slug"], p["diets"]))
                del p["meta"], p["store"], p["image"], p["diets"]

                food = FoodItem(_id=p["_id"], name=p["name"])
                food.update(**p)
                food.price = price
                food.diets = diets
                food.save()

            # TODO for each item, fetch the full version and add it to the DB
            if not data["hasLoadMore"]:
                finished = True
            skip += 20



def main():
    poll_wf()
    print("Completed!")

main()