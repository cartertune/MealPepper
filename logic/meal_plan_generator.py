from logic.db_connection import mongo_connection
from logic.models.food_item import FoodItem
import random
from pulp import *

class MealPlanGenerator:

    days_of_week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    food_items = mongo_connection.get_collection("food_item")

    def get_random_food_items(self, n):
        random_ints = []

        #TODO solve for food items with out serving costs (aka make up serving??)
        food_objects = FoodItem.objects(noServingCount__ne=True)
        for i in range(n):
            random_ints.append(random.randint(1, food_objects.count() - 1))

        return list(map(lambda r: food_objects[r], random_ints))

    def generate_random_meal_plan(self):
        meal_plan = {}
        for dow in self.days_of_week:
            meal_plan[dow] = {}
            meal_plan[dow]["food"] = list(map(lambda r: r.to_json(), self.get_random_food_items(12)))
        return meal_plan

    def generate_basic_IP_plan(self, constraintFilter, sample_size=20):
        food_items = self.get_random_food_items(sample_size)
        food_ids = []
        food_calories = []
        food_fat = []
        food_carbs = []
        food_protein = []
        food_prices = []

        for food in food_items:
            food_ids.append(food.name)
            food_prices.append(float(food.pricePerServing))
            food_calories.append(float(food.nutritionMap.calories.perServing))
            food_fat.append(float(food.nutritionMap.totalFat.perServing))
            food_carbs.append(float(food.nutritionMap.carbohydrates.perServing))
            food_protein.append(float(food.nutritionMap.protein.perServing))



        prob = LpProblem("Simple Diet Problem", LpMinimize)

        prices = dict(zip(food_ids, food_prices ))

        # Create a dictionary of calories for all food items
        calories = dict(zip(food_ids, food_calories))

        # Create a dictionary of total fat for all food items
        fat = dict(zip(food_ids, food_fat))

        # Create a dictionary of carbohydrates for all food items
        carbs = dict(zip(food_ids, food_carbs))

        protein = dict(zip(food_ids, food_protein))

        food_vars = LpVariable.dicts("Food", food_ids, lowBound=0, cat='Integer')
        prob += lpSum([prices[i] * food_vars[i] for i in food_ids])

        prob += lpSum([calories[f] * food_vars[f] for f in food_ids]) >= 2000.0
        prob += lpSum([calories[f] * food_vars[f] for f in food_ids]) <= 2500.0

        prob += lpSum([fat[f] * food_vars[f] for f in food_ids]) >= 20.0, "FatMinimum"
        prob += lpSum([fat[f] * food_vars[f] for f in food_ids]) <= 50.0, "FatMaximum"

        # Carbs
        prob += lpSum([carbs[f] * food_vars[f] for f in food_ids]) >= 130.0, "CarbsMinimum"
        prob += lpSum([carbs[f] * food_vars[f] for f in food_ids]) <= 200.0, "CarbsMaximum"


        # Protein
        prob += lpSum([protein[f] * food_vars[f] for f in food_ids]) >= 120.0, "ProteinMinimum"
        prob += lpSum([protein[f] * food_vars[f] for f in food_ids]) <= 150.0, "ProteinMaximum"

        prob.solve()
        print("Status:", LpStatus[prob.status])
        for v in prob.variables():
            if v.varValue > 0:
                print(v.name, "=", v.varValue)
        obj = value(prob.objective)
        print("The total cost of this balanced diet is: ${}".format(round(obj, 2)))






    def generate(self, constraintFilters={}):

        # print(FoodItem.objects(diets__all=constraintFilters["filters"].count()))
        #meal_plan = self.generate_random_meal_plan()
        meal_plan = self.generate_basic_IP_plan(constraintFilters, 1400)
        #return meal_plan

MealPlanGenerator().generate()