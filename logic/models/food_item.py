from mongoengine import connect, Document, StringField, BooleanField, \
    EmbeddedDocument, EmbeddedDocumentField, IntField, DecimalField, ListField, GenericEmbeddedDocumentField

from enum import Enum

connection = connect("meal_planner_db")


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

    totalSizeUom = StringField()
    secondaryServingSize = DecimalField()
    secondaryTotalSize = DecimalField()
    servingsPerContainerDisplay = StringField()
    secondaryTotalSizeUom = StringField()
    servingsPerContainer = DecimalField()
    secondaryServingSizeUom = StringField()
    servingSizeDisplay = StringField()
    meta = {
        "strict": False
    }


class NutritionData(EmbeddedDocument):
    isDense = BooleanField()  # probably won't this, may be helpful in a heuristic
    key = StringField()
    name = StringField()
    defaultDvp = DecimalField()  # percent of daily value
    perServing = DecimalField()
    uom = StringField()  # unit of measure
    fullDvp = DecimalField()  # full daily value
    perServingDisplay = StringField()
    defaultDvpDisplay = StringField()
    meta = {
        "strict": False
    }


class NutritionMap(EmbeddedDocument):
    carbohydrates = EmbeddedDocumentField(NutritionData)
    vitaminB6 = EmbeddedDocumentField(NutritionData)
    vitaminD = EmbeddedDocumentField(NutritionData)
    totalFat = EmbeddedDocumentField(NutritionData)
    phosphorus = EmbeddedDocumentField(NutritionData)
    magnesium = EmbeddedDocumentField(NutritionData)
    zinc = EmbeddedDocumentField(NutritionData)
    vitaminA = EmbeddedDocumentField(NutritionData)
    calcium = EmbeddedDocumentField(NutritionData)
    cholesterol = EmbeddedDocumentField(NutritionData)
    potassium = EmbeddedDocumentField(NutritionData)
    iron = EmbeddedDocumentField(NutritionData)
    folate = EmbeddedDocumentField(NutritionData)
    sugar = EmbeddedDocumentField(NutritionData)
    vitaminE = EmbeddedDocumentField(NutritionData)
    calories = EmbeddedDocumentField(NutritionData)
    copper = EmbeddedDocumentField(NutritionData)
    polyunsaturatedFat = EmbeddedDocumentField(NutritionData)
    protein = EmbeddedDocumentField(NutritionData)
    selenium = EmbeddedDocumentField(NutritionData)
    sodium = EmbeddedDocumentField(NutritionData)
    vitaminC = EmbeddedDocumentField(NutritionData)
    vitaminB12 = EmbeddedDocumentField(NutritionData)
    transFat = EmbeddedDocumentField(NutritionData)
    manganese = EmbeddedDocumentField(NutritionData)
    saturatedFat = EmbeddedDocumentField(NutritionData)
    monounsaturatedFat = EmbeddedDocumentField(NutritionData)
    vitaminK = EmbeddedDocumentField(NutritionData)
    fiber = EmbeddedDocumentField(NutritionData)
    riboflavin = EmbeddedDocumentField(NutritionData)
    pantothenicAcid = EmbeddedDocumentField(NutritionData)
    thiamin = EmbeddedDocumentField(NutritionData)
    niacin = EmbeddedDocumentField(NutritionData)
    folicAcid = EmbeddedDocumentField(NutritionData)
    fatCalories = EmbeddedDocumentField(NutritionData)
    addedSugar = EmbeddedDocumentField(NutritionData)
    fructose = EmbeddedDocumentField(NutritionData)
    maltose = EmbeddedDocumentField(NutritionData)
    dextrose = EmbeddedDocumentField(NutritionData)
    galactose = EmbeddedDocumentField(NutritionData)

    meta = {
        "strict": False
    }


class BrandInfo(EmbeddedDocument):
    _id = StringField()
    slug = StringField()
    name = StringField()
    meta = {
        "strict": False
    }

#TODO add indexes
class FoodItem(Document):
    _id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    slug = StringField()
    imageUrl = StringField()
    thumbnailUrl = StringField()
    servingInfo = EmbeddedDocumentField(ServingInfo)
    nutritionMap = EmbeddedDocumentField(NutritionMap)
    categories = ListField(StringField())
    ingredientList = ListField(StringField())
    price = DecimalField()
    brand = EmbeddedDocumentField(BrandInfo)
    diets = ListField(StringField())  # Should be one of diets in DIET ENUM
    allergenList = ListField(StringField())
    pricePerServing = DecimalField()

    # Not Used-------
    asin = StringField()
    identifier = StringField()
    mediaList = ListField()
    nutritionGroup = StringField()
    nutritionLabelFormat = StringField()
    facilityAllergenList = ListField()
    certificationList = ListField()
    additiveList = ListField()
    meta = {
        'indexes': ['name', 'diets', 'price', 'allergenList'],
        'strict': False
    }
"""TODO:
    - Allow for different stores
    - Allow for Foods to be rated (so we can optimize for ratings)
    - Allow including allergens
    - Allow for calculating heuristics based on constraints
"""

