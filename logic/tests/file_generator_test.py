from logic.meal_plan_generator import MealPlanGenerator

# test 1
constraintFilters1 = {
    "filters": ["paleo-friendly"],
    "constraints": [{
        "name": "calories",
        "min_val": 2500,
        "max_val": 2800
    }, {
        "name": "protein",
        "min_val": 150
    }, {
        "name": "carbohydrates",
        "max_val": 30
    }]}

def test1():
    MealPlanGenerator().generate(constraintFilters1)

def main():
    test1()

main()
