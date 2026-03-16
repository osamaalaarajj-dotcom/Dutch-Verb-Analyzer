import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="Nederlandse Tool", layout="wide")

@st.cache_data
def load_data():
    file = "0-KNM-A2_Tool4.xlsx"
    if os.path.exists(file):
        df = pd.read_excel(file, sheet_name="Blad2")
        df['original_index'] = range(len(df))
        return df
    return None

data = load_data()

st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar:", ["Over Ons", "Woordzoeker", "Tekst Analyse"])

if page == "Over Ons":
    st.header("Osama Abd Al-Nasser Al-Aaraj")
    st.write("Geomatics Engineer | Master in Project Management")

elif page == "Woordzoeker":
    if data is not None:
        word = st.selectbox("Zoek een woord:", [""] + data.iloc[:, 0].tolist())
        if word:
            row = data[data.iloc[:, 0] == word].iloc[0]
            is_irr = row['original_index'] <= 206
            color = "red" if is_irr else "green"
            st.subheader(f"Resultaat: {word}")
            st.write(f"Type: {('Onregelmatig' if is_irr else 'Regelmatig')}")
            st.write(row.iloc[1:5])

elif page == "Tekst Analyse":
    st.header("Tekst Analyse")
    text = st.text_area("Plak je tekst hier:", height=300)
    if st.button("Analyseer"):
        if text and data is not None:
            words = set(re.sub(r'[^\w\s]', ' ', text).lower().split())
            irr_list = set(data[data['original_index'] <= 206].iloc[:, 0].str.lower())
            reg_list = set(data[data['original_index'] > 206].iloc[:, 0].str.lower())
            
            f_irr = [w for w in words if w in irr_list]
            f_reg = [w for w in words if w in reg_list]
            f_oth = [w for w in words if w not in irr_list and w not in reg_list]
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.error("🔴 Onregelmatig")
                st.write(", ".join(f_irr) if f_irr else "Geen")
            with c2:
                st.success("🟢 Regelmatig")
                st.write(", ".join(f_reg) if f_reg else "Geen")
            with c3:
                st.info("🔵 Overige")
                st.write(", ".join(f_oth) if f_oth else "Geen")
