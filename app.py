# -------------------------------------------------------------------------
# PROJECT: Nederlandse Woordenschat & Werkwoorden Analyse
# AUTEUR: Osama Abd Al-Nasser Al-Aaraj
# LICENTIE: MIT License
# COPYRIGHT: © 2026 Osama Al-Aaraj. Alle rechten voorbehouden.
# -------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import os
import re

# 1. Pagina Configuratie
st.set_page_config(page_title="Nederlandse Werkwoorden Tool", layout="wide")

FILE_NAME = "0-KNM-A2_Tool4.xlsx"

@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME, sheet_name="Blad2")
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            df = df.drop_duplicates(subset=[df.columns[0]])
            df['original_index'] = range(len(df))
            return df
        except Exception as e:
            st.error(f"Fout bij het laden: {e}")
            return None
    return None

data = load_data()

# 2. Sidebar Navigatie
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar:", ["Over Ons", "Woordzoeker", "Tekst Analyse", "Juridische Informatie", "Contact"])

# --- SECTIE 1: OVER ONS ---
if page == "Over Ons":
    st.header("Over Ons")
    st.markdown("### Osama Abd Al-Nasser Al-Aaraj")
    st.write("**Geomatics Engineer | Master in Project Management**")
    st.info("'Mijn liefde voor het leren van alles zorgt ervoor dat ik niets afmaak.'")

# --- SECTIE 2: WOORDZOEKER (FIXED) ---
elif page == "Woordzoeker":
    if data is not None:
        cols = data.columns
        st.title("Nederlandse Woordenschat")
        word_list = data.iloc[:, 0].astype(str).tolist()
        selected_word = st.selectbox(f"Zoek {cols[0]}:", options=[""] + word_list, key="search_box")

        if selected_word:
            result_row = data[data.iloc[:, 0] == selected_word].iloc[0]
            is_irregular = result_row['original_index'] <= 206
            st.divider()
            
            color = "#ff4b4b" if is_irregular else "#28a745"
            status = "Onregelmatig" if is_irregular else "Regelmatig"
            st.markdown(f"<h2 style='color: {color};'>{status}: {selected_word}</h2>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                # Column 1 & 2
                val1 = result_row.iloc[1] if pd.notna(result_row.iloc[1]) else "-"
                val2 = result_row.iloc[2] if pd.notna(result_row.iloc[2]) else "-"
                if is_irregular:
                    st.error(f"**{cols[1]}**\n\n{val1}")
                    st.error(f"**{cols[2]}**\n\n{val2}")
                else:
                    st.info(f"**{cols[1]}**\n\n{val1}")
                    st.info(f"**{cols[2]}**\n\n{val2}")
            
            with c2:
                # Column 3 & 4
                val3 = result_row.iloc[3] if pd.notna(result_row.iloc[3]) else "-"
                val4 = result_row.iloc[4] if pd.notna(result_row.iloc[4]) else "-"
                st.success(f"**{cols[3]}**\n\n{val3}")
                st.success(f"**{cols[4]}**\n\n{val4}")

            if len(cols) > 5 and pd.notna(result_row.iloc[5]):
                st.warning(f"**{cols[5]}**\n\n{result_row.iloc[5]}")

# --- SECTIE 3: TEKST ANALYSE ---
elif page == "Tekst Analyse":
    st.header("Tekst Analyse")
    text_area = st.text_area("Voer tekst in:", height=300, key="txt_input")
    if st.button("Analyseer Tekst", key="btn_ana"):
        if text_area:
            clean_text = re.sub(r'[^\w\s]', ' ', text_area)
            words = sorted(set([w.lower() for w in clean_text.split()]))
            irr_db = set(data[data['original_index'] <= 206].iloc[:, 0].str.lower())
            reg_db = set(data[data['original_index'] > 206].iloc[:, 0].str.lower())
            
            f_irr = [w for w in words if w in irr_db]
            f_reg = [w for w in words if w in reg_db]
            f_oth = [w for w in words if w not in irr_db and w not in reg_db]
            
            col1, col2, col3 = st.columns(3)
            col1.error("Onregelmatig\n\n" + ", ".join(f_irr)) if f_irr else col1.write("Geen")
            col2.success("Regelmatig\n\n" + ", ".join(f_reg)) if f_reg else col2.write("Geen")
            col3.info("Overige\n\n" + ", ".join(f_oth)) if f_oth else col3.write("Geen")

# --- SECTIE 4 & 5: LEGAL & CONTACT ---
elif page == "Juridische Informatie":
    st.header("Juridische Informatie")
    st.write("© 2026 Osama Al-Aaraj. Alle rechten voorbehouden.")
elif page == "Contact":
    st.header("Contact")
    st.info("osamaalaarajj@gmail.com")
