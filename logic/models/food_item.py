from mongoengine import Document, StringField, BooleanField, \
    EmbeddedDocument, EmbeddedDocumentField, IntField, DecimalField, ListField

from enum import Enum


class Diets(Enum):
    DAIRY_FREE = "dairy-free"
    ENGINE_TWO = "engine-2"
    GLUTEN_FREE = "gluten-free"
    LOW_SODIUM = "low-sodium"
    PALEO = "paleo-friendly"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    KETO_FRIENDLY = "keto-friendly"


class ServingInfo(EmbeddedDocument):
    servingSizeUom = StringField()  # unit of measure
    totalSize = IntField()  # total size of item
    servingSize = DecimalField()  # size of single serving


class NutritionMap(EmbeddedDocument):
    isDense = BooleanField()  # probably won't this, may be helpful in a heuristic
    key = StringField()
    name = StringField()
    defaultDvp = DecimalField()  # percent of daily value
    perServing = DecimalField()
    uom = StringField()  # unit of measure
    fullDvp = DecimalField()  # full daily value


#TODO add indexes
class FoodItem(Document):
    id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    slug = StringField(required=True)
    imageUrl = StringField()
    thumbnailUrl = StringField()
    servingInfo = EmbeddedDocumentField(ServingInfo)
    categories = ListField(StringField())
    ingredientList = ListField(StringField())
    brand = StringField()
    price = DecimalField()
    diets = ListField(StringField(choices=[d.value for d in Diets]))  # Should be one of diets in DIET ENUM


"""TODO:
    - Allow for different stores
    - Allow for Foods to be rated (so we can optimize for ratings)
    - Allow including allergens
    - Allow for calculating heuristics based on constraints
"""
