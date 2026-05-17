import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import joblib

# ============================================
# ΒΗΜΑ 1 - ΦΟΡΤΩΝΟΥΜΕ ΤΑ MERGED DATA
# ============================================

# Διαβάζουμε το αρχείο που φτιάξαμε στο προηγούμενο βήμα
df = pd.read_csv("data/merged_data.csv")
print(f"Φορτώθηκαν {len(df)} παίκτες")

# ============================================
# ΒΗΜΑ 2 - ΕΠΙΛΟΓΗ FEATURES
# ============================================

# Features = οι μεταβλητές που δίνουμε στο model για να μάθει
# Διαλέγουμε αυτά που λογικά επηρεάζουν τον κίνδυνο τραυματισμού

# 'pos' = θέση παίκτη (DF, MF, FW, GK)
# Το model πρέπει να ξέρει τη θέση γιατί οι defenders τραυματίζονται 
# διαφορετικά από τους forwards
le = LabelEncoder()
df['pos_encoded'] = le.fit_transform(df['pos'].fillna('Unknown'))

# Επιλέγουμε τις στήλες που θα χρησιμοποιήσει το model
features = [
    'age',          # Ηλικία — όσο μεγαλύτερος, τόσο μεγαλύτερος κίνδυνος
    'minutes',      # Λεπτά συμμετοχής — περισσότερα λεπτά = περισσότερη κόπωση
    'matches',      # Αριθμός αγώνων — συχνότητα συμμετοχής
    'starts',       # Πόσες φορές ήταν βασικός
    'yellow_cards', # Κίτρινες κάρτες — δείκτης aggressiveness
    'red_cards',    # Κόκκινες κάρτες
    'goals_90',     # Γκολ ανά 90 λεπτά — ένταση παιχνιδιού
    'assists_90',   # Ασίστ ανά 90 λεπτά
    'pos_encoded',  # Θέση παίκτη (κωδικοποιημένη σε αριθμό)
]

# X = τα features που δίνουμε στο model
X = df[features]

# y = αυτό που θέλουμε να προβλέψει (0=δεν τραυματίστηκε, 1=τραυματίστηκε)
y = df['injured']

print(f"\nFeatures: {features}")
print(f"Σύνολο παραδειγμάτων: {len(X)}")

# ============================================
# ΒΗΜΑ 3 - ΧΩΡΙΖΟΥΜΕ ΣΕ TRAINING ΚΑΙ TEST SET
# ============================================

# Χωρίζουμε τα data σε δύο μέρη:
# - Training set (80%): αυτά δίνουμε στο model για να μάθει
# - Test set (20%): αυτά κρατάμε κρυφά για να δοκιμάσουμε πόσο καλό είναι
# random_state=42 σημαίνει ότι το χώρισμα είναι πάντα το ίδιο (αναπαραγώγιμο)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% για testing
    random_state=42     # για αναπαραγωγιμότητα
)

print(f"\nTraining set: {len(X_train)} παίκτες")
print(f"Test set: {len(X_test)} παίκτες")

# ============================================
# ΒΗΜΑ 4 - ΕΚΠΑΙΔΕΥΟΥΜΕ ΤΟ XGBOOST MODEL
# ============================================

# XGBoost = ένας από τους πιο δυνατούς αλγορίθμους ML
# Λειτουργεί χτίζοντας πολλά decision trees και τα συνδυάζει
print("\nΕκπαιδεύω το model...")

# Αντικατέστησε τον ορισμό του model με αυτό:

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    random_state=42,
    eval_metric='logloss'
)

# Εδώ γίνεται η εκπαίδευση — το model κοιτά τα training data
# και μαθαίνει ποια features συνδέονται με τραυματισμό
model.fit(X_train, y_train)
print("Εκπαίδευση ολοκληρώθηκε!")

# ============================================
# ΒΗΜΑ 5 - ΑΞΙΟΛΟΓΟΥΜΕ ΤΟ MODEL
# ============================================

# Δοκιμάζουμε το model στα test data που δεν έχει ξαναδεί
y_pred = model.predict(X_test)

# Accuracy = ποσοστό σωστών προβλέψεων
accuracy = accuracy_score(y_test, y_pred)
print(f"\nΑκρίβεια (Accuracy): {accuracy*100:.1f}%")

# Αναλυτική αναφορά απόδοσης
print("\nΑναλυτική απόδοση:")
print(classification_report(y_test, y_pred, 
      target_names=['Δεν τραυματίστηκε', 'Τραυματίστηκε']))

# ============================================
# ΒΗΜΑ 6 - ΣΩΖΟΥΜΕ ΤΟ MODEL
# ============================================

# joblib = εργαλείο για να αποθηκεύουμε Python objects σε αρχείο
# Έτσι δεν χρειάζεται να εκπαιδεύουμε ξανά κάθε φορά
joblib.dump(model, "models/injury_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")
print("\nΤο model αποθηκεύτηκε στο models/injury_model.pkl!")
# ============================================
# ΒΗΜΑ 7 - ΠΟΙΑ FEATURES ΕΙΝΑΙ ΠΙΟ ΣΗΜΑΝΤΙΚΑ
# ============================================

# Feature importance = πόσο χρησιμοποιεί το model κάθε feature
# για να πάρει αποφάσεις
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
# Ταξινομούμε από το πιο σημαντικό στο λιγότερο
}).sort_values('importance', ascending=False)

print("\nΣημαντικότητα Features:")
print(importance.to_string(index=False))