from logic.db_connection import mongo_connection
from logic.models.food_item import FoodItem
import random

class MealPlanGenerator:

    days_of_week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    food_items = mongo_connection.get_collection("food_item")

    def generate_random_meal_plan(self):
        meal_plan = {}
        for dow in self.days_of_week:
            random_ints = []
            for i in range(12):
                random_ints.append(random.randint(1, 2000))

            meal_plan[dow] = {}
            meal_plan[dow]["food"] = list(map(lambda r: FoodItem.objects()[r].to_json(), random_ints))
        return meal_plan

    def generate(self, constraintFilters):

        # print(FoodItem.objects(diets__all=constraintFilters["filters"].count()))
        meal_plan = self.generate_random_meal_plan()
        return meal_plan
