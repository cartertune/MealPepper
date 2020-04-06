from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, ObjectIdField

"""
    This is designed so that we can store meal plans in MongoDB as well, this may be helpful later, but we probably
    wont use this except as an idea for how to structure the data 
"""


class DailyPlan(EmbeddedDocument):
    plan: ListField(ListField(EmbeddedDocumentField(ObjectIdField)))  # [[FoodItem Id]]


class MealPlan(Document):
    sunday = EmbeddedDocumentField(DailyPlan)
    monday = EmbeddedDocumentField(DailyPlan)
    tuesday = EmbeddedDocumentField(DailyPlan)
    wednesday = EmbeddedDocumentField(DailyPlan)
    thursday = EmbeddedDocumentField(DailyPlan)
    friday = EmbeddedDocumentField(DailyPlan)
    saturday = EmbeddedDocumentField(DailyPlan)
    # may add things here for something like total calories, carbs, cost, etc. instead of calculating it later


"""
    What Front-End should get:
    
    data: {
        sunday: [[{id: "asdfa", name: "Avocado", price: "1.99", nutritionalData: (NutritionalMap as Json) }, ...]]
        monday: ...
    }
"""