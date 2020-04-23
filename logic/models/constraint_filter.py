class ConstraintsFilters:
    def __init__(self, constraints, diet_filters):
        self.constraints = constraints  # an array of Constraints
        self.diet_filters = diet_filters  # [String] that should be filtered (listed in Diets enum on food_item.py)


class Constraint:
    def __init__(self, name, min_val, max_val):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val



"""
What Front-end should send:

body: {
    constraintsFilters: {
        constraints: [{ name: "calories", min_val: 2000, max_val: 2400}, { name: "protein", min: 80 }],
        filters: ["vegan", "paleo-friendly"]
    }
}
"""