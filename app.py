import streamlit as st
import pandas as pd
import os
import re

# 1. Page Configuration
st.set_page_config(
    page_title="Nederlandse Werkwoorden Tool", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS to hide GitHub icon, Fork button, and Manage app button ---
st.markdown("""
    <style>
    /* Hide the entire top right toolbar except for the menu/theme if possible */
    header [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    
    /* Target specific GitHub and Fork links by their href or position */
    header a[href*="github.com"] {
        display: none !important;
    }
    
    /* Target the Deploy/Fork button specifically */
    .stAppDeployButton {
        display: none !important;
    }

    /* Hide the footer and the Manage app button at the bottom right */
    footer {
        display: none !important;
    }
    
    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* Additional layer to hide any developer-related icons in header */
    header svg {
        display: none !important;
    }
    
    /* Keep the sidebar toggle visible by specifically exempting its icon if needed */
    [data-testid="stSidebarCollapsedControl"] svg {
        display: block !important;
    }
    </style>
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

# 2. Sidebar Navigation (Word Search first)
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar:", ["Woordzoeker", "Tekst Analyse", "Over Ons", "Juridische Informatie", "Contact"])

# Sharing Section
st.sidebar.write("---")
st.sidebar.write("🔗 **Deel de website:**")
app_url = "https://dutch-verb-analyzer-uqtt8megnkusmtu5mwba6g.streamlit.app/"
st.sidebar.code(app_url, language=None)

# --- Page Logic ---

if page == "Woordzoeker":
    if data is not None:
        cols = data.columns
        st.title("Nederlandse Woordenschat")
        word_list = data.iloc[:, 0].astype(str).tolist()
        selected_word = st.selectbox(f"Zoek {cols[0]}:", options=[""] + word_list)

        if selected_word:
            result_row = data[data.iloc[:, 0] == selected_word].iloc[0]
            is_irregular = result_row['original_index'] <= 206
            color = "#ff4b4b" if is_irregular else "#28a745"
            status = "Onregelmatig" if is_irregular else "Regelmatig"
            st.markdown(f"<h2 style='color: {color};'>{status}: {selected_word}</h2>", unsafe_allow_html=True)

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
    if st.button("Analyseer"):
        if text_area and data is not None:
            clean_text = re.sub(r'[^\w\s]', ' ', text_area)
            words = sorted(set([w.lower() for w in clean_text.split()]))
            irr_db = set(data[data['original_index'] <= 206].iloc[:, 0].str.lower())
            reg_db = set(data[data['original_index'] > 206].iloc[:, 0].str.lower())
            f_irr = [w for w in words if w in irr_db]
            f_reg = [w for w in words if w in reg_db]
            f_oth = [w for w in words if w not in irr_db and w not in reg_db]
            
            col1, col2, col3 = st.columns(3)
            with col1: st.error(f"🔴 **Onregelmatig** ({len(f_irr)})\n\n" + ", ".join(f_irr))
            with col2: st.success(f"🟢 **Regelmatig** ({len(f_reg)})\n\n" + ", ".join(f_reg))
            with col3: st.info(f"🔵 **Overige** ({len(f_oth)})\n\n" + ", ".join(f_oth))

elif page == "Over Ons":
    st.header("Over Ons")
    st.markdown(f"### Osama Abd Al-Nasser Al-Aaraj")
    st.write("**Geomatics Engineer | Master in Project Management**")
    st.info("'Mijn liefde voor het leren van alles zorgt ervoor dat ik niets afmaak.'")

elif page == "Juridische Informatie":
    st.header("Juridische Informatie")
    st.write("© 2026 Osama Abd Al-Nasser Al-Aaraj. Alle rechten voorbehouden.")

elif page == "Contact":
    st.header("Contact informatie")
    st.success("📧 **Email:** osamaalaarajj@gmail.com")
