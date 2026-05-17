import soccerdata as sd
import pandas as pd

# Συνδεόμαστε στο FBref
fbref = sd.FBref(leagues="ENG-Premier League", seasons=["2223", "2324"])

# Κατεβάζουμε stats παικτών
print("Κατεβάζω data...")
player_stats = fbref.read_player_season_stats(stat_type="standard")

print("Έγινε! Διαστάσεις:", player_stats.shape)
print(player_stats.head())
# Αποθηκεύουμε σε CSV
player_stats.to_csv("data/player_stats.csv")
print("Αποθηκεύτηκε στο data/player_stats.csv!")