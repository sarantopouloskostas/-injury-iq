import pandas as pd

# Φορτώνουμε και τα δύο datasets
print("Φορτώνω data...")
df_stats = pd.read_csv("data/player_stats.csv", header=[0,1], index_col=[0,1,2,3])
df_stats.columns = ['nation', 'pos', 'age', 'born', 
                    'matches', 'starts', 'minutes', '90s',
                    'goals', 'assists', 'g_a', 'g_pk', 'pk', 'pkatt',
                    'yellow_cards', 'red_cards',
                    'goals_90', 'assists_90', 'g_a_90', 'g_pk_90', 'g_a_pk_90']
df_stats = df_stats.reset_index()

df_injuries = pd.read_csv("data/injuries.csv")

print(f"Stats: {df_stats.shape}")
print(f"Injuries: {df_injuries.shape}")

# Μετράμε πόσες φορές τραυματίστηκε κάθε παίκτης
injury_counts = df_injuries.groupby('player_name').agg(
    total_injuries=('injury_reason', 'count'),
    injury_types=('injury_reason', lambda x: ', '.join(x.unique()))
).reset_index()

print(f"\nΜοναδικοί παίκτες με injuries: {len(injury_counts)}")
print(injury_counts.head())
# Καθαρίζουμε τα ονόματα για να ταιριάξουν
# Το FBref έχει "Bukayo Saka" αλλά το API έχει "B. Saka"
# Φτιάχνουμε σύντομη μορφή και για τα δύο

def shorten_name(full_name):
    parts = full_name.strip().split()
    if len(parts) >= 2:
        return parts[0][0] + '. ' + ' '.join(parts[1:])
    return full_name

df_stats['player_short'] = df_stats['player'].apply(shorten_name)

# Merge — συνδυάζουμε τα δύο datasets
df_merged = df_stats.merge(
    injury_counts,
    left_on='player_short',
    right_on='player_name',
    how='left'
)

# Παίκτες χωρίς injuries παίρνουν 0
df_merged['total_injuries'] = df_merged['total_injuries'].fillna(0)
df_merged['injury_types'] = df_merged['injury_types'].fillna('None')

# Φτιάχνουμε το target variable — τραυματίστηκε ή όχι
df_merged['injured'] = (df_merged['total_injuries'] > 0).astype(int)

print(f"\nΠαίκτες με injuries: {df_merged['injured'].sum()}")
print(f"Παίκτες χωρίς injuries: {(df_merged['injured'] == 0).sum()}")
print(f"\nΠοσοστό τραυματισμών: {df_merged['injured'].mean()*100:.1f}%")

# Αποθηκεύουμε
df_merged.to_csv("data/merged_data.csv", index=False)
print("\nΑποθηκεύτηκε στο data/merged_data.csv!")