import streamlit as st
import pandas as pd
import os
import re

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Dutch Verbs Tool",
    page_icon="🇳🇱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Hide GitHub, Manage App, Deploy and Footer
# ---------------------------------------------------
hide_streamlit_style = """
<style>

/* Hide GitHub icon */
header a[href*="github"] {
    display: none !important;
}

/* Hide Manage App button */
button[kind="header"] {
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

/* Keep main menu visible */
#MainMenu {
    visibility: visible;
}

</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@st.cache_data
def load_data():
    file = "0-KNM-A2_Tool4.xlsx"
    if os.path.exists(file):
        try:
            df = pd.read_excel(file, sheet_name="Blad2")
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            df["original_index"] = range(len(df))
            return df
        except:
            return None
    return None

data = load_data()

# ---------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to:",
    [
        "Word Finder",
        "Text Analysis",
        "About",
        "Legal Information",
        "Contact"
    ]
)

# Share section
st.sidebar.write("---")
st.sidebar.write("🔗 Share this website:")

link = "https://dutch-verb-analyzer-uqtt8megnkusmtu5mwba6g.streamlit.app/"
st.sidebar.code(link)

# ---------------------------------------------------
# Word Finder Page
# ---------------------------------------------------
if page == "Word Finder":

    if data is not None:

        cols = data.columns

        st.title("Dutch Vocabulary Tool")

        word_list = data.iloc[:, 0].astype(str).tolist()

        selected_word = st.selectbox(
            f"Search {cols[0]}:",
            options=[""] + word_list
        )

        if selected_word:

            result_row = data[data.iloc[:, 0] == selected_word].iloc[0]

            is_irregular = result_row["original_index"] <= 206

            color = "#ff4b4b" if is_irregular else "#28a745"

            verb_type = "Irregular Verb" if is_irregular else "Regular Verb"

            st.markdown(
                f"<h2 style='color:{color};'>{verb_type}: {selected_word}</h2>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"**{cols[1]}**\n\n{result_row.iloc[1]}")
                st.info(f"**{cols[2]}**\n\n{result_row.iloc[2]}")

            with col2:
                st.success(f"**{cols[3]}**\n\n{result_row.iloc[3]}")
                st.success(f"**{cols[4]}**\n\n{result_row.iloc[4]}")

# ---------------------------------------------------
# Text Analysis Page
# ---------------------------------------------------
elif page == "Text Analysis":

    st.header("Text Analysis")

    text_area = st.text_area(
        "Paste your text here:",
        height=300
    )

    if st.button("Analyze Text"):

        if text_area and data is not None:

            clean_text = re.sub(r"[^\w\s]", " ", text_area)

            words = sorted(set([w.lower() for w in clean_text.split()]))

            irregular_db = set(
                data[data["original_index"] <= 206]
                .iloc[:, 0]
                .str.lower()
            )

            regular_db = set(
                data[data["original_index"] > 206]
                .iloc[:, 0]
                .str.lower()
            )

            found_irregular = [w for w in words if w in irregular_db]
            found_regular = [w for w in words if w in regular_db]
            found_other = [
                w for w in words
                if w not in irregular_db and w not in regular_db
            ]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.error(
                    f"🔴 Irregular ({len(found_irregular)})\n\n"
                    + ", ".join(found_irregular)
                )

            with col2:
                st.success(
                    f"🟢 Regular ({len(found_regular)})\n\n"
                    + ", ".join(found_regular)
                )

            with col3:
                st.info(
                    f"🔵 Other Words ({len(found_other)})\n\n"
                    + ", ".join(found_other)
                )

# ---------------------------------------------------
# About Page
# ---------------------------------------------------
elif page == "About":

    st.header("About")

    st.markdown("### Osama Abd Al-Nasser Al-Aaraj")

    st.write("Geomatics Engineer | Master in Project Management")

    st.info(
        "My love for learning everything sometimes means I finish nothing."
    )

# ---------------------------------------------------
# Legal Information
# ---------------------------------------------------
elif page == "Legal Information":

    st.header("Legal Information")

    st.write(
        "© 2026 Osama Abd Al-Nasser Al-Aaraj. All rights reserved."
    )

# ---------------------------------------------------
# Contact Page
# ---------------------------------------------------
elif page == "Contact":

    st.header("Contact Information")

    st.success(
        "📧 Email: osamaalaarajj@gmail.com"
    )
