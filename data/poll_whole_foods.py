import requests
import urllib3
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
    return f'https://products.wholefoodsmarket.com/api/search?sort=relevance&store={store}&skip={skip}&filters=%5B%7B%22ns%22%3A%22category%22%2C%22key%22%3A%22{category}%22%2C%22value%22%3A%22produce%22%7D%5D'


for category in CATEGORIES:
    finished = False
    skip = 0
    while not finished:
        r = requests.get(url = create_url(DEFAULT_STORE, skip, category), verify=False)
        print("Just fetched ", category, " and skipped ", skip)
        data = r.json()
        #TODO for each item, fetch the full version and add it to the DB
        if not data["hasLoadMore"]:
            print(data)
            finished = True
        skip+=20
