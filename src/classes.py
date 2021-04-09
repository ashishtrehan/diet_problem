class Values(object):
    def __init__(self,object):
        self.name = object.get("name")
        self.group = object.get("group")
        self.protein = object.get("protein (g)")
        self.calcium = object.get("calcium (g)")
        self.sodium = object.get("sodium (g)")
        self.fiber = object.get("fiber (g)")
        self.vitaminc = object.get("vitaminc (g)")
        self.potassium = object.get("potassium (g)")
        self.carbohydrate = object.get("carbohydrate (g)")
        self.sugars = object.get("sugars (g)")
        self.fat = object.get("fat (g)")
        self.water = object.get("water (g)")
        self.calories = object.get("calories")
        self.saturated = object.get("saturated (g)")
        self.monounsat = object.get("monounsat (g)")
        self.polyunsat = object.get("polyunsat (g)")
    

class URL:
    def __init__(self,year,month,week,url,ingredients):
        self.year = year
        self.month = month
        self.week = week
        self.url = url
        self.ingredients = ingredients