import streamlit as st
import pandas as pd
import os
import re

# 1. Page Configuration (Keep existing layout)
st.set_page_config(
    page_title="Nederlandse Werkwoorden Tool",
    page_icon="🇳🇱",
    layout="wide"
)

# --- THE CLEAN INTERFACE PROTOCOL (Targeted Hiding) ---
# This CSS will target ONLY the GitHub icon in the main header
st.markdown("""
    <style>
    /* 1. Target the GitHub link specifically and hide it */
    header a[href*="github.com"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 2. Target any developer-specific deploy/fork buttons in the main header */
    .stAppDeployButton {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Ensure other native top right buttons like full screen, menu, and light switch are NOT hidden */
    header [data-testid="stHeader"] .stException {
        display: none !important;
    }
    
    /* Target the Deploy button's parent container just in case, but keep the core menu dot */
    header button[kind="secondary"] {
        display: none !important;
    }
    
    /* Explicitly keep the native sidebar toggle */
    [data-testid="stSidebarCollapsedControl"] {
        display: block !important;
        visibility: visible !important;
    }

    /* Keep the original main menu (three dots) so options like print/theme settings remain */
    #MainMenu {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Remove 'Made with Streamlit' and 'Manage app' for a clean public look */
    footer {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }
    iframe[title="manage-app"] {
        display: none !important;
    }
    button[title="Manage app"] {
        display: none !important;
    }
    </style>
    
    <div style="display:none;">
        <title>Nederlandse Werkwoorden Tool - Osama Al-Aaraj</title>
        <meta name="description" content="Master Dutch verbs with Osama Al-Aaraj's professional tool. Built for students.">
        <meta property="og:title" content="Nederlandse Werkwoorden Tool - Osama Al-Aaraj">
        <meta property="og:image" content="https://raw.githubusercontent.com/osamaalaarajj-dotcom/Dutch-Verb-Analyzer/main/preview_image.jpg">
        <meta property="og:url" content="https://dutch-verb-analyzer-uqtt8megnkusmtu5mwba6g.streamlit.app/">
        <meta property="og:type" content="website">
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

# 2. Sidebar Navigation (Words Search first)
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar:", ["Woordzoeker", "Tekst Analyse", "Over Ons", "Juridische Informatie", "Contact"])

# Sharing Section in Sidebar (Native Share button remains active, this is extra)
st.sidebar.write("---")
st.sidebar.write("🔗 **Deel de website:**")
app_url = "https://dutch-verb-analyzer-uqtt8megnkusmtu5mwba6g.streamlit.app/"
st.sidebar.code(app_url, language=None)

# --- SECTIONS ---

# Search section (FIRST)
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

            if len(cols) > 5 and pd.notna(result_row.iloc[5]):
                st.warning(f"**{cols[5]}**\n\n{result_row.iloc[5]}")

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
    st.markdown("### Osama Abd Al-Nasser Al-Aaraj")
    st.write("**Geomatics Engineer | Master in Project Management**")
    st.info("'Mijn liefde voor het leren van alles zorgt ervoor dat ik niets afmaak.'")

elif page == "Juridische Informatie":
    st.header("Juridische Informatie")
    st.write("© 2026 Osama Abd Al-Nasser Al-Aaraj. Alle rechten voorbehouden.")

elif page == "Contact":
    st.header("Contact informatie")
    st.success("📧 **Email:** osamaalaarajj@gmail.com")
