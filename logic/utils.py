

GRAMS_IN_OUNCE = 28.3495
GRAMS_IN_POUND = 453.592

def isGram(s):
    return s == "g" or s =="gram"

def isOunce(s):
    return s == "oz" or s =="ounce" or s == "OUNCE"

def isPound(s):
    return s == "lb" or s == "lbs" or s == "pound"

def isKnownUnit(s):
    return isPound(s) or isOunce(s) or isGram(s)


# takes in a [unit, amount of unit] array and converts to grams
def convertToGrams(u_a):
    unit = u_a[0]
    amount = u_a[1]
    if isGram(unit):
        return float(amount)
    if isOunce(unit):
        return float(amount) * GRAMS_IN_OUNCE
    if isPound(unit):
        return float(amount) * GRAMS_IN_POUND

    print("ERROR: Unrecognized Unit")
    return -1

def calculate_price_per_serving(food, debug=False):
    if not food.servingInfo:
        print(food.to_json())
        return 99

    if food.servingInfo.servingsPerContainer:
        price = food.price
        serving_count = food.servingInfo.servingsPerContainer
        return price / float(serving_count)

    # Else this is a by weight produce that needs to be calculated
    si = food.servingInfo

    # tuples of (unit, servingSize)
    s = [si.servingSizeUom, si.servingSize]
    s2 = [si.secondaryServingSizeUom, si.secondaryServingSize]
    t = [si.totalSizeUom, si.totalSize]
    t2 = [si.secondaryTotalSizeUom, si.secondaryTotalSize]

    if debug:
        print(s, s2, t, t2)

    # convert known servings units to grams
    if isKnownUnit(s[0]):
        servingsInGrams = convertToGrams(s)
    elif isKnownUnit(s2[0]):
        servingsInGrams = convertToGrams(s2)
    else:
        return 99

    # convert known total units to grams
    if isKnownUnit(t[0]):
        #TODO: Converts items priced per pound correctly (need to add store info for more data
        if isPound(t[0]) and t[1] != 1:
            if debug:
                print(food.store.to_json())
            t[1] = 1
            if food.slug == "organic-clementine-mandarin-3ecac6":
                t[1] = 2
        totalInGrams = convertToGrams(t)
    elif isKnownUnit(t2[0]):
        if isPound(t2[0]) and t2[1] != 1:
            if debug:
                print(food.store.to_json())
            t2[1] = 1
        totalInGrams = convertToGrams(t2)
    else:
        return 99

    if debug:
        print(totalInGrams, servingsInGrams)
    servingsPerContainer = totalInGrams / servingsInGrams
    if servingsPerContainer == 0:
        return 99
    pricePerServing = float(food.price) / float(servingsPerContainer)
    return pricePerServing


bad_data_list = ["farm-raised-littleneck-clams-f3faa7",
                 "365-everyday-value-organic-boneless-skinless-chicken-breast-7298db",
                 "marys-chicken-whole-heirloom-chicken-6ee8ea",
                 "365-everyday-value-whole-chicken-6a03a1",
                 "little-neck-clams-dc7420"]