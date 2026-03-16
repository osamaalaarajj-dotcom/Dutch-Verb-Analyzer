# 🇳🇱 Nederlandse Werkwoorden & Woordenschat Analyzer
**Ontwikkeld door: Osama Abd Al-Nasser Al-Aaraj**

Dit project is een geavanceerde webapplicatie gebouwd met **Python** en **Streamlit**. Het is ontworpen om studenten van de Nederlandse taal te helpen bij het begrijpen, zoeken en analyseren van de Nederlandse woordenschat en werkwoorden.

---

## 🚀 Functionaliteiten

- **Woordzoeker:** Zoek direct in een uitgebreide database naar infinitieven, imperfectum (enkelvoud/meervoud) en voltooid deelwoorden.
- **Tekst Analyse (Pro):** Plak grote teksten (tot 1500+ woorden). De tool fragmenteert de tekst en categoriseert woorden automatisch in drie groepen:
  - 🔴 **Onregelmatig:** Werkwoorden uit de top 206 lijst.
  - 🟢 **Regelmatig:** Woorden die de standaardregels volgen.
  - 🔵 **Overige Woorden:** Alle andere woorden uit de tekst voor een volledig overzicht.
- **Kleurcodering:** Visuele feedback om het leerproces te versnellen.

---

## 🛠️ Installatie & Gebruik

Om deze applicatie lokaal te draaien, heb je Python nodig. 

1. Kloon deze repository.
2. Installeer de vereiste bibliotheken:
   ```bash
   pip install streamlit pandas openpyxl
