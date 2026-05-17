import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# ΒΑΣΙΚΗ ΡΥΘΜΙΣΗ
# Πρέπει να είναι η ΠΡΩΤΗ εντολή Streamlit
# ============================================
st.set_page_config(
    page_title="InjuryIQ — Football Injury Analytics",
    page_icon="⚽",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# Πλήρης έλεγχος εμφάνισης μέσω CSS
# ============================================
st.markdown("""
<style>
    /* Κρύβουμε τα default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}

    /* Κύριο background — βαθύ σκούρο μπλε */
    .stApp { background-color: #0A0E1A; }

    /* Αφαιρούμε το default top padding από το main content */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {
        background-color: #0D1120;
        border-right: 1px solid rgba(0, 255, 135, 0.12);
    }
    /* Αφαιρούμε το default padding του sidebar */
    [data-testid="stSidebar"] > div {
        padding: 0 !important;
    }

    /* ---- METRIC CARDS ---- */
    /* Τα κουτιά με τα μεγάλα νούμερα στην κορυφή */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #111827 0%, #161D2F 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 20px 24px;
        transition: all 0.25s ease;
    }
    /* Hover effect — ανεβαίνει και αλλάζει border */
    [data-testid="stMetric"]:hover {
        border-color: rgba(0, 255, 135, 0.35);
        transform: translateY(-2px);
    }
    /* Το μεγάλο νούμερο — φωτεινό πράσινο */
    [data-testid="stMetricValue"] {
        color: #00FF87 !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    /* Η ετικέτα πάνω από το νούμερο */
    [data-testid="stMetricLabel"] {
        color: #9CA3AF !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }

    /* ---- ΤΙΤΛΟΙ ---- */
    h1 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        letter-spacing: -0.5px;
        padding-bottom: 12px;
        border-bottom: 2px solid #00FF87;
        /* Ευθυγράμμιση με το sidebar logo */
        margin-top: 2rem !important;
        margin-bottom: 4px !important;
    }
    h2 { color: #FFFFFF !important; font-weight: 700 !important; }
    /* Section headers — μικρά uppercase */
    h3, h4 {
        color: #D1D5DB !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px !important;
        margin-top: 0 !important;
    }

    /* ---- DROPDOWN ---- */
    div[data-baseweb="select"] * {
        color: #F9FAFB !important;
        background-color: #111827 !important;
        border-color: rgba(255,255,255,0.08) !important;
    }
    div[data-baseweb="popover"] * {
        color: #F9FAFB !important;
        background-color: #111827 !important;
    }
    div[data-baseweb="option"]:hover {
        background-color: #1E2640 !important;
        color: #00FF87 !important;
    }

    /* ---- NAVIGATION RADIO BUTTONS ----
       Κρύβουμε το label "nav" και στυλίζουμε τα buttons
    */
    [data-testid="stRadio"] > label { display: none; }
    [data-testid="stRadio"] div[role="radiogroup"] { gap: 2px !important; }
    [data-testid="stRadio"] label {
        color: #9CA3AF !important;
        font-size: 13px !important;
        font-weight: 500;
        padding: 9px 14px !important;
        border-radius: 8px;
        transition: all 0.15s;
        cursor: pointer;
        width: 100%;
        display: flex !important;
        align-items: center !important;
        gap: 10px;
    }
    [data-testid="stRadio"] label:hover {
        color: #FFFFFF !important;
        background: rgba(255,255,255,0.04) !important;
    }
    /* Μικρό radio κουτάκι δίπλα στο όνομα */
    [data-testid="stRadio"] input[type="radio"] {
        accent-color: #00FF87;
        width: 8px !important;
        height: 8px !important;
    }

    /* ---- INFO BOX ---- */
    [data-testid="stAlert"] {
        background-color: rgba(0,255,135,0.04) !important;
        border: 1px solid rgba(0,255,135,0.15) !important;
        border-radius: 12px !important;
    }
    [data-testid="stAlert"] p {
        color: #D1D5DB !important;
        font-size: 13px !important;
        line-height: 1.7 !important;
    }

    /* ---- DIVIDER ---- */
    hr {
        border-color: rgba(255,255,255,0.05) !important;
        margin: 24px 0 !important;
    }

    /* ---- ΓΕΝΙΚΟ ΚΕΙΜΕΝΟ ---- */
    p { color: #D1D5DB !important; font-size: 13px !important; }
    strong { color: #FFFFFF !important; }
    label { color: #D1D5DB !important; }

    /* ---- DATAFRAME ---- */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* ---- CUSTOM SCROLLBAR ---- */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1E2640; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #00FF87; }

    /* ---- ΚΡΥΒΟΥΜΕ SELECT BOX LABEL ---- */
    [data-testid="stSelectbox"] label { display: none; }
</style>
""", unsafe_allow_html=True)

# ============================================
# ΦΟΡΤΩΝΟΥΜΕ MODEL ΚΑΙ DATA
# @st.cache_resource = φορτώνει ΜΟΝΟ ΜΙΑ ΦΟΡΑ στη μνήμη
# @st.cache_data = cache για data — δεν ξαναδιαβάζει CSV
# ============================================
@st.cache_resource
def load_model():
    # Φορτώνουμε το εκπαιδευμένο XGBoost model από το .pkl αρχείο
    model = joblib.load("models/injury_model.pkl")
    # Label encoder — μετατρέπει θέσεις (DF/MF/FW/GK) σε αριθμούς
    le = joblib.load("models/label_encoder.pkl")
    return model, le

@st.cache_data
def load_data():
    # Φορτώνουμε το merged dataset με παίκτες + injuries
    df = pd.read_csv("data/merged_data.csv")
    return df

# Καλούμε τις functions
model, le = load_model()
df = load_data()

# ============================================
# ΚΑΘΑΡΙΣΜΟΣ DATA
# Κρατάμε μόνο την πιο πρόσφατη σεζόν για κάθε παίκτη
# Αποφεύγουμε διπλότυπα από πολλές σεζόν
# ============================================
df = df.sort_values('season').drop_duplicates(
    subset='player', keep='last'
).reset_index(drop=True)

# ============================================
# ΥΠΟΛΟΓΙΣΜΟΣ RISK SCORE
# Features — ΑΚΡΙΒΩΣ ίδια με αυτά του training
# ============================================
features = ['age', 'minutes', 'matches', 'starts',
            'yellow_cards', 'red_cards', 'goals_90',
            'assists_90', 'pos_encoded']

# Θέση → αριθμός (το model δεν καταλαβαίνει κείμενο)
df['pos_encoded'] = le.transform(df['pos'].fillna('Unknown'))

# predict_proba[:, 1] = πιθανότητα τραυματισμού (0-1) × 100 = (0-100)
df['risk_score'] = (model.predict_proba(df[features])[:, 1] * 100).round(1)

# Κατηγοριοποίηση: 0-40=Low, 40-70=Medium, 70-100=High
df['risk_level'] = pd.cut(
    df['risk_score'],
    bins=[0, 40, 70, 100],
    labels=['Low', 'Medium', 'High']
)

# ============================================
# ΧΑΡΤΟΓΡΑΦΗΣΗ ΘΕΣΕΩΝ
# Μετατρέπουμε σύνθετες θέσεις (DF,MF) σε απλές κατηγορίες
# ============================================
def map_position(pos):
    if pd.isna(pos):
        return 'Unknown'
    pos = str(pos).upper()
    if 'GK' in pos:
        return 'Goalkeeper'
    elif 'DF' in pos:
        return 'Defender'
    elif 'MF' in pos:
        return 'Midfielder'
    elif 'FW' in pos:
        return 'Forward'
    return 'Other'

df['pos_simple'] = df['pos'].apply(map_position)

# ============================================
# ΕΚΤΙΜΗΣΗ ΑΞΙΑΣ ΠΑΙΚΤΩΝ
# Υπολογίζουμε εδώ ώστε να είναι διαθέσιμο σε όλες τις σελίδες
# Σε production version: Transfermarkt API
# ============================================
df['estimated_value_M'] = (
    # Λεπτά συμμετοχής → max 50M (περισσότερα λεπτά = πιο πολύτιμος)
    (df['minutes'] / df['minutes'].max() * 50) +
    # Bonus νέων παικτών — κορυφή στα 24 χρόνια
    (10 - abs(df['age'] - 24) * 0.5).clip(0, 10) +
    # Bonus για παίκτες που σκοράρουν
    (df['goals_90'] * 20)
).round(1)

# Financial risk = αξία × πιθανότητα τραυματισμού
df['financial_risk_M'] = (
    df['estimated_value_M'] * df['risk_score'] / 100
).round(1)

# ============================================
# SIDEBAR
# Πλήρως custom HTML για τέλεια στοίχιση
# ============================================
with st.sidebar:

    # Logo — margin-top 2rem για ευθυγράμμιση με τους τίτλους
    st.markdown("""
    <div style="padding: 2rem 1.5rem 1.5rem 1.5rem;">
        <div style="
            font-size: 20px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.5px;
            line-height: 1.1;
        ">InjuryIQ</div>
        <div style="
            font-size: 9px;
            color: #374151;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            margin-top: 5px;
        ">Football Injury Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # Λεπτή γραμμή διαχωρισμού
    st.markdown(
        "<div style='height:1px; background:rgba(255,255,255,0.05); margin:0 1.5rem;'></div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # Navigation radio buttons
    # Το CSS παραπάνω κρύβει το label "nav" και στυλίζει τα buttons
    page = st.radio(
        "nav",
        ["Team Overview", "Player Search", "Financial Impact"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='height:1px; background:rgba(255,255,255,0.05); margin:0 1.5rem;'></div>",
        unsafe_allow_html=True
    )

    # Live stats — ανανεώνονται με κάθε φόρτωση
    high_risk_n = len(df[df['risk_level'] == 'High'])
    avg_risk_n = round(float(df['risk_score'].mean()), 1)

    st.markdown(f"""
    <div style="padding: 1.2rem 1.5rem;">
        <div style="font-size:9px; color:#374151; text-transform:uppercase; letter-spacing:2px; margin-bottom:14px;">
            Live Stats
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <span style="color:#9CA3AF; font-size:12px;">High Risk</span>
            <span style="color:#FF4444; font-size:12px; font-weight:700;">{high_risk_n}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <span style="color:#9CA3AF; font-size:12px;">Avg Risk Score</span>
            <span style="color:#FF9900; font-size:12px; font-weight:700;">{avg_risk_n}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#9CA3AF; font-size:12px;">Total Players</span>
            <span style="color:#00FF87; font-size:12px; font-weight:700;">{len(df)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='height:1px; background:rgba(255,255,255,0.05); margin:0 1.5rem;'></div>",
        unsafe_allow_html=True
    )

    # About section — πληροφορίες για το project
    st.markdown("""
    <div style="padding: 1.2rem 1.5rem;">
        <div style="font-size:9px; color:#374151; text-transform:uppercase; letter-spacing:2px; margin-bottom:14px;">
            About
        </div>
        <div style="margin-bottom:10px;">
            <div style="color:#4B5563; font-size:9px; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:3px;">Data</div>
            <div style="color:#9CA3AF; font-size:12px;">FBref · API-Football</div>
        </div>
        <div style="margin-bottom:10px;">
            <div style="color:#4B5563; font-size:9px; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:3px;">Model</div>
            <div style="color:#9CA3AF; font-size:12px;">XGBoost · 70.4% acc.</div>
        </div>
        <div>
            <div style="color:#4B5563; font-size:9px; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:3px;">Season</div>
            <div style="color:#9CA3AF; font-size:12px;">Premier League 23/24</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# HELPER — STYLED TABLE
# Επαναχρησιμοποιήσιμη συνάρτηση για dark πίνακα
# Χρησιμοποιείται και στις 3 σελίδες
# ============================================
def style_table(dataframe, risk_col='Risk Level', score_col=None):

    # Χρωματίζει το κελί του risk level ανάλογα με την τιμή
    def color_risk(val):
        if val == 'High':
            return 'background-color:#2D0F0F; color:#FF6B6B; font-weight:600;'
        elif val == 'Medium':
            return 'background-color:#2D1F0A; color:#FFB347; font-weight:600;'
        return 'background-color:#0A2D1A; color:#00FF87; font-weight:600;'

    # Χρωματίζει τον αριθμό του risk score
    def color_score(val):
        if val >= 70:
            return 'color:#FF6B6B; font-weight:700;'
        elif val >= 40:
            return 'color:#FFB347; font-weight:700;'
        return 'color:#00FF87; font-weight:700;'

    # Εφαρμόζουμε dark styling σε ολόκληρο τον πίνακα
    styled = dataframe.style.set_properties(**{
        'background-color': '#0D1120',
        'color': '#E5E7EB',
        'font-size': '13px',
        'padding': '10px 16px',
    }).set_table_styles([
        # Header row styling
        {'selector': 'th', 'props': [
            ('background-color', '#080C18'),
            ('color', '#00FF87'),
            ('font-size', '10px'),
            ('text-transform', 'uppercase'),
            ('letter-spacing', '1.5px'),
            ('padding', '12px 16px'),
            ('border-bottom', '1px solid rgba(0,255,135,0.12)'),
            ('font-weight', '700'),
        ]},
        # Data rows
        {'selector': 'td', 'props': [
            ('border-bottom', '1px solid rgba(255,255,255,0.03)'),
        ]},
        # Hover effect
        {'selector': 'tr:hover td', 'props': [
            ('background-color', '#111827 !important'),
        ]},
    ])

    # Εφαρμόζουμε χρωματισμό μόνο αν υπάρχουν οι στήλες
    if risk_col in dataframe.columns:
        styled = styled.map(color_risk, subset=[risk_col])
    if score_col and score_col in dataframe.columns:
        styled = styled.map(color_score, subset=[score_col])

    return styled

# ============================================
# ΣΕΛΙΔΑ 1: TEAM OVERVIEW
# ============================================
if page == "Team Overview":

    st.markdown("<h1>Team Overview</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6B7280; margin-bottom:28px;'>Premier League · Season 2023/24 · XGBoost ML</p>",
        unsafe_allow_html=True
    )

    # 4 metrics στην κορυφή
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        # Παίκτες με υψηλό κίνδυνο τραυματισμού
        st.metric("High Risk", len(df[df['risk_level'] == 'High']))
    with c2:
        # Παίκτες με μέτριο κίνδυνο
        st.metric("Medium Risk", len(df[df['risk_level'] == 'Medium']))
    with c3:
        # Μέσο risk score όλης της αποστολής
        st.metric("Avg Risk Score", f"{round(float(df['risk_score'].mean()), 1)}/100")
    with c4:
        # Σύνολο παικτών στο dataset
        st.metric("Total Players", len(df))

    st.markdown("---")

    # Δύο γραφήματα δίπλα δίπλα
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Risk Distribution")

        # Donut chart — κατανομή Low/Medium/High
        # Μετράμε πόσοι παίκτες ανήκουν σε κάθε κατηγορία
        risk_counts = df['risk_level'].value_counts()

        fig_donut = go.Figure(go.Pie(
            labels=risk_counts.index.tolist(),
            values=risk_counts.values.tolist(),
            hole=0.68,              # Μέγα τρύπα για donut effect
            marker=dict(
                colors=['#00FF87', '#FF9900', '#FF4444'],
                line=dict(color='#0A0E1A', width=3)  # Διαχωριστικές γραμμές
            ),
            textinfo='percent',     # Εμφανίζουμε μόνο ποσοστά
            textfont=dict(color='#FFFFFF', size=13),
            hovertemplate='<b>%{label}</b><br>%{value} players<extra></extra>'
        ))

        # Κείμενο στο κέντρο του donut
        fig_donut.add_annotation(
            text=f"<b>{len(df)}</b><br><span>Players</span>",
            x=0.5, y=0.5,
            font=dict(size=16, color='#FFFFFF'),
            showarrow=False
        )

        fig_donut.update_layout(
            plot_bgcolor='#0D1120',
            paper_bgcolor='#0D1120',
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='#D1D5DB', size=12),
                x=0.72, y=0.5,
                yanchor='middle'
            ),
            margin=dict(l=0, r=0, t=10, b=10),
            height=280
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        st.markdown("#### Risk Profile by Position")

        # Radar chart — κάθε θέση σε διαφορετικό άξονα
        # Δείχνει μέσο risk score ΚΑΙ % high risk ανά θέση
        positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
        avg_risks = []
        high_risk_pcts = []

        for pos in positions:
            pos_df = df[df['pos_simple'] == pos]
            if len(pos_df) > 0:
                # Μέσο risk score για αυτή τη θέση
                avg_risks.append(round(pos_df['risk_score'].mean(), 1))
                # Ποσοστό high risk παικτών σε αυτή τη θέση
                high_pct = round(
                    len(pos_df[pos_df['risk_level'] == 'High']) / len(pos_df) * 100, 1
                )
                high_risk_pcts.append(high_pct)
            else:
                avg_risks.append(0)
                high_risk_pcts.append(0)

        fig_radar = go.Figure()

        # Trace 1: Avg Risk Score — πράσινο
        fig_radar.add_trace(go.Scatterpolar(
            r=avg_risks + [avg_risks[0]],           # Κλείνουμε τον κύκλο
            theta=positions + [positions[0]],
            fill='toself',
            fillcolor='rgba(0, 255, 135, 0.1)',
            line=dict(color='#00FF87', width=2),
            name='Avg Risk Score',
            hovertemplate='<b>%{theta}</b><br>Avg Risk: %{r:.1f}<extra></extra>'
        ))

        # Trace 2: % High Risk Players — κόκκινο
        fig_radar.add_trace(go.Scatterpolar(
            r=high_risk_pcts + [high_risk_pcts[0]],
            theta=positions + [positions[0]],
            fill='toself',
            fillcolor='rgba(255, 68, 68, 0.1)',
            line=dict(color='#FF4444', width=2),
            name='% High Risk',
            hovertemplate='<b>%{theta}</b><br>High Risk: %{r:.1f}%<extra></extra>'
        ))

        fig_radar.update_layout(
            polar=dict(
                bgcolor='#111827',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color='#6B7280', size=10),
                    gridcolor='rgba(255,255,255,0.06)',
                    linecolor='rgba(255,255,255,0.06)',
                ),
                angularaxis=dict(
                    tickfont=dict(color='#D1D5DB', size=12),
                    linecolor='rgba(255,255,255,0.08)',
                    gridcolor='rgba(255,255,255,0.06)'
                )
            ),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='#D1D5DB', size=11),
                x=0.85, y=1.1
            ),
            paper_bgcolor='#0D1120',
            margin=dict(l=40, r=40, t=30, b=30),
            height=280
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # Gauge chart — μέσο risk score της αποστολής
    st.markdown("#### Squad Risk Gauge")

    avg_g = round(float(df['risk_score'].mean()), 1)
    # Χρώμα gauge ανάλογα με την τιμή
    gauge_color = '#00FF87' if avg_g < 40 else ('#FF9900' if avg_g < 70 else '#FF4444')

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_g,
        number={'font': {'size': 42, 'color': gauge_color}, 'suffix': '/100'},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': '#374151',
                'tickfont': {'color': '#9CA3AF', 'size': 10},
                'nticks': 6
            },
            'bar': {'color': gauge_color, 'thickness': 0.55},
            'bgcolor': '#111827',
            'borderwidth': 0,
            # Ζώνες χρωμάτων στο background
            'steps': [
                {'range': [0, 40], 'color': 'rgba(0,255,135,0.05)'},
                {'range': [40, 70], 'color': 'rgba(255,153,0,0.05)'},
                {'range': [70, 100], 'color': 'rgba(255,68,68,0.05)'}
            ],
            # Γραμμή κινδύνου στο 70
            'threshold': {
                'line': {'color': 'rgba(255,68,68,0.4)', 'width': 2},
                'thickness': 0.75,
                'value': 70
            }
        },
        title={'text': "Average Squad Injury Risk Score", 'font': {'color': '#9CA3AF', 'size': 12}}
    ))
    fig_gauge.update_layout(
        paper_bgcolor='#0D1120',
        height=230,
        margin=dict(l=60, r=60, t=50, b=10)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Player Risk Rankings")

    # Επιλέγουμε και μετονομάζουμε στήλες για καθαρότερη εμφάνιση
    df_display = df[['player', 'team', 'pos', 'age', 'minutes', 'risk_score', 'risk_level']].sort_values(
        'risk_score', ascending=False
    ).rename(columns={
        'player': 'Player', 'team': 'Team', 'pos': 'Position',
        'age': 'Age', 'minutes': 'Minutes',
        'risk_score': 'Risk Score', 'risk_level': 'Risk Level'
    })

    # height=420 = σταθερό ύψος με scroll μέσα στον πίνακα
    st.dataframe(
        style_table(df_display, risk_col='Risk Level', score_col='Risk Score'),
        use_container_width=True,
        hide_index=True,
        height=420
    )

# ============================================
# ΣΕΛΙΔΑ 2: PLAYER SEARCH
# ============================================
elif page == "Player Search":

    st.markdown("<h1>Player Search</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6B7280; margin-bottom:24px;'>Search any Premier League player — full injury risk profile</p>",
        unsafe_allow_html=True
    )

    # Dropdown με όλους τους παίκτες αλφαβητικά
    # Το label κρύβεται με CSS
    all_players = sorted(df['player'].unique().tolist())
    selected_player = st.selectbox("player", all_players, label_visibility="collapsed")

    # Φιλτράρουμε για τον επιλεγμένο παίκτη
    # .iloc[0] = παίρνουμε την πρώτη (μοναδική) γραμμή
    player_data = df[df['player'] == selected_player].iloc[0]
    risk = round(float(player_data['risk_score']), 1)

    # Καθορισμός επιπέδου και χρωμάτων ανάλογα με risk
    if risk >= 70:
        level, badge_color, bg_color, border_color = (
            "HIGH RISK", "#FF4444", "rgba(255,68,68,0.06)", "rgba(255,68,68,0.25)"
        )
    elif risk >= 40:
        level, badge_color, bg_color, border_color = (
            "MEDIUM RISK", "#FF9900", "rgba(255,153,0,0.06)", "rgba(255,153,0,0.25)"
        )
    else:
        level, badge_color, bg_color, border_color = (
            "LOW RISK", "#00FF87", "rgba(0,255,135,0.06)", "rgba(0,255,135,0.25)"
        )

    st.markdown("---")

    # Player header card — custom HTML για premium look
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0D1120 0%, #111827 100%);
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 3px solid {badge_color};
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
            <div>
                <div style="color:#FFFFFF; font-size:1.5rem; font-weight:800; letter-spacing:-0.3px; margin-bottom:6px;">
                    {selected_player}
                </div>
                <div style="color:#6B7280; font-size:13px;">
                    {player_data['team']} &nbsp;·&nbsp; {player_data['pos']} &nbsp;·&nbsp; Age {player_data['age']}
                </div>
            </div>
            <div style="background:{bg_color}; border:1px solid {border_color}; border-radius:12px; padding:14px 28px; text-align:center;">
                <div style="color:{badge_color}; font-size:32px; font-weight:800; line-height:1; letter-spacing:-1px;">{risk}</div>
                <div style="color:{badge_color}; font-size:9px; font-weight:700; letter-spacing:2.5px; margin-top:5px; opacity:0.8;">{level}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Δύο columns — stats αριστερά, gauge δεξιά
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("#### Player Stats")

        # Stats σε custom HTML rows για καθαρό look
        stats = [
            ("Minutes Played", str(player_data['minutes'])),
            ("Matches", str(player_data['matches'])),
            ("Predicted Days Out", f"{int(risk * 0.6)} days"),
            ("Yellow Cards", str(player_data['yellow_cards'])),
            ("Red Cards", str(player_data['red_cards'])),
            ("Goals per 90", f"{round(float(player_data['goals_90']), 2)}"),
            ("Assists per 90", f"{round(float(player_data['assists_90']), 2)}"),
        ]

        for label, value in stats:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.04);">
                <span style="color:#9CA3AF; font-size:13px;">{label}</span>
                <span style="color:#FFFFFF; font-size:13px; font-weight:600;">{value}</span>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown("#### Risk Gauge")

        # Gauge chart για τον συγκεκριμένο παίκτη
        fig_pg = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            number={'font': {'size': 38, 'color': badge_color}, 'suffix': '/100'},
            gauge={
                'axis': {
                    'range': [0, 100],
                    'tickwidth': 1,
                    'tickcolor': '#374151',
                    'tickfont': {'color': '#9CA3AF', 'size': 10},
                    'nticks': 6
                },
                'bar': {'color': badge_color, 'thickness': 0.6},
                'bgcolor': '#111827',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(0,255,135,0.05)'},
                    {'range': [40, 70], 'color': 'rgba(255,153,0,0.05)'},
                    {'range': [70, 100], 'color': 'rgba(255,68,68,0.05)'}
                ],
            },
            title={'text': "Injury Risk Score", 'font': {'color': '#9CA3AF', 'size': 12}}
        ))
        fig_pg.update_layout(
            paper_bgcolor='#0D1120',
            height=250,
            margin=dict(l=30, r=30, t=40, b=10)
        )
        st.plotly_chart(fig_pg, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Injury History")

    # Injury history — εμφανίζουμε ως badges
    if str(player_data['injury_types']) != 'None':
        injuries = str(player_data['injury_types']).split(', ')

        # Φτιάχνουμε badges σε μία γραμμή Python
        # Αποφεύγουμε multiline f-strings που εμφανίζονται ως κείμενο
        badges = " ".join([
            f'<span style="display:inline-block; background:rgba(255,68,68,0.08); '
            f'border:1px solid rgba(255,68,68,0.2); color:#FCA5A5; padding:5px 14px; '
            f'border-radius:20px; font-size:12px; margin:4px; font-weight:500;">{inj}</span>'
            for inj in injuries
        ])
        st.markdown(
            f'<div style="margin-top:8px; line-height:2.8;">{badges}</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("No injury history found for this player.")

# ============================================
# ΣΕΛΙΔΑ 3: FINANCIAL IMPACT
# ============================================
elif page == "Financial Impact":

    st.markdown("<h1>Financial Impact</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6B7280; margin-bottom:24px;'>Squad financial exposure · Estimated market values · Injury probability</p>",
        unsafe_allow_html=True
    )

    # Info box με εξήγηση μεθοδολογίας
    st.info(
        "**Financial Impact** = Estimated Market Value × (Risk Score / 100)  \n"
        "Estimates squad value at risk per player. "
        "Market values estimated from age, minutes & performance. "
        "Production version: Transfermarkt API."
    )

    # 3 metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        # Άθροισμα financial risk όλης της αποστολής
        st.metric("Total Squad Risk", f"€{df['financial_risk_M'].sum().round(1)}M")
    with c2:
        # Παίκτης με τον μεγαλύτερο οικονομικό κίνδυνο
        # idxmax() = βρίσκει τον index της μέγιστης τιμής
        st.metric("Most At Risk", df.loc[df['financial_risk_M'].idxmax(), 'player'])
    with c3:
        # Μέση εκτιμώμενη αξία παίκτη
        st.metric("Avg Player Value", f"€{df['estimated_value_M'].mean().round(1)}M")

    st.markdown("---")

    # ---- ΓΡΑΦΗΜΑ 1: Top 15 Financial Risk — Horizontal Bar ----
    # Καθαρό, ευανάγνωστο, δείχνει ποιοι παίκτες κοστίζουν περισσότερο
    st.markdown("#### Top 15 Players by Financial Risk")

    top15_chart = df.nlargest(15, 'financial_risk_M').sort_values('financial_risk_M', ascending=True)

    # Χρώμα ανά risk level
    bar_colors = ['#FF4444' if x == 'High' else ('#FF9900' if x == 'Medium' else '#00FF87')
                  for x in top15_chart['risk_level']]

    fig_fin_bar = go.Figure(go.Bar(
        y=top15_chart['player'],            # Παίκτες στον Y άξονα
        x=top15_chart['financial_risk_M'],  # Αξία στον X άξονα
        orientation='h',                    # Οριζόντιο bar chart
        marker=dict(color=bar_colors, opacity=0.82, line=dict(width=0)),
        # Εμφανίζουμε αξία δίπλα στη μπάρα
        text=[f"€{v}M" for v in top15_chart['financial_risk_M']],
        textposition='outside',
        textfont=dict(color='#D1D5DB', size=12),
        hovertemplate='<b>%{y}</b><br>Financial Risk: €%{x}M<extra></extra>'
    ))

    fig_fin_bar.update_layout(
        plot_bgcolor='#0D1120',
        paper_bgcolor='#0D1120',
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            color='#9CA3AF',
            zeroline=False,
            showline=False,
            title=dict(text='Financial Risk (€M)', font=dict(color='#9CA3AF', size=11))
        ),
        yaxis=dict(
            color='#E5E7EB',
            gridcolor='rgba(0,0,0,0)',
            showline=False,
            tickfont=dict(size=12, color='#E5E7EB')
        ),
        showlegend=False,
        height=460,
        margin=dict(l=20, r=80, t=10, b=20)
    )

    st.plotly_chart(fig_fin_bar, use_container_width=True)

    st.markdown("---")

    # ---- ΓΡΑΦΗΜΑ 2: Bubble Chart — Value vs Risk ----
    # x = estimated value, y = risk score
    # Μέγεθος φούσκας = financial risk (πόσο κοστίζει ο τραυματισμός)
    # Χρώμα = risk level
    # Έτσι βλέπεις ταυτόχρονα: αξία, κίνδυνος, οικονομική έκθεση
    st.markdown("#### Market Value vs Injury Risk")

    # Παίρνουμε top 40 πιο πολύτιμους — αποφεύγουμε chaos με όλους
    top40 = df.nlargest(40, 'estimated_value_M').copy()

    fig_bubble = px.scatter(
        top40,
        x='estimated_value_M',         # Χ άξονας = αξία παίκτη
        y='risk_score',                 # Y άξονας = risk score
        size='financial_risk_M',        # Μέγεθος φούσκας = financial risk
        color='risk_level',             # Χρώμα = risk level
        hover_name='player',            # Όνομα παίκτη στο hover
        hover_data={
            'team': True,
            'estimated_value_M': ':.1f',
            'risk_score': ':.1f',
            'financial_risk_M': ':.1f',
            'risk_level': False
        },
        labels={
            'estimated_value_M': 'Estimated Value (€M)',
            'risk_score': 'Injury Risk Score',
            'financial_risk_M': 'Financial Risk (€M)',
            'risk_level': 'Risk Level'
        },
        color_discrete_map={
            'Low': '#00FF87',
            'Medium': '#FF9900',
            'High': '#FF4444'
        },
        size_max=60,    # Μέγιστο μέγεθος φούσκας
        opacity=0.75
    )

    # Οριζόντια γραμμή κινδύνου στο risk score 70
    fig_bubble.add_hline(
        y=70,
        line_dash="dot",
        line_color="rgba(255,68,68,0.3)",
        line_width=1.5,
        annotation_text=" High Risk Threshold",
        annotation_position="right",
        annotation_font=dict(color="#FF6B6B", size=11)
    )

    # Λεπτό border στις φούσκες για καλύτερη εμφάνιση
    fig_bubble.update_traces(
        marker=dict(line=dict(width=1, color='rgba(255,255,255,0.1)'))
    )

    fig_bubble.update_layout(
        plot_bgcolor='#0D1120',
        paper_bgcolor='#0D1120',
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            color='#9CA3AF',
            zeroline=False,
            title_font=dict(color='#9CA3AF', size=11)
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            color='#9CA3AF',
            zeroline=False,
            title_font=dict(color='#9CA3AF', size=11),
            range=[0, 110]
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#D1D5DB', size=12),
            title=dict(text='Risk Level', font=dict(color='#9CA3AF', size=10)),
        ),
        height=420,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Full Rankings by Financial Risk")

    # Πίνακας top 15 με rename στήλων
    top15_table = df.nlargest(15, 'financial_risk_M')[
        ['player', 'team', 'age', 'risk_score', 'estimated_value_M', 'financial_risk_M', 'risk_level']
    ].reset_index(drop=True).rename(columns={
        'player': 'Player', 'team': 'Team', 'age': 'Age',
        'risk_score': 'Risk Score', 'estimated_value_M': 'Est. Value (€M)',
        'financial_risk_M': 'Financial Risk (€M)', 'risk_level': 'Risk Level'
    })

    # height=400 = σταθερό ύψος με scroll μέσα
    st.dataframe(
        style_table(top15_table, risk_col='Risk Level', score_col='Risk Score'),
        use_container_width=True,
        hide_index=True,
        height=400
    )