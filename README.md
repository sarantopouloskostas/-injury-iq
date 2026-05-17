# InjuryIQ — Football Injury Prediction Dashboard

> A machine learning-powered dashboard for predicting injury risk in professional football players.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)
![Streamlit](https://img.shields.io/badge/App-Streamlit-red)
![Accuracy](https://img.shields.io/badge/Accuracy-70.4%25-green)

**🔗 Live Demo:** [injuryiq.streamlit.app](https://injuryiq.streamlit.app)

---

## Overview

InjuryIQ is a predictive analytics tool that estimates the injury risk of professional football players using machine learning. Built on Premier League data from the 2022–2024 seasons, it provides clubs and coaching staff with actionable insights to protect both player health and squad value.

The dashboard was developed as an academic project and subsequently recognized by faculty as a commercially viable concept worth pursuing.

---

## Features

- **Team Overview** — Full squad ranked by injury risk score, with risk distribution charts and a position-based radar chart
- **Player Search** — Individual player risk profile with injury history, predicted days out, and a visual risk gauge
- **Financial Impact** — Estimated financial exposure per player based on market value and injury probability, including a bubble chart of value vs risk

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| ML Model | XGBoost (70.4% accuracy) |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Web App | Streamlit |
| Data Sources | FBref, API-Football |
| Deployment | Streamlit Cloud |

---

## Methodology

### Data Collection
- **Player statistics** collected from FBref via the `soccerdata` library — 774 players across 2 Premier League seasons (2022/23, 2023/24)
- **Injury records** collected from API-Football — 6,909 real injury events

### Feature Engineering
The model uses the following features to predict injury risk:
- Age
- Minutes played
- Matches & starts
- Yellow and red cards
- Goals and assists per 90 minutes
- Player position (encoded)

### Model
- Algorithm: **XGBoost Classifier**
- Train/test split: 80/20
- Accuracy: **70.4%**
- Target variable: whether a player sustained an injury during the season

### Risk Score
Each player receives a risk score from 0 to 100, derived from the model's predicted injury probability. Players are categorized as:
- 🟢 **Low** — 0 to 40
- 🟡 **Medium** — 40 to 70
- 🔴 **High** — 70 to 100

### Financial Impact
Financial exposure is estimated as:

```
Financial Impact (€M) = Estimated Market Value × (Risk Score / 100)
```

Market values are estimated from performance data. Production version would integrate live Transfermarkt API data.

---

## Project Structure

```
injury-iq/
│
├── 01_data_collection.py     # FBref data pipeline
├── 02_data_cleaning.py       # Data cleaning & preprocessing
├── 03_injury_data.py         # API-Football injury data collection
├── 04_merge_data.py          # Merge player stats + injury records
├── 05_model_training.py      # XGBoost model training & evaluation
├── app.py                    # Streamlit web application
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Installation & Local Setup

```bash
# Clone the repository
git clone https://github.com/sarantopouloskostas/-injury-iq.git
cd -injury-iq

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo API_KEY=your_api_football_key > .env

# Run data pipeline
python 01_data_collection.py
python 03_injury_data.py
python 04_merge_data.py
python 05_model_training.py

# Launch the app
streamlit run app.py
```

---

## Roadmap

- [ ] Integrate real club training load data
- [ ] Add GPS and biometric features
- [ ] Live market values via Transfermarkt API
- [ ] Pilot with a professional club
- [ ] Expand to additional leagues

---

## Author

**Konstantinos Sarantopoulos**
Computer Engineering Student

---

## Disclaimer

Market values and injury predictions are estimates based on publicly available data. This tool is intended for research and demonstration purposes. Production deployment would require proprietary club data for higher accuracy.