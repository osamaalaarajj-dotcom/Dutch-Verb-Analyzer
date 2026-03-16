import streamlit as st
import pandas as pd
import os
import re

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Nederlandse Werkwoorden Tool",
    page_icon="🇳🇱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Hide GitHub, Manage App and Deploy only
# ---------------------------------------------------
hide_streamlit_style = """
<style>

/* Hide GitHub icon */
header a[href*="github"] {
    display: none !important;
}

/* Hide Manage App */
a[href*="share.streamlit.io"] {
    display: none !important;
}

/* Hide Deploy button */
.stAppDeployButton {
    display: none !important;
}

/* Hide footer */
footer {
    visibility: hidden;
}

</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------------------------------
# Load Excel data
# ---------------------------------------------------
@st.cache_data
def load_data():

    file_path = "0-KNM-A2_Tool4.xlsx"

    if os.path.exists(file_path):

        try:
            df = pd.read_excel(file_path, sheet_name="Blad2")

            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

            df["original_index"] = range(len(df))

            return df

        except:
            return None

    return None


data = load_data()

# ---------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------
st.sidebar.title("Navigatie")

page = st.sidebar.radio(
    "Ga naar:",
    [
        "Woordzoeker",
        "Tekst Analyse",
        "Over Ons",
        "Juridische Informatie",
        "Contact"
    ]
)

# Share section
st.sidebar.write("---")
st.sidebar.write("🔗 **Deel de website:**")

website_link = "https://dutch-verb-analyzer-uqtt8megnkusmtu5mwba6g.streamlit.app/"
st.sidebar.code(website_link)

# ---------------------------------------------------
# Word Finder page
# ---------------------------------------------------
if page == "Woordzoeker":

    if data is not None:

        columns = data.columns

        st.title("Nederlandse Woordenschat")

        word_list = data.iloc[:, 0].astype(str).tolist()

        selected_word = st.selectbox(
            f"Zoek {columns[0]}:",
            options=[""] + word_list
        )

        if selected_word:

            result_row = data[data.iloc[:, 0] == selected_word].iloc[0]

            is_irregular = result_row["original_index"] <= 206

            color = "#ff4b4b" if is_irregular else "#28a745"

            verb_type = "Onregelmatig" if is_irregular else "Regelmatig"

            st.markdown(
                f"<h2 style='color:{color};'>{verb_type}: {selected_word}</h2>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"**{columns[1]}**\n\n{result_row.iloc[1]}")
                st.info(f"**{columns[2]}**\n\n{result_row.iloc[2]}")

            with col2:
                st.success(f"**{columns[3]}**\n\n{result_row.iloc[3]}")
                st.success(f"**{columns[4]}**\n\n{result_row.iloc[4]}")

# ---------------------------------------------------
# Text Analysis page
# ---------------------------------------------------
elif page == "Tekst Analyse":

    st.header("Tekst Analyse")

    text_input = st.text_area(
        "Plak je tekst hier:",
        height=300
    )

    if st.button("Analyseer"):

        if text_input and data is not None:

            clean_text = re.sub(r"[^\w\s]", " ", text_input)

            words = sorted(set([w.lower() for w in clean_text.split()]))

            irregular_database = set(
                data[data["original_index"] <= 206]
                .iloc[:, 0]
                .str.lower()
            )

            regular_database = set(
                data[data["original_index"] > 206]
                .iloc[:, 0]
                .str.lower()
            )

            found_irregular = [w for w in words if w in irregular_database]
            found_regular = [w for w in words if w in regular_database]

            found_other = [
                w for w in words
                if w not in irregular_database and w not in regular_database
            ]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.error(
                    f"🔴 Onregelmatig ({len(found_irregular)})\n\n"
                    + ", ".join(found_irregular)
                )

            with col2:
                st.success(
                    f"🟢 Regelmatig ({len(found_regular)})\n\n"
                    + ", ".join(found_regular)
                )

            with col3:
                st.info(
                    f"🔵 Overige ({len(found_other)})\n\n"
                    + ", ".join(found_other)
                )

# ---------------------------------------------------
# About page
# ---------------------------------------------------
elif page == "Over Ons":

    st.header("Over Ons")

    st.markdown("### Osama Abd Al-Nasser Al-Aaraj")

    st.write("Geomatics Engineer | Master in Project Management")

    st.info(
        "'Mijn liefde voor het leren van alles zorgt ervoor dat ik niets afmaak.'"
    )

# ---------------------------------------------------
# Legal page
# ---------------------------------------------------
elif page == "Juridische Informatie":

    st.header("Juridische Informatie")

    st.write(
        "© 2026 Osama Abd Al-Nasser Al-Aaraj. Alle rechten voorbehouden."
    )

# ---------------------------------------------------
# Contact page
# ---------------------------------------------------
elif page == "Contact":

    st.header("Contactinformatie")

    st.success(
        "📧 Email: osamaalaarajj@gmail.com"
    )
