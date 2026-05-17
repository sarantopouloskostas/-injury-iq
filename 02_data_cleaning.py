import pandas as pd
import numpy as np

# Φορτώνουμε τα data που αποθηκεύσαμε
print("Φορτώνω data...")
df = pd.read_csv("data/player_stats.csv", header=[0,1], index_col=[0,1,2,3])

# Βλέπουμε τι έχουμε
print("Διαστάσεις:", df.shape)
print("\nΟνόματα στηλών:")
print(df.columns.tolist())
# Ισοπεδώνουμε τις διπλές επικεφαλίδες σε απλά ονόματα
df.columns = ['nation', 'pos', 'age', 'born', 
              'matches', 'starts', 'minutes', '90s',
              'goals', 'assists', 'g_a', 'g_pk', 'pk', 'pkatt',
              'yellow_cards', 'red_cards',
              'goals_90', 'assists_90', 'g_a_90', 'g_pk_90', 'g_a_pk_90']

# Κάνουμε reset το index για να έχουμε κανονικές στήλες
df = df.reset_index()

# Βλέπουμε τι έχουμε τώρα
print("\nΝέες στήλες:")
print(df.columns.tolist())
print("\nΠρώτες 3 γραμμές:")
print(df.head(3))
# Ελέγχουμε για missing values
print("\nMissing values ανά στήλη:")
print(df.isnull().sum())

# Ελέγχουμε τους τύπους δεδομένων
print("\nΤύποι δεδομένων:")
print(df.dtypes)