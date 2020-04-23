from flask import Flask, jsonify
from flask_cors import CORS
import json
from mongoengine import connect
connect("meal_planner_db")

from logic.meal_plan_generator import MealPlanGenerator

app = Flask(__name__)
CORS(app)

planner = MealPlanGenerator()


@app.route("/")
def main(input_data):
    data = jsonify({"data": planner.generate(json.loads(input_data))})
    return data


if __name__ == '__main__':
    app.run(debug=True)
