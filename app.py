# -------------------------------------------------------------------------
# PROJECT: Nederlandse Woordenschat & Werkwoorden Analyse (Pro Version)
# AUTEUR: Osama Abd Al-Nasser Al-Aaraj
# LICENTIE: MIT License (Open-source voor persoonlijk gebruik)
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
            st.error(f"Fout bij het laden van het Excel-bestand: {e}")
            return None
    return None

data = load_data()

# 2. Sidebar Navigatie
st.sidebar.title("Navigatie")
page = st.sidebar.radio(
    "Ga naar:",
    ["Over Ons", "Woordzoeker", "Tekst Analyse", "Juridische Informatie", "Contact"]
)

# --- SECTIE 1: OVER ONS ---
if page == "Over Ons":
    st.header("Over Ons")
    st.markdown(f"""
    ### Osama Abd Al-Nasser Al-Aaraj
    **Geomatics Engineer | Master in Project Management**
    
    > "Mijn liefde voor het leren van alles zorgt ervoor dat ik niets afmaak."
    
    *Ik presenteer u deze tool om u te helpen bij uw taalreis.*
    """)

# --- SECTIE 2: WOORDZOEKER ---
elif page == "Woordzoeker":
    if data is not None:
        cols = data.columns
        st.title("Nederlandse Woordenschat")
        word_list = data.iloc[:, 0].astype(str).tolist()
        selected_word = st.selectbox(f"Zoek {cols[0]}:", options=[""] + word_list, key="main_search")

        if selected_word:
            result_row = data[data.iloc[:, 0] == selected_word].iloc[0]
            is_irregular = result_row['original_index'] <= 206
            st.divider()
            
            color = "#ff4b4b" if is_irregular else "#28a745"
            label = "Onregelmatig" if is_irregular else "Regelmatig"
            st.markdown(f"<h2 style='color: {color};'>{label}: {selected_word}</h2>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.error(f"**{cols[1]}**\n\n{result_row.iloc[1]}") if is_irregular else st.info(f"**{cols[1]}**\n\n{result_row.iloc[1]}")
                st.error(f"**{cols[2]}**\n\n{result_row.iloc[2]}") if is_irregular else st.info(f"**{cols[2]}**\n\n{result_row.iloc[2]}")
            with c2:
                st.success(f"**{cols[3]}**\n\n{result_row.iloc[3]}")
                st.success(f"**{cols[4]}**\n\n{result_row.iloc[4]}")
            
            if len(cols) > 5 and pd.notna(result_row.iloc[5]):
                st.warning(f"**{cols[5]}**\n\n{result_row.iloc[5]}")

# --- SECTIE 3: TEKST ANALYSE ---
elif page == "Tekst Analyse":
    st.header("Tekst Analyse")
    text_area = st.text_area("Voer tekst in:", height=400, placeholder="Plak uw tekst hier...", key="input_text")
    if st.button("Analyseer Tekst", key="analyze_btn"):
        if text_area and data is not None:
            clean_text = re.sub(r'[^\w\s]', ' ', text_area)
            words_in_text = [w.strip().lower() for w in clean_text.split() if w.strip()]
            unique_words = sorted(set(words_in_text))
            irr_db = set(data[data['original_index'] <= 206].iloc[:, 0].str.lower().tolist())
            reg_db = set(data[data['original_index'] > 206].iloc[:, 0].str.lower().tolist())
            found_irr = [w for w in unique_words if w in irr_db]
            found_reg = [w for w in unique_words if w in reg_db]
            others = [w for w in unique_words if w not in irr_db and w not in reg_db]
            
            col_irr, col_reg, col_other = st.columns(3)
            with col_irr:
                st.markdown("<h3 style='color: #ff4b4b;'>Onregelmatig</h3>", unsafe_allow_html=True)
                st.error(", ".join(found_irr)) if found_irr else st.write("Geen gevonden.")
            with col_reg:
                st.markdown("<h3 style='color: #28a745;'>Regelmatig</h3>", unsafe_allow_html=True)
                st.success(", ".join(found_reg)) if found_reg else st.write("Geen gevonden.")
            with col_other:
                st.markdown("<h3 style='color: #808080;'>Overige Woorden</h3>", unsafe_allow_html=True)
                st.info(", ".join(others)) if others else st.write("Geen gevonden.")

# --- SECTIE 4: JURIDISCHE INFORMATIE (القانونية) ---
elif page == "Juridische Informatie":
    st.header("Juridische Informatie & Licentie")
    st.markdown("""
    #### 1. Auteursrecht (Copyright)
    Alle rechten op deze software en de bijbehorende database zijn eigendom van **Osama Abd Al-Nasser Al-Aaraj**. 
    Het kopiëren, verspreiden of commercieel gebruiken van deze code zonder uitdrukkelijke toestemming is verboden.

    #### 2. Licentie (MIT License)
    Deze tool is gelicenseerd onder de MIT-licentie. Dit betekent dat de software wordt geleverd "zoals deze is" (AS IS), 
    zonder enige garantie van welke aard dan ook.

    #### 3. Beperking van Aansprakelijkheid
    De auteur is niet verantwoordelijk voor eventuele fouten in de vertalingen of voor schade die voortvloeit uit het gebruik van deze applicatie. 
    Gebruikers zijn verantwoordelijk voor het controleren van de nauwkeurigheid van de resultaten.
    """)

# --- SECTIE 5: CONTACT ---
elif page == "Contact":
    st.header("Contact")
    st.info("osamaalaarajj@gmail.com")
    st.write("---")
    st.caption("© 2026 Osama Al-Aaraj. Alle rechten voorbehouden.")
