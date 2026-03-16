import streamlit as st
import pandas as pd
import os
import re

# 1. إعدادات الصفحة - جعل البحث يفتح تلقائياً
st.set_page_config(
    page_title="Nederlandse Werkwoorden Tool",
    page_icon="🇳🇱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- كود CSS لإخفاء أزرار البرمجة فقط ---
st.markdown("""
    <style>
    /* 1. إخفاء زر Deploy وشعار GitHub في الأعلى */
    .stAppDeployButton {display: none !important;}
    header [data-testid="stHeader"] {background-color: transparent !important;}
    header a {display: none !important;}
    
    /* 2. إخفاء زر Manage app في الأسفل تماماً */
    [data-testid="stStatusWidget"] {display: none !important;}
    footer {display: none !important;}
    
    /* ملاحظة: لم نضف أي كود لإخفاء زر القائمة أو الإضاءة لضمان بقائهما */
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

# 2. القائمة الجانبية - صفحة البحث هي الخيار الأول
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar:", ["Woordzoeker", "Tekst Analyse", "Over Ons", "Juridische Informatie", "Contact"])

# إضافة رابط المشاركة في القائمة الجانبية
st.sidebar.write("---")
st.sidebar.write("🔗 **Deel de website:**")
app_url = "https://dutch-verb-analyzer-uqtt8megnkusmtu5mwba6g.streamlit.app/"
st.sidebar.code(app_url, language=None)

# --- محتوى الصفحات ---

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
    st.header("Contactinformatie")
    st.success("📧 **Email:** osamaalaarajj@gmail.com")
