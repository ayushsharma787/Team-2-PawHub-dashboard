# city_data.py
import pandas as pd

CITY_COORDS = {
    "Mumbai":    (19.0760, 72.8777),
    "Delhi":     (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Indore":    (22.7196, 75.8577),
    "Pune":      (18.5204, 73.8567),
    "Hyderabad": (17.3850, 78.4867),
}

PLACES = [
    {"city":"Mumbai","name":"PawFect Vet Clinic","category":"Vet Centre","lat":19.0822,"lon":72.8914,"rating":4.7,"reviews":312,"note":"24hr emergency"},
    {"city":"Mumbai","name":"Bandstand Dog Park","category":"Dog Park","lat":19.0474,"lon":72.8179,"rating":4.5,"reviews":891,"note":"Sea-facing off-leash area"},
    {"city":"Mumbai","name":"The Doggy Cafe","category":"Dog Cafe","lat":19.0596,"lon":72.8295,"rating":4.3,"reviews":204,"note":"Bandra favourite"},
    {"city":"Mumbai","name":"Happy Paws Grooming","category":"Grooming","lat":19.1197,"lon":72.9082,"rating":4.6,"reviews":178,"note":"Mobile grooming available"},
    {"city":"Mumbai","name":"Vet Express Andheri","category":"Vet Centre","lat":19.1139,"lon":72.8697,"rating":4.4,"reviews":256,"note":"Walk-ins welcome"},
    {"city":"Mumbai","name":"Canine Corner Pet Store","category":"Pet Store","lat":19.0728,"lon":72.8826,"rating":4.2,"reviews":143,"note":"Large accessories range"},
    {"city":"Delhi","name":"Sanjay Lake Dog Park","category":"Dog Park","lat":28.6594,"lon":77.3129,"rating":4.4,"reviews":634,"note":"Large fenced area"},
    {"city":"Delhi","name":"Capital Vet Hospital","category":"Vet Centre","lat":28.5672,"lon":77.2100,"rating":4.8,"reviews":487,"note":"Top rated in South Delhi"},
    {"city":"Delhi","name":"Paws & Claws Cafe","category":"Dog Cafe","lat":28.5245,"lon":77.1855,"rating":4.1,"reviews":312,"note":"Pet menu available"},
    {"city":"Delhi","name":"Delhi Dog Grooming Studio","category":"Grooming","lat":28.6328,"lon":77.2197,"rating":4.5,"reviews":221,"note":"Spa treatments"},
    {"city":"Delhi","name":"Lodhi Dog Zone","category":"Dog Park","lat":28.5916,"lon":77.2244,"rating":4.3,"reviews":412,"note":"Morning hours only"},
    {"city":"Delhi","name":"Pet Nation Store","category":"Pet Store","lat":28.5487,"lon":77.1937,"rating":4.0,"reviews":98,"note":"Organic food range"},
    {"city":"Bengaluru","name":"Cubbon Park Dog Area","category":"Dog Park","lat":12.9763,"lon":77.5929,"rating":4.6,"reviews":1203,"note":"City centre, very popular"},
    {"city":"Bengaluru","name":"CUPA Animal Hospital","category":"Vet Centre","lat":12.9853,"lon":77.6095,"rating":4.9,"reviews":892,"note":"Best rescue & care in BLR"},
    {"city":"Bengaluru","name":"Barks & Brews","category":"Dog Cafe","lat":12.9352,"lon":77.6245,"rating":4.4,"reviews":567,"note":"Koramangala hotspot"},
    {"city":"Bengaluru","name":"The Groom Room","category":"Grooming","lat":12.9580,"lon":77.6481,"rating":4.7,"reviews":334,"note":"Indiranagar, premium service"},
    {"city":"Bengaluru","name":"Whitefield Pet Clinic","category":"Vet Centre","lat":12.9702,"lon":77.7500,"rating":4.3,"reviews":289,"note":"East BLR coverage"},
    {"city":"Bengaluru","name":"Pets Paradise","category":"Pet Store","lat":12.9279,"lon":77.6271,"rating":4.1,"reviews":176,"note":"Imported food brands"},
    {"city":"Indore","name":"Indore Pet Clinic","category":"Vet Centre","lat":22.7241,"lon":75.8839,"rating":4.5,"reviews":187,"note":"Experienced small animal vet"},
    {"city":"Indore","name":"Rajwada Dog Park","category":"Dog Park","lat":22.7190,"lon":75.8573,"rating":4.0,"reviews":312,"note":"Central location"},
    {"city":"Indore","name":"Pawsome Cafe Indore","category":"Dog Cafe","lat":22.7332,"lon":75.8865,"rating":4.2,"reviews":145,"note":"Newly opened"},
    {"city":"Indore","name":"FurFresh Grooming","category":"Grooming","lat":22.7456,"lon":75.8921,"rating":4.4,"reviews":98,"note":"Home visits available"},
    {"city":"Indore","name":"City Pet Hospital","category":"Vet Centre","lat":22.7083,"lon":75.8683,"rating":4.3,"reviews":234,"note":"24hr service"},
    {"city":"Indore","name":"Petzone Indore","category":"Pet Store","lat":22.7201,"lon":75.8801,"rating":3.9,"reviews":67,"note":"Good accessories range"},
    {"city":"Pune","name":"Paws Pune Vet","category":"Vet Centre","lat":18.5362,"lon":73.8479,"rating":4.6,"reviews":298,"note":"Koregaon Park"},
    {"city":"Pune","name":"Empress Garden Dog Zone","category":"Dog Park","lat":18.5388,"lon":73.8782,"rating":4.4,"reviews":534,"note":"Weekends get crowded"},
    {"city":"Pune","name":"Doggo Cafe Baner","category":"Dog Cafe","lat":18.5590,"lon":73.7868,"rating":4.3,"reviews":276,"note":"IT crowd favourite"},
    {"city":"Pune","name":"Snip & Wag","category":"Grooming","lat":18.5204,"lon":73.8567,"rating":4.5,"reviews":189,"note":"Appointment only"},
    {"city":"Pune","name":"Pune Animal Hospital","category":"Vet Centre","lat":18.4912,"lon":73.8278,"rating":4.7,"reviews":412,"note":"Surgical facility"},
    {"city":"Hyderabad","name":"Jubilee Hills Vet","category":"Vet Centre","lat":17.4314,"lon":78.4079,"rating":4.7,"reviews":341,"note":"Premium area clinic"},
    {"city":"Hyderabad","name":"KBR Park Dog Walk","category":"Dog Park","lat":17.4256,"lon":78.4344,"rating":4.5,"reviews":789,"note":"Gated, safe, early morning"},
    {"city":"Hyderabad","name":"Cafe Barko","category":"Dog Cafe","lat":17.4478,"lon":78.3916,"rating":4.2,"reviews":223,"note":"Banjara Hills"},
    {"city":"Hyderabad","name":"PawLux Grooming","category":"Grooming","lat":17.4100,"lon":78.4567,"rating":4.6,"reviews":167,"note":"Luxury spa packages"},
    {"city":"Hyderabad","name":"CCMB Pet Clinic","category":"Vet Centre","lat":17.3742,"lon":78.5533,"rating":4.4,"reviews":198,"note":"Uppal area"},
    {"city":"Hyderabad","name":"City Pet Mart","category":"Pet Store","lat":17.3952,"lon":78.4712,"rating":4.1,"reviews":112,"note":"Budget friendly"},
]

CATEGORY_COLORS = {
    "Vet Centre": [229, 57, 53],
    "Dog Park":   [76, 175, 80],
    "Dog Cafe":   [212, 134, 11],
    "Grooming":   [111, 78, 55],
    "Pet Store":  [123, 31, 162],
}
CATEGORY_ICONS = {
    "Vet Centre": "🏥", "Dog Park": "🌳",
    "Dog Cafe": "☕", "Grooming": "✂️", "Pet Store": "🛍️",
}

def get_places_df():
    return pd.DataFrame(PLACES)
