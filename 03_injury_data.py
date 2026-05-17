import requests
import pandas as pd
import time

# Φορτώνουμε το API key από το .env αρχείο
# Έτσι το key δεν εμφανίζεται ποτέ στον κώδικα
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

# Δοκιμάζουμε ότι το API key δουλεύει
print("Ελέγχω σύνδεση με API...")
response = requests.get(
    "https://v3.football.api-sports.io/status",
    headers=headers
)

data = response.json()
print("Κατάσταση:", data)
# Κατεβάζουμε injuries από Premier League
# Season 2023 = σεζόν 2022-23
# League ID 39 = Premier League

print("\nΚατεβάζω injury data...")

all_injuries = []

for season in [2022, 2023]:
    print(f"Σεζόν {season}...")
    
    response = requests.get(
        "https://v3.football.api-sports.io/injuries",
        headers=headers,
        params={
            "league": 39,  # Premier League
            "season": season
        }
    )
    
    data = response.json()
    
    if data['response']:
        all_injuries.extend(data['response'])
        print(f"  Βρήκα {len(data['response'])} εγγραφές")
    else:
        print(f"  Κανένα δεδομένο για {season}")
    
    # Περιμένουμε 1 δευτερόλεπτο για να μην κατακλύσουμε το API
    time.sleep(1)

print(f"\nΣύνολο εγγραφών: {len(all_injuries)}")
# Μετατρέπουμε σε DataFrame και βλέπουμε τι έχουμε
injuries_list = []

for injury in all_injuries:
    injuries_list.append({
        'player_name': injury['player']['name'],
        'player_id': injury['player']['id'],
        'team': injury['team']['name'],
        'injury_type': injury['player']['type'],
        'injury_reason': injury['player']['reason'],
        'fixture_date': injury['fixture']['date'],
    })

df_injuries = pd.DataFrame(injuries_list)

print("\nΠρώτες 5 εγγραφές:")
print(df_injuries.head())

# Αποθηκεύουμε
df_injuries.to_csv("data/injuries.csv", index=False)
print("\nΑποθηκεύτηκε στο data/injuries.csv!")