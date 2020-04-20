import requests
import urllib3

from logic.models.food_item import FoodItem
from logic.utils import calculate_price_per_serving

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
CATEGORIES = {
    "produce": ["fresh-fruit", "fresh-herbs", "fresh-vegetables"],
    "dairy-eggs": ["butter-margarine", "dairy-alternatives", "eggs", "milk-cream", "yogurt"],
    "cheese": [""], # TODO make sure this works
    "frozen-foods": ["frozen-breakfast", "frozen-entr-es-appetizers",
                       "frozen-fruits-vegetables", "frozen-pizza", "ice-cream-frozen-desserts"],
    "beverages": [], # skip
    "snacks-chips-salsas-dips": ["candy-chocolate", "chips", "cookies", "crackers", "jerky",
                                   "nutrition-granola-bars", "nuts-seeds-dried-fruit",
                                   "popcorn-puffs-rice-cakes", "salsas-dips-spreads"],
    "pantry-essentials": ["baking", "canned-goods", "condiments-dressing", "jam-jellies-nut-butters",
                            "pasta-noodles", "rice-grains", "sauces", "soups-broths", "spices-seasonings"],
    "breads-rolls-bakery": ["breads", "breakfast-bakery", "desserts", "rolls-buns", "tortillas-flat-breads"],
    "breakfast": ["cereal", "hot-cereal-pancake-mixes"],
    "beef-poultry-pork": ["deli-meat", "hot-dogs-bacon-sausage", "meat-alternatives", "meat-counter",
                            "packaged-meat", "packaged-poultry", "poultry-counter"],
    "seafood": [""], #TODO make sure this works
    "prepared-foods": [""],
    }
DEFAULT_STORE = "10241"  # Green Hills, TN (:

def create_url(store, skip, category, subcategory):
    if subcategory == "":
        return f"https://products.wholefoodsmarket.com/api/search?sort=relevance&store={store}&skip={skip}&filters=%5B%7B%22ns%22%3A%22category%22%2C%22key%22%3A%22{category}%22%2C%22value%22%3A%22{category}%22%7D%5D"
    return f'https://products.wholefoodsmarket.com/api/search?sort=relevance&store={store}&skip={skip}&filters=%5B%7B%22ns%22%3A%22category%22%2C%22key%22%3A%22{category}%22%2C%22value%22%3A%22{category}%22%7D%2C%7B%22ns%22%3A%22subcategory%22%2C%22key%22%3A%22{subcategory}%22%2C%22value%22%3A%22{category}.{subcategory}%22%7D%5D'

def create_product_url(slug, store):
    return f'https://products.wholefoodsmarket.com/api/Product/{slug}?store={store}'



def poll_wf():
    for category in CATEGORIES.keys():
        for subcategory in CATEGORIES[category]:
            finished = False
            skip = 0
            print(category, subcategory)
            while not finished:
                r = requests.get(url=create_url(DEFAULT_STORE, skip, category, subcategory), verify=False)
                print("Just fetched ", category, "@ subcategory", subcategory, " and skipped ", skip)
                data = r.json()
                for item in data["list"]:
                    product = requests.get(url=create_product_url(item["slug"], DEFAULT_STORE), verify=False)
                    p = product.json()
                    price = p["store"]["basePrice"]
                    imageUrl = p["image"]["source"]
                    thumbnailUrl = p["image"]["thumbnail"]
                    diets = list(map(lambda d: d["slug"], p["diets"]))
                    del p["meta"], p["image"], p["diets"]

                    food = FoodItem(_id=p["_id"], name=p["name"], servingInfo=p["servingInfo"])
                    food.save()
                    food.update(**p)
                    food.imageUrl = imageUrl
                    food.thumbnailUrl = thumbnailUrl
                    food.price = price
                    food.diets = diets
                    food.save()

                    # calculate price
                    food.pricePerServing = calculate_price_per_serving(food)
                    food.save()

                if not data["hasLoadMore"]:
                    finished = True
                skip += 20

def update_food_items():
    for f in FoodItem.objects():
        if f.slug == "organic-spaghetti-squash-f47cbb":
            f.pricePerServing = calculate_price_per_serving(f, True)
        f.pricePerServing = calculate_price_per_serving(f)
        f.save()

def main():
    #poll_wf()

    update_food_items()
    # print(FoodItem.objects()[0:20].to_json())
        # if not (Uom == "g" or Uom == "oz" or Uom2 == "g" or Uom2 == "oz"):
        #     print(f.name)
        #     print(Uom)
        #     print(Uom2)
        #     print("-----")

    print("Completed")


main()