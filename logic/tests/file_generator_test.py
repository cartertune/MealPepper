from logic.meal_plan_generator import MealPlanGenerator

# test 1
constraintFilters1 = {
    "filters": ["paleo-friendly"],
    "constraints": [{
        "name": "calories",
        "min_val": 3000,
        "max_val": 3100
    }, {
        "name": "protein",
        "min_val": 200
    }, {
        "name": "carbohydrates",
        "max_val": 80
    }, {
        "name": "vitaminD",
        "min_val": 20
    }, {
        "name": "vitaminA",
        "min_val": 1000
    }, {
        "name": "vitaminE",
        "min_val": 15
    }, {
        "name": "vitaminK",
        "min_val": 120
    }, {
        "name": "vitaminC",
        "min_val": 90
    }, {
        "name": "thiamin",
        "min_val": 1.2
    }, {
        "name": "selenium",
        "min_val": 55
    }, {
        "name": "riboflavin",
        "min_val": 1.3
    }, {
        "name": "niacin",
        "min_val": 16
    }, {
        "name": "vitaminB6",
        "min_val": 2
    }, {
        "name": "vitaminB12",
        "min_val": 6
    }, {
        "name": "iron",
        "min_val": 18
    }, {
        "name": "magnesium",
        "min_val": 420
    }]}


def test1():
    MealPlanGenerator().generate(constraintFilters1)


def main():
    test1()

main()
