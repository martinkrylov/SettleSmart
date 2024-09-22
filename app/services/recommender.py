from app.database import get_database_connection

TAXONOMY_FIELD = "Healthcare Provider Taxonomy Code_1"
CITY_FIELD = "Provider Business Practice Location Address City Name"
STATE_FIELD = "Provider Business Practice Location Address State Name"

class Doctor:
    def __init__(self, name: str, address: str, phone_number: str, distance: float):
        pass

    def to_json(self):
        return {
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "distance": self.distance
        }

class LocationRecommendations:
    def __init__(self, location_data: dict, doctors: list[Doctor]):
        self.city = location_data['city']
        self.city_ascii = location_data['city_ascii']
        self.state_id = location_data['state_id']
        self.state_name = location_data['state_name']
        self.lat = location_data['lat']
        self.lng = location_data['lng']
        self.population = location_data['population']
        self.density = location_data['density']
        self.military = location_data['military']
        self.timezone = location_data['timezone']
        self.doctors = doctors  # Store the doctors list

    def to_json(self):
        return {
            "city": self.city,
            "city_ascii": self.city_ascii,
            "state_id": self.state_id,
            "state_name": self.state_name,
            "lat": self.lat,
            "lng": self.lng,
            "population": self.population,
            "density": self.density,
            "military": self.military,
            "timezone": self.timezone,
            "doctors": self.doctors
        }

class Recommender:
    def __init__(self):
        self.db = get_database_connection()

    def get_recommendations(self, user):
        required_taxonomies = [item['Taxonomy Code'] for item in list(self.db.resources.conditions.find({"Conditions": {"$in": user['conditions']}}))]
        # get all doctors with same taxonomy
        doctors = list(self.db.resources.healthcare_professionals.find({TAXONOMY_FIELD: {"$in": required_taxonomies}}))
        # get all unique locations
        doctor_locations = dict()
        for doctor in doctors:
            key = (doctor[CITY_FIELD], doctor[STATE_FIELD])
            if key not in doctor_locations:
                doctor_locations[key] = []
            doctor_locations[key].append(doctor)
        #filter locations
        locations = []
        for location in doctor_locations.keys():
            city = ' '.join(word.capitalize() for word in location[0].split())
            state = location[1].upper()
            city_data = self.db.resources.cities.find_one({"city": city, "state_id": state})
            if city_data is None:
                print(f"City data not found for {city}, {state}")
                continue
            locations.append(LocationRecommendations(city_data, doctor_locations[location]))

        return locations

        