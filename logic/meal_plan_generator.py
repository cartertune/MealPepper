from logic.db_connection import mongo_connection
from logic.models.food_item import FoodItem
import random
from pulp import *

from logic.utils import bad_data_list


class MealPlanGenerator:

    days_of_week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    food_items = mongo_connection.get_collection("food_item")

    def get_random_food_items(self, filters=["paleo-friendly"], n=20):
        random_ints = []

        #TODO solve for food items with out serving costs (aka make up serving??)
        if len(filters) > 0:
            food_objects = FoodItem.objects(pricePerServing__lt=20, diets__all=filters, slug__nin=bad_data_list)
        else:
            food_objects = FoodItem.objects(pricePerServing__lt=20, slug__nin=bad_data_list)

        food_count = food_objects.count()
        #print(food_count, n)
        # if below some threshold, no need for random
        if food_count * .67 < n:
            print(food_count)
            return food_objects
        for i in range(n):
            random_ints.append(random.randint(0, food_objects.count() - 1))

        return list(map(lambda r: food_objects[r], random_ints))

    def print_solution(self, prob, food_map, constraints):
        print("Status:", LpStatus[prob.status])
        constraintTotals = {}
        for v in prob.variables():
            if v.varValue > 0:
                id = v.name[5:]
                f = FoodItem.objects(_id=id)[0]
                amount = v.varValue
                print("\n", f.name, "servings:", amount, "total:", round(f.pricePerServing * amount, 2))
                print(f.to_json())
                for i in range(len(constraints)):
                    c = constraints[i]
                    if not c["name"] in constraintTotals:
                        constraintTotals[c["name"]] = 0
                    adj_amount = round(food_map[id][i + 1] * amount, 2)
                    constraintTotals[c["name"]] += adj_amount
                    print(c["name"], "total:", adj_amount)
        print("Totals:")
        for ct in constraintTotals.keys():
            print(ct, constraintTotals[ct])
        obj = value(prob.objective)
        print("The total cost of this balanced diet is: ${}".format(round(obj, 2)))

    def generate_random_meal_plan(self):
        meal_plan = {}
        for dow in self.days_of_week:
            meal_plan[dow] = {}
            meal_plan[dow]["food"] = list(map(lambda r: r.to_json(), self.get_random_food_items(12)))
        return meal_plan

    def generate_basic_IP_plan(self, constraintFilter, sample_size):
        """
            For each constraint:
            1. Create a table of food id -> that field
                - For each constraint field, assign a number i
                - create a dict of id -> array where the ith element is the val for that 
            2. Add the min & max to the problem
        """
        food_items = self.get_random_food_items(constraintFilter["filters"], sample_size)
        food_map = dict()
        for food in food_items:
            if not food.id in food_map.keys():
                food_map[food.id] = []
                food_map[food.id].append(float(food.pricePerServing))

        prob = LpProblem("Simple Diet Problem", LpMinimize)
        food_vars = LpVariable.dicts("Food", food_map.keys(), lowBound=0, cat='Integer')
        prob += lpSum([food_map[i][0] * food_vars[i] for i in food_map.keys()])

        constraints = constraintFilter["constraints"]

        for i in range(len(constraints)):
            c = constraints[i]

            # build food map
            for food in food_items:

                if len(food_map[food.id]) <= i + 1:
                    nm = food.to_mongo().to_dict()["nutritionMap"]
                    if c["name"] in nm:
                        food_map[food.id].append(nm[c["name"]]["perServing"])
                    else:
                        food_map[food.id].append(0)

            if "min_val" in c:
                prob += lpSum(food_map[f][i + 1] * food_vars[f] for f in food_map.keys()) >= c["min_val"], "min_" + c["name"]
            if "max_val" in c:
                prob += lpSum(food_map[f][i + 1] * food_vars[f] for f in food_map.keys()) <= c["max_val"], "max_" + c["name"]

        prob.solve()

        self.print_solution(prob, food_map, constraints)







    def generate(self, constraintFilters):
        print(constraintFilters)

        meal_plan = self.generate_basic_IP_plan(constraintFilters, 500)
        #return meal_plan
