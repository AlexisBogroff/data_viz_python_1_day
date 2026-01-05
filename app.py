import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Configuration de la page (Le "Look & Feel" pro)
st.set_page_config(page_title="Dashboard Étudiants 2026", layout="wide", page_icon="🎓")

# 2. Simulation de données (Similaire à ton TP, mais généré à la volée)
# Dans la vraie vie, on ferait un: df = pd.read_csv("data.csv")
@st.cache_data # Astuce 2026 : On cache les données pour que ça aille vite
def load_data():
    # Génération de fausses données pour l'exemple
    np.random.seed(42)
    n_rows = 100
    data = {
        'id_student': range(1, n_rows + 1),
        'grade': np.random.normal(12, 3, n_rows).clip(0, 20).round(1),
        'age': np.random.randint(18, 25, n_rows),
        'groupe': np.random.choice(['TD1', 'TD2', 'TD3'], n_rows),
        'assiduite': np.random.choice(['Haute', 'Moyenne', 'Basse'], n_rows)
    }
    return pd.DataFrame(data)

df = load_data()

# 3. La Sidebar (Le centre de contrôle)
st.sidebar.header("🎛️ Filtres")
selected_group = st.sidebar.multiselect("Filtrer par Groupe TD", options=df['groupe'].unique(), default=df['groupe'].unique())
age_range = st.sidebar.slider("Tranche d'âge", int(df['age'].min()), int(df['age'].max()), (18, 25))

# Filtrage des données
filtered_df = df[
    (df['groupe'].isin(selected_group)) & 
    (df['age'].between(age_range[0], age_range[1]))
]

# 4. Le Main Dashboard
st.title("🎓 Analyse des Résultats - Session 2026")
st.markdown("Ce dashboard interactif remplace les 15 graphiques statiques que nous faisions avant.")

# Les KPIs (Key Performance Indicators) en haut
col1, col2, col3 = st.columns(3)
col1.metric("Moyenne Générale", f"{filtered_df['grade'].mean():.2f}/20", delta_color="normal")
col2.metric("Meilleure Note", f"{filtered_df['grade'].max()}/20")
col3.metric("Nombre d'étudiants", len(filtered_df))

# 5. Les Graphiques (Plotly intégré nativement)
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Distribution des notes par assiduité")
    # On utilise Plotly Express comme dans ton cours, mais injecté dans Streamlit
    fig_scatter = px.scatter(
        filtered_df, 
        x="grade", 
        y="age", 
        color="assiduite", 
        size="grade", 
        hover_data=['id_student'],
        title="Note vs Age (Taille = Note)",
        template="plotly_dark" # Mode sombre moderne
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with c2:
    st.subheader("Moyenne par Groupe")
    avg_by_group = filtered_df.groupby('groupe')['grade'].mean().reset_index()
    fig_bar = px.bar(avg_by_group, x='groupe', y='grade', color='groupe', title="Moyenne par TD")
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. Afficher les données brutes (Optionnel avec un expander)
with st.expander("Voir les données brutes"):
    st.dataframe(filtered_df)

# 7. Section "IA Assistant" (Simulation pour ton cours)
st.divider()
st.subheader("🤖 L'analyse de l'IA (Simulation)")
st.info(f"L'IA détecte que le groupe **{avg_by_group.sort_values('grade').iloc[-1]['groupe']}** performe mieux que les autres. Une corrélation semble exister entre l'assiduité 'Haute' et les notes supérieures à 14.")