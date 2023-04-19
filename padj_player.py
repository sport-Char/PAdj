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
    name  = df["Team within selected timeframe"].unique()
    new_df = pd.DataFrame(name,  columns =['Team within selected timeframe'])
    new_df = new_df.sort_values(by="Team within selected timeframe")
    new_df.reset_index(drop=True,inplace=True)
    new_df["Posession"]= 50.00
    df["KPI"]=0
    df["Defense"] = df["PAdj Sliding tackles"] + df["PAdj Interceptions"]
    df["Jeu Long"] = df["Accurate long passes, %"]* df["Average long pass length, m"]
    age_max = st.sidebar.slider("Âge Max", 16, 40, 24)
    pos = []
    pos = df["Position"].tolist()
    pos = [p.split(", ") for p in pos]
    flat_list = [item for sublist in pos for item in sublist]
    unique_list_pos = list(set(flat_list))
    positions = st.sidebar.multiselect("Position voulue",unique_list_pos)
    st.sidebar.title("Choix de variable relative à un profil")
    test = []
    i= 0
    choice_var = st.sidebar.selectbox("Variables_Off",("Gardien","Défenseur central","WingBack","Milieu défensif","Milieu offensif","Ailier","Centre avant"))
    if choice_var == "Milieu défensif":
        choice_variable_off = ["Assists per 90","xA per 90","Second assists per 90","Accurate forward passes, %","Progressive runs per 90","Progressive passes per 90","Accurate passes to final third, %","Forward passes per 90","Passes to final third per 90","Shot assists per 90","Key passes per 90","Smart passes per 90","Through passes per 90","Passes to penalty area per 90"]
    elif choice_var=="Défenseur central":
        choice_variable_off = ["Defense","Defensive duels per 90","Jeu Long","Accurate forward passes, %","Aerial duels per 90","Progressive runs per 90","Third assists per 90"]
    elif choice_var == "Milieu offensif":
        choice_variable_off = ["PAdj Interceptions","Shots blocked per 90","Defensive duels per 90","Forward passes per 90","Accurate passes, %","Progressive runs per 90","Third assists per 90","Second assists per 90","PAdj Sliding tackles"]
    elif choice_var == "Gardien":
        choice_variable_off = ["Prevented goals per 90","Save rate, %","Exits per 90","Accurate long passes, %"]
    elif choice_var == "WingBack":
        choice_variable_off = ["Deep completed crosses per 90","Deep completions per 90","Passes to final third per 90","Defensive duels per 90","Defense","Aerial duels per 90","Accurate forward passes, %","xA per 90","Assists per 90","Shot assists per 90","Progressive runs per 90","Key passes per 90","Crosses per 90","Second assists per 90"]
    elif choice_var == "Centre avant":
        choice_var_off = []
    elif choice_var =="Ailier":
        choice_var_off= []
    else:
        choice_var_off=[]
    st.header("Équipes")
    edited_df = st.experimental_data_editor(new_df)
    if "Unknow" not in edited_df["Posession"].values and len(choice_variable_off)>0:
        age_mask = df["Age"] <= age_max
        pos_mask = df["Position"].apply(lambda x: any(pos in x for pos in positions))
        final_mask = age_mask & pos_mask
        df = df[final_mask]
        df = df.merge(edited_df, on='Team within selected timeframe', how = "left")
        df["Posession"]= df["Posession"].astype(float)
        st.sidebar.title("Influence de chaque parametre offensif")
        for variable in choice_variable_off:
            var = st.sidebar.slider(variable, 0, 100, 100)
            df[variable] = (df[variable] * 2 /(1 + np.exp(-0.1*(50-df["Posession"]))))
            df[variable] = stats.zscore(df[variable])
            #st.write(df[[variable,'Joueur']])
            df["KPI"] += df[variable]*(var/100)

        """if len(choice_variable_def)>0:
            st.sidebar.title("Influence de chaque parametre défensif")
            for variable_def in choice_variable_def:
                var = st.sidebar.slider(variable_def, 0, 100, 100)
                df[variable_def] = (df[variable_def] * 2 /(1 + np.exp(-0.1*(df["Posession"]-50))))
                df[variable_def] = stats.zscore(df[variable_def])
            #st.write(df[[variable,'Joueur']])
                df["KPI"] += df[variable_def]*(var/100)"""

        df = df.sort_values(by='KPI', ascending=False)
        df.reset_index(drop=True, inplace=True)
        st.header("Liste des joueurs")
        #st.write(df[['Player', 'Team within selected timeframe',"Minutes played","Position", "Age","Market value","Contract expires","Accurate forward passes, %","Accurate progressive passes, %","Accurate passes to final third, %","Key passes per 90","Accurate smart passes, %","Goals","xG","Passes per 90","Long passes per 90","Free kicks per 90","KPI"]].head(50))
        st.write(df[['Player', 'Team within selected timeframe',"Minutes played","Position", "Age","Market value","Contract expires","Accurate forward passes, %","Passes per 90","Long passes per 90","KPI"]])
