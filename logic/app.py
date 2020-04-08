from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from logic.meal_plan_generator import MealPlanGenerator
import logic.db_connection

app = Flask(__name__)
CORS(app)

planner = MealPlanGenerator()


@app.route("/")
def main():
    return jsonify({"data": planner.generate()})


if __name__ == '__main__':
    app.run(debug=True)
