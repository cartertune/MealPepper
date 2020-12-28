from logic.models.food_item import FoodItem
from logic.utils import bad_data_list
import heapq


class FoodsByHeuristic:

    def __init__(self, constraint_filters, size):
        self.constraints = constraint_filters["constraints"]
        self.filters = constraint_filters["filters"]
        self.size = size


    # ((SUM of Min Constraint Percentage met) - (SUM of Max Constraint Percentage met)) / pricePerServing
    def calculate_heuristic(self, food):
        perc_points = 0
        for c in self.constraints:
             name = c["name"]  # the nutrient constrained by constraint
             nutrient = food.nutritionMap.__getitem__(name)

             # value per serving for given food and nutrient
             food_val = nutrient.perServing if not nutrient == None else 0
             if "min_val" in c:
                perc_points += (food_val / c["min_val"])
             if "max_val" in c:
                perc_points -= (food_val / c["max_val"])

        return perc_points / food.pricePerServing





    def get_foods(self):
        filters = self.filters
        if len(filters) > 0:
            food_objects = FoodItem.objects(pricePerServing__lt=20, diets__all=filters, slug__nin=bad_data_list)
        else:
            food_objects = FoodItem.objects(pricePerServing__lt=20, slug__nin=bad_data_list)

        print(len(food_objects))
        print("calculating heuristics")
        return heapq.nlargest(self.size, food_objects, self.calculate_heuristic)


