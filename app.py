import streamlit as st
import pandas as pd
import os
import re

# 1. Page Configuration
st.set_page_config(
    page_title="Nederlandse Werkwoorden Tool",
    page_icon="🇳🇱",
    layout="wide"
)

# --- THE CLEAN INTERFACE PROTOCOL (Hiding Streamlit UI) ---
# This CSS will target and remove the header, footer, and management buttons
st.markdown("""
    <style>
    /* Hide the top header bar (Share, Star, GitHub, Deploy) */
    header {visibility: hidden !important;}
    
    /* Hide the footer (Made with Streamlit) */
    footer {visibility: hidden !important;}
    
    /* Hide the 'Manage app' button at the bottom right */
    [data-testid="stStatusWidget"] {display: none !important;}
    .stAppDeployButton {display: none !important;}
    
    /* Remove any extra padding at the top */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Hide the 'Manage app' specifically for mobile/desktop */
    iframe[title="manage-app"] {display: none !important;}
    button[title="Manage app"] {display: none !important;}
    </style>
    
    <div style="display:none;">
        <title>Nederlandse Werkwoorden Tool - Osama Al-Aaraj</title>
        <meta name="description" content="Master Dutch verbs with Osama Al-Aaraj's professional tool.">
        <meta property="og:title" content="Nederlandse Werkwoorden Tool - Osama Al-Aaraj">
        <meta property="og:image" content="https://raw.githubusercontent.com/osamaalaarajj-dotcom/Dutch-Verb-Analyzer/main/preview_image.jpg">
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file = "0-KNM-A2_Tool4.xlsx"
    if os.path.exists(file):
        try:
            df = pd.read_excel(file, sheet_name="Blad2")
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            df['original_index'] = range(len(df))
            return df
        except:
            return None
    return None

data = load_data()

# 2. Sidebar Navigation
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar:", ["Over Ons", "Woordzoeker", "Tekst Analyse", "Juridische Informatie", "Contact"])

# --- SECTIONS ---
if page == "Over Ons":
    st.header("Over Ons")
    st.markdown("### Osama Abd Al-Nasser Al-Aaraj")
    st.write("**Geomatics Engineer | Master in Project Management**")
    st.info("'Mijn liefde voor het leren van alles zorgt ervoor dat ik niets afmaak.'")
    st.write("Ik presenteer u deze tool om u te helpen bij uw taalreis.")

elif page == "Woordzoeker":
    if data is not None:
        cols = data.columns
        st.title("Nederlandse Woordenschat")
        word_list = data.iloc[:, 0].astype(str).tolist()
        selected_word = st.selectbox(f"Zoek {cols[0]}:", options=[""] + word_list)

        if selected_word:
            result_row = data[data.iloc[:, 0] == selected_word].iloc[0]
            is_irregular = result_row['original_index'] <= 206
            color = "#ff4b4b" if is_irregular else "#28a745"
            st.markdown(f"<h2 style='color: {color};'>{'Onregelmatig' if is_irregular else 'Regelmatig'}: {selected_word}</h2>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**{cols[1]}**\n\n{result_row.iloc[1]}")
                st.info(f"**{cols[2]}**\n\n{result_row.iloc[2]}")
            with c2:
                st.success(f"**{cols[3]}**\n\n{result_row.iloc[3]}")
                st.success(f"**{cols[4]}**\n\n{result_row.iloc[4]}")

elif page == "Tekst Analyse":
    st.header("Tekst Analyse")
    text_area = st.text_area("Voer tekst in:", height=300)
    if st.button("Analyseer Tekst"):
        if text_area and data is not None:
            clean_text = re.sub(r'[^\w\s]', ' ', text_area)
            words = sorted(set([w.lower() for w in clean_text.split()]))
            irr_db = set(data[data['original_index'] <= 206].iloc[:, 0].str.lower())
            reg_db = set(data[data['original_index'] > 206].iloc[:, 0].str.lower())
            f_irr = [w for w in words if w in irr_db]
            f_reg = [w for w in words if w in reg_db]
            f_oth = [w for w in words if w not in irr_db and w not in reg_db]
            
            col1, col2, col3 = st.columns(3)
            with col1: st.error(f"🔴 Onregelmatig ({len(f_irr)})\n\n" + ", ".join(f_irr))
            with col2: st.success(f"🟢 Regelmatig ({len(f_reg)})\n\n" + ", ".join(f_reg))
            with col3: st.info(f"🔵 Overige ({len(f_oth)})\n\n" + ", ".join(f_oth))

elif page == "Juridische Informatie":
    st.header("Juridische Informatie")
    st.write("© 2026 Osama Abd Al-Nasser Al-Aaraj. Alle rechten voorbehouden.")

elif page == "Contact":
    st.header("Contactinformatie")
    st.success("📧 **Email:** osamaalaarajj@gmail.com")
