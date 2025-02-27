import pandas as pd
import plotly.express as px
import streamlit as st

#Titre
st.title("Analyse des ventes e-commerce")
st.markdown("Cette application permet d'explorer les données de ventes d'un site e-commerce")

#Section 1 : Omportation des données
uploaded_file = st.file_uploader("Importer un fichier CSV", type="csv")

if uploaded_file is None:
    st.warning('Veuillez importer un fichier pour continuer')
else:
    # Essayer UTF-8
    try:
        data = pd.read_csv(uploaded_file, encoding="utf-8")
    except UnicodeDecodeError:
        print("UTF-8 ne fonctionne pas, essayons Latin-1...")
        data = pd.read_csv(uploaded_file, encoding="ISO-8859-1") 
    st.write("Aperçu des données : ", data.head())

#Section 2 : Exploration des données
st.subheader("Exploration des données")
if uploaded_file is not None:
    if st.checkbox("Affciher les statistiques descriptives"):
        st.write(data.describe())

#Section 3 : Visualisation des données
st.subheader("Visualisation des données")
if uploaded_file is not None:
    column = st.selectbox("Sélectionner une colonne pour le graphique", data.columns)

    #Initialisation
    modification=0

    date_column = st.selectbox('Sélectionner la colonne qui correspond au date', data.columns)
    date = st.date_input("Choisissez un date")

    if date_column:
        data[date_column] = pd.to_datetime(data[date_column], errors="coerce").dt.date
        date = pd.to_datetime(date)

        if not data[date_column].isna().all():
            if date is not None:
                données_modifiées = data.loc[data[date_column] == date]
                modification += 1
            else:
                données_modifiées = data
        else:
            st.warning("⚠️ La colonne sélectionnée ne contient pas de dates valides.")
            données_modifiées = data

    if date and date_column:
        data[date_column] = pd.to_datetime(data[date_column])
        date = pd.to_datetime(date)
        données_modifiées = data.loc[data[date_column] == date]
    else:
        données_modifiées = data

    if st.button("Générer le graphique"):
            if not données_modifiées.empty:
                fig = px.bar(données_modifiées, x=column, title=f"Distribution de {column} pour {date}")
                st.plotly_chart(fig)
            else:
                st.warning('Aucune donnée trouvée pour cette date')

#Section 4 : Enregistrement des données
st.subheader("Téléchargement des données")
if uploaded_file is not None:
    if modification == 1:
        st.download_button("Télécharger avec la date sélectionnée", data.to_csv(index=False), "data_modifiées.csv")
    else:
        st.download_button("Télécharger les données initiale", data.to_csv(index=False), "data_modifiées.csv")
