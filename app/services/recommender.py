from app.database import get_database_connection

TAXONOMY_FIELD = "Healthcare Provider Taxonomy Code_1"
CITY_FIELD = "Provider Business Practice Location Address City Name"
STATE_FIELD = "Provider Business Practice Location Address State Name"

class LocationRecommendations:
    def __init__(self, location_data: dict, doctors_in: list):
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
        self.doctors = []
        for doctor in doctors_in:
            self.doctors.append({
                'Authorized Official First Name': doctor['Authorized Official First Name'],
                'Authorized Official Last Name': doctor['Authorized Official Last Name'],
                'Authorized Official Telephone Number': doctor['Authorized Official Telephone Number'],
            })

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
        user_conditions = user['conditions']
        required_taxonomies = [item['Taxonomy Code'] for item in list(self.db.resources.conditions.find({"Conditions": {"$in": user_conditions}}))]
        
        prev_locations = {}
        locations = {}
        for index, taxonomy in enumerate(required_taxonomies):
            # get all doctors with same taxonomy
            doctors = list(self.db.resources.healthcare_professionals.find({TAXONOMY_FIELD: taxonomy}))
            for doctor in doctors:
                if not isinstance(doctor[CITY_FIELD], str) or not isinstance(doctor[STATE_FIELD], str):
                    continue

                loc_key = (doctor[CITY_FIELD], doctor[STATE_FIELD])
                if index == 0:
                    if loc_key not in locations:
                        locations[loc_key] = []
                    locations[loc_key].append(doctor)
                elif loc_key in prev_locations:
                    if loc_key not in locations:
                        locations[loc_key] = prev_locations[loc_key]
                    locations[loc_key].append(doctor)
            prev_locations = locations
            locations = {}
                    
        #filter locations
        results = []
        for location in prev_locations.keys():
            city = ' '.join(word.capitalize() for word in location[0].split())
            state = location[1].upper()
            city_data = self.db.resources.cities.find_one({"city": city, "state_id": state})
            if city_data is None:
                print(f"City data not found for {city}, {state}")
                continue
            results.append(LocationRecommendations(city_data, prev_locations[location]))

        return results

        