import streamlit as st
import pandas as pd
import os
import re

# 1. Page Configuration
st.set_page_config(page_title="Nederlandse Werkwoorden Tool", layout="wide")

@st.cache_data
def load_data():
    file = "0-KNM-A2_Tool4.xlsx"
    if os.path.exists(file):
        try:
            df = pd.read_excel(file, sheet_name="Blad2")
            df['original_index'] = range(len(df))
            return df
        except:
            return None
    return None

data = load_data()

# 2. Sidebar Navigation
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar:", ["Over Ons", "Woordzoeker", "Tekst Analyse", "Juridische Informatie", "Contact"])

# --- SECTION 1: ABOUT THE DEVELOPER ---
if page == "Over Ons":
    st.header("Over Ons")
    st.markdown("### Osama Abd Al-Nasser Al-Aaraj")
    st.write("**Geomatics Engineer | Master in Project Management**")
    st.info("'Mijn liefde voor het leren van alles zorgt ervoor dat ik niets afmaak.'")
    st.write("Deze tool is ontwikkeld om de Nederlandse taalreis te vergemakkelijken.")

# --- SECTION 2: WORD SEARCH ---
elif page == "Woordzoeker":
    if data is not None:
        st.title("Woordzoeker")
        word_list = data.iloc[:, 0].astype(str).tolist()
        word = st.selectbox("Zoek Infinitive:", [""] + word_list)
        if word:
            row = data[data.iloc[:, 0] == word].iloc[0]
            is_irr = row['original_index'] <= 206
            color = "#ff4b4b" if is_irr else "#28a745"
            status = "Onregelmatig" if is_irr else "Regelmatig"
            
            st.markdown(f"<h2 style='color: {color};'>{status}: {word}</h2>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**Imperfectum:** {row.iloc[1]} / {row.iloc[2]}")
            with c2:
                st.success(f"**Voltooid Deelwoord:** {row.iloc[3]}")
            
            if len(data.columns) > 5 and pd.notna(row.iloc[5]):
                st.warning(f"**Extra Info:** {row.iloc[5]}")

# --- SECTION 3: TEXT ANALYSIS ---
elif page == "Tekst Analyse":
    st.header("Tekst Analyse")
    st.write("Plak uw tekst hieronder voor een volledige analyse.")
    text = st.text_area("Tekst invoeren:", height=300, key="main_text_area")
    
    if st.button("Analyseer Nu"):
        if text and data is not None:
            words = set(re.sub(r'[^\w\s]', ' ', text).lower().split())
            irr_db = set(data[data['original_index'] <= 206].iloc[:, 0].str.lower())
            reg_db = set(data[data['original_index'] > 206].iloc[:, 0].str.lower())
            
            f_irr = sorted([w for w in words if w in irr_db])
            f_reg = sorted([w for w in words if w in reg_db])
            f_oth = sorted([w for w in words if w not in irr_db and w not in reg_db])
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("<h3 style='color: #ff4b4b;'>Onregelmatig</h3>", unsafe_allow_html=True)
                st.error(", ".join(f_irr) if f_irr else "Geen gevonden")
            with c2:
                st.markdown("<h3 style='color: #28a745;'>Regelmatig</h3>", unsafe_allow_html=True)
                st.success(", ".join(f_reg) if f_reg else "Geen gevonden")
            with c3:
                st.markdown("<h3 style='color: #555555;'>Overige Woorden</h3>", unsafe_allow_html=True)
                st.info(", ".join(f_oth) if f_oth else "Geen")

# --- SECTION 4: LEGAL INFO ---
elif page == "Juridische Informatie":
    st.header("Juridische Informatie")
    st.write("© 2026 Osama Abd Al-Nasser Al-Aaraj. Alle rechten voorbehouden.")
    st.markdown("""
    - **Auteursrecht:** De database en code zijn intellectueel eigendom van de auteur.
    - **Licentie:** MIT License.
    """)

# --- SECTION 5: CONTACT ---
elif page == "Contact":
    st.header("Contactinformatie")
    st.write("Heeft u vragen of wilt u samenwerken? Neem contact op:")
    st.success("📧 **Email:** osamaalaarajj@gmail.com")
    st.info("🔗 **LinkedIn:** [Uw LinkedIn Profiel]")
    st.write("---")
    st.caption("Locatie: Nederland | Ontwikkeld in 2026")
