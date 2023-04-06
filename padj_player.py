import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats



st.title('Joueurs avec ajustement selon la possession')

uploaded_file = st.sidebar.file_uploader("Choose a file")
pdi = []
if uploaded_file is not None:
    df = pd.read_excel(io=uploaded_file)
    df = df.fillna(0)
    name  = df["Équipe dans la période sélectionnée"].unique()
    new_df = pd.DataFrame(name,  columns =['Équipe dans la période sélectionnée'])
    new_df = new_df.sort_values(by="Équipe dans la période sélectionnée")
    new_df.reset_index(drop=True,inplace=True)
    new_df["Posession"]= 50.00
    df["PDI"]=0
    age_max = st.sidebar.slider("Âge Max", 16, 40, 24)
    pos = []
    pos = df["Place"].tolist()
    pos = [p.split(", ") for p in pos]
    flat_list = [item for sublist in pos for item in sublist]
    unique_list_pos = list(set(flat_list))
    positions = st.sidebar.multiselect("Position voulue",unique_list_pos)
    st.sidebar.title("Variable de sélection Offensive")
    test = []
    i= 0
    choice_variable_off = st.sidebar.multiselect("Variables_Off",df.select_dtypes(["float","int"]).columns)
    st.sidebar.title("Variable de sélection Défensive")
    choice_variable_def = st.sidebar.multiselect("Variables_Def",df.select_dtypes(["float","int"]).columns)
    st.header("Équipes")
    edited_df = st.experimental_data_editor(new_df)
    if "Unknow" not in edited_df["Posession"].values and len(choice_variable_off)>0:
        age_mask = df["Âge"] <= age_max
        pos_mask = df["Place"].apply(lambda x: any(pos in x for pos in positions))
        final_mask = age_mask & pos_mask
        df = df[final_mask]
        df = df.merge(edited_df, on='Équipe dans la période sélectionnée', how = "left")
        df["Posession"]= df["Posession"].astype(float)
        st.sidebar.title("Influence de chaque parametre offensif")
        for variable in choice_variable_off:
            var = st.sidebar.slider(variable, 0, 100, 100)
            df[variable] = (df[variable] * 2 /(1 + np.exp(-0.1*(50-df["Posession"]))))
            df[variable] = stats.zscore(df[variable])
            #st.write(df[[variable,'Joueur']])
            df["PDI"] += df[variable]*(var/100)

        if len(choice_variable_def)>0:
            st.sidebar.title("Influence de chaque parametre défensif")
            for variable_def in choice_variable_def:
                var = st.sidebar.slider(variable_def, 0, 100, 100)
                df[variable_def] = (df[variable_def] * 2 /(1 + np.exp(-0.1*(df["Posession"]-50))))
                df[variable_def] = stats.zscore(df[variable_def])
            #st.write(df[[variable,'Joueur']])
                df["PDI"] += df[variable_def]*(var/100)

        df = df.sort_values(by='PDI', ascending=False)
        df.reset_index(drop=True, inplace=True)
        st.header("Liste des joueurs")
        st.write(df[['Joueur', 'Équipe dans la période sélectionnée',"Place", "Âge","Valeur marchande","Tirs contre par 90","Buts concédés par 90","Buts concédés","xG contre par 90","xG contre","PDI"]].head(50))
