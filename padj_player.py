import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats



st.title('Visualisation pour le recrutement')

uploaded_file = st.sidebar.file_uploader("Choose a file")
pdi = []
if uploaded_file is not None:
    df = pd.read_excel(io=uploaded_file)
    df = df.fillna(0)
    name  = df["Équipe dans la période sélectionnée"].unique()
    new_df = pd.DataFrame(name,  columns =['Équipe dans la période sélectionnée'])
    new_df = new_df.sort_values(by="Équipe dans la période sélectionnée")
    new_df.reset_index(drop=True,inplace=True)
    new_df["Posession"]= "Unknow"
    df["PDI"]=0
    st.sidebar.title("Variable de sélection")
    test = []
    i= 0
    choice_variable = st.sidebar.multiselect("Variables",df.select_dtypes(["float","int"]).columns)
    st.header("Équipes")
    edited_df = st.experimental_data_editor(new_df)
    if "Unknow" not in edited_df["Posession"].values and len(choice_variable)>0:
        df = df.merge(edited_df, on='Équipe dans la période sélectionnée', how = "left")
        df["Posession"]= df["Posession"].astype(float)
        for variable in choice_variable:
            var = st.sidebar.slider(variable, 0, 100, 100)
            df[variable] = (df[variable] * 2 /(1 + np.exp(-0.1*(50-df["Posession"]))))
            df[variable] = stats.zscore(df[variable])
            #st.write(df[[variable,'Joueur']])
            df["PDI"] += df[variable]*(var/100)

        df = df.sort_values(by='PDI', ascending=False)
        df.reset_index(drop=True, inplace=True)
        st.header("Liste des joueurs")
        st.write(df[['Joueur', 'Équipe dans la période sélectionnée',"Place", "Âge","Valeur marchande","PDI"]].head(50))
