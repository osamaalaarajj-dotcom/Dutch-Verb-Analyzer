# --- إخفاء GitHub و Manage App فقط ---
hide_style = """
<style>

/* إخفاء زر Github */
header a[href*="github"] {
    display: none !important;
}

/* إخفاء زر Manage app */
button[kind="header"] {
    display: none !important;
}

/* إخفاء Deploy */
.stAppDeployButton {
    display: none !important;
}

/* إخفاء الفوتر */
footer {
    visibility: hidden;
}

/* إبقاء القائمة الرئيسية */
#MainMenu {
    visibility: visible;
}

</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
