from app import mongo

class User:
    def __init__(self, name, condition, city):
        self.name = name
        self.condition = condition
        self.city = city

    def save(self):
        if mongo.db:  # Check if MongoDB is initialized
            mongo.db.users.insert_one({
                'name': self.name,
                'condition': self.condition,
                'city': self.city
            })
        else:
            print(f"Skipping save for {self.name}, MongoDB not initialized.")
