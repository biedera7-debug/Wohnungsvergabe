import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(
    page_title="Wohnungsvergabe Cockpit",
    page_icon="🏠",
    layout="wide"
)
st.set_page_config(page_title="Wohnungsvergabe Cockpit", page_icon="🏠", layout="wide")

# ---------------------------------------------------------
# HILFSFUNKTION: LEERE / STAMMDATEN ERSTELLEN
# ---------------------------------------------------------
def get_empty_data():
    """Erstellt leere Tabellen mit allen nötigen Spalten für die manuelle Eingabe."""
    df_w = pd.DataFrame({
        "Wohnungsnummer": ["Wohnung 1 EG Bestand", "Wohnung 2 1. OG"],
        "Zimmer": [3, 2],
        "Nutzfläche": [76.0, 49.32],
        "Max_Personen": [4, 2]
    })
    
    df_m = pd.DataFrame({
        "Mieter-ID": ["M01", "M02"],
        "Name": ["Familie Huber", "Anna Schmidt"],
        "Personenanzahl": [4, 2],
        "Empfehlung (Ja/Nein)": ["Ja", "Nein"],
        "Anmeldedatum": ["2026-01-02", "2026-01-01"],
        "1. Wahl": ["Wohnung 1 EG Bestand", "Wohnung 2 1. OG"],
        "2. Wahl": ["Wohnung 2 1. OG", ""],
        "3. Wahl": ["", ""],
        "4. Wahl": ["", ""]
    })
    return df_w, df_m

# ---------------------------------------------------------
# SIDEBAR: EINGABE-METHODE WÄHLEN
# ---------------------------------------------------------
st.sidebar.header("📁 1. Datenbasis")

input_mode = st.sidebar.radio(
    "Wie möchtest du die Daten eingeben?",
    ["Excel-Datei hochladen", "Manuell eingeben / Bearbeiten"]
)

if input_mode == "Excel-Datei hochladen":
    uploaded_file = st.sidebar.file_uploader("Excel-Datei hochladen (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        try:
            df_w = pd.read_excel(uploaded_file, sheet_name="Wohnungsdaten")
            df_m = pd.read_excel(uploaded_file, sheet_name="Mieterdaten")
            st.sidebar.success("Excel-Datei geladen!")
        except Exception as e:
            st.sidebar.error("Fehler beim Lesen. Beispiel-Daten geladen.")
            df_w, df_m = get_empty_data()
    else:
        df_w, df_m = get_empty_data()

else:  # Manuelle Eingabe im Browser
    st.sidebar.info("Bearbeite die Tabellen im Tab '📝 Manuelle Dateneingabe'.")
    if "df_w" not in st.session_state or "df_m" not in st.session_state:
        st.session_state.df_w, st.session_state.df_m = get_empty_data()
    df_w, df_m = st.session_state.df_w, st.session_state.df_m


# ---------------------------------------------------------
# NEUER TAB FÜR MANUELLE EINGABE (falls ausgewählt)
# ---------------------------------------------------------
if input_mode == "Manuell eingeben / Bearbeiten":
    st.header("📝 Manuelle Eingabe & Bearbeitung")
    st.caption("Füge neue Zeilen hinzu (+-Button unten in den Tabellen) oder klicke in eine Zelle, um Werte direkt zu ändern.")
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        st.subheader("🏢 Wohnungsdaten")
        df_w = st.data_editor(
            df_w,
            num_rows="dynamic",  # Erlaubt das Hinzufügen/Löschen von Zeilen
            use_container_width=True,
            key="editor_wohnungen"
        )
        st.session_state.df_w = df_w

    with col_e2:
        st.subheader("👥 Mieterdaten")
        df_m = st.data_editor(
            df_m,
            num_rows="dynamic",  # Erlaubt das Hinzufügen/Löschen von Zeilen
            use_container_width=True,
            key="editor_mieter"
        )
        st.session_state.df_m = df_m

    st.markdown("---")



# ---------------------------------------------------------
# HILFSFUNKTIONEN & ALGORITHMUS
# ---------------------------------------------------------

def load_default_data():
    """Erstellt Demo-Daten für Wohnungen und Mieter, falls keine Datei hochgeladen wird."""
    wohnungen = pd.DataFrame([
        {"Wohnungs-ID": f"W{i:02d}", "Adresse": f"Top {i:02d} - Hauptstraße", "Zimmer": (i % 4) + 1, "Max_Personen": (i % 4) + 1}
        for i in range(1, 11)
    ])
    
    mieter = pd.DataFrame([
        {"Mieter-ID": "M01", "Name": "Anna Schmidt", "Personen": 2, "Empfehlung": "Ja", "Anmeldedatum": "2026-01-02", "Wunsch_1": "W02", "Wunsch_2": "W01", "Wunsch_3": "W03"},
        {"Mieter-ID": "M02", "Name": "Markus Gruber", "Personen": 1, "Empfehlung": "Nein", "Anmeldedatum": "2026-01-01", "Wunsch_1": "W01", "Wunsch_2": "W02", "Wunsch_3": "W07"},
        {"Mieter-ID": "M03", "Name": "Familie Weber", "Personen": 4, "Empfehlung": "Ja", "Anmeldedatum": "2026-01-05", "Wunsch_1": "W04", "Wunsch_2": "W05", "Wunsch_3": "W06"},
        {"Mieter-ID": "M04", "Name": "Julia Steiner", "Personen": 1, "Empfehlung": "Ja", "Anmeldedatum": "2026-01-03", "Wunsch_1": "W01", "Wunsch_2": "W07", "Wunsch_3": "W02"},
        {"Mieter-ID": "M05", "Name": "David Wagner", "Personen": 3, "Empfehlung": "Nein", "Anmeldedatum": "2026-01-04", "Wunsch_1": "W03", "Wunsch_2": "W04", "Wunsch_3": "W05"},
        {"Mieter-ID": "M06", "Name": "Familie Huber", "Personen": 3, "Empfehlung": "Ja", "Anmeldedatum": "2026-01-08", "Wunsch_1": "W05", "Wunsch_2": "W04", "Wunsch_3": "W06"},
        {"Mieter-ID": "M07", "Name": "Stefan Pichler", "Personen": 2, "Empfehlung": "Nein", "Anmeldedatum": "2026-01-06", "Wunsch_1": "W02", "Wunsch_2": "W03", "Wunsch_3": "W08"},
        {"Mieter-ID": "M08", "Name": "Elena Berger", "Personen": 1, "Empfehlung": "Ja", "Anmeldedatum": "2026-01-07", "Wunsch_1": "W07", "Wunsch_2": "W01", "Wunsch_3": "W02"},
        {"Mieter-ID": "M09", "Name": "Familie Hofer", "Personen": 4, "Empfehlung": "Nein", "Anmeldedatum": "2026-01-09", "Wunsch_1": "W06", "Wunsch_2": "W05", "Wunsch_3": "W04"},
        {"Mieter-ID": "M10", "Name": "Martin Eder", "Personen": 2, "Empfehlung": "Ja", "Anmeldedatum": "2026-01-10", "Wunsch_1": "W03", "Wunsch_2": "W08", "Wunsch_3": "W02"},
    ])
    return wohnungen, mieter

def calculate_matching(df_w, df_m, w_empf, w_pass, w_anm, w_prio):
    """Berechnet die verfeinerte Zuordnung von Mietern zu Wohnungen basierend auf den Gewichtungen."""
    
    # Anmeldedatum normalisieren
    df_m['Anmeldedatum_dt'] = pd.to_datetime(df_m['Anmeldedatum'])
    min_date = df_m['Anmeldedatum_dt'].min()
    max_date = df_m['Anmeldedatum_dt'].max()
    date_range = (max_date - min_date).days if max_date != min_date else 1
    
    candidates = []
    
    # Für jede Kombination aus Mieter und dessen 3 Wunschwohnungen Punkte berechnen
    for _, m in df_m.iterrows():
        # Teil-Scores
        score_empf = 100 if str(m.get('Empfehlung', '')).strip().lower() in ['ja', 'true', '1'] else 0
        days_diff = (max_date - m['Anmeldedatum_dt']).days
        score_anm = (days_diff / date_range) * 100
        
        for p_rank, w_col in [(1, 'Wunsch_1'), (2, 'Wunsch_2'), (3, 'Wunsch_3')]:
            w_id = m.get(w_col)
            if pd.isna(w_id) or not w_id:
                continue
                
            w_row = df_w[df_w['Wohnungs-ID'] == w_id]
            if w_row.empty:
                continue
            w_info = w_row.iloc[0]
            
            # Passgenauigkeit (Optimal wenn Personenanzahl knapp unter/gleich Max_Personen)
            max_p = w_info.get('Max_Personen', 2)
            pers = m.get('Personen', 1)
            diff = abs(max_p - pers)
            score_pass = max(0, 100 - (diff * 30))
            
            # Prio Bonus
            score_prio = 100 if p_rank == 1 else (60 if p_rank == 2 else 30)
            
            # Gesamt-Score für diese Wohnung
            total_score = (
                (score_empf * w_empf) +
                (score_pass * w_pass) +
                (score_anm * w_anm) +
                (score_prio * w_prio)
            )
            
            candidates.append({
                'Mieter_ID': m['Mieter-ID'],
                'Name': m['Name'],
                'Wohnungs_ID': w_id,
                'Wunsch_Rang': p_rank,
                'Score': round(total_score, 1),
                'Score_Empf': score_empf,
                'Score_Pass': score_pass,
                'Score_Anm': round(score_anm, 1),
            })
            
    df_cand = pd.DataFrame(candidates)
    
    if df_cand.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    # Deferred Acceptance / Matching-Algorithmus
    df_cand_sorted = df_cand.sort_values(by=['Score', 'Wunsch_Rang'], ascending=[False, True])
    
    assigned_tenants = set()
    assigned_apartments = set()
    matches = []
    
    for _, row in df_cand_sorted.iterrows():
        m_id = row['Mieter_ID']
        w_id = row['Wohnungs_ID']
        
        if m_id not in assigned_tenants and w_id not in assigned_apartments:
            assigned_tenants.add(m_id)
            assigned_apartments.add(w_id)
            matches.append(row.to_dict())
            
    df_matches = pd.DataFrame(matches)
    return df_matches, df_cand

# ---------------------------------------------------------
# DASHBOARD UI
# ---------------------------------------------------------

st.title("🏠 Wohnungsvergabe – Szenario-Cockpit")
st.markdown("Vergleiche verschiedene Vergabekriterien und ordne Mietern optimal ihre Wunschwohnungen zu.")

# SIDEBAR: Datei & Szenario Steuerzeile
st.sidebar.header("📁 1. Datenbasis")
uploaded_file = st.sidebar.file_uploader("Excel-Datei hochladen (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_w = pd.read_excel(uploaded_file, sheet_name="Wohnungsdaten")
        df_m = pd.read_excel(uploaded_file, sheet_name="Mieterdaten")
        st.sidebar.success("Excel-Datei erfolgreich geladen!")
    except Exception as e:
        st.sidebar.error("Fehler beim Lesen der Sheets 'Wohnungsdaten' & 'Mieterdaten'. Beispieldaten werden geladen.")
        df_w, df_m = load_default_data()
else:
    st.sidebar.info("Demo-Daten geladen. Lade deine Excel hoch, um eigene Daten zu nutzen.")
    df_w, df_m = load_default_data()

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 2. Szenario-Gewichtung")

szenario_preset = st.sidebar.selectbox(
    "Vordefiniertes Szenario wählen:",
    ["Ausgewogen (Standard)", "Sozial & Bevorzugt", "Fairness / Schnelligkeit", "Maximale Auslastung", "Individuell"]
)

# Standard-Gewichtungen je nach Preset
if szenario_preset == "Sozial & Bevorzugt":
    w_e, w_p, w_a, w_r = 0.50, 0.20, 0.10, 0.20
elif szenario_preset == "Fairness / Schnelligkeit":
    w_e, w_p, w_a, w_r = 0.00, 0.20, 0.60, 0.20
elif szenario_preset == "Maximale Auslastung":
    w_e, w_p, w_a, w_r = 0.10, 0.60, 0.10, 0.20
else:  # Ausgewogen / Individuell
    w_e, w_p, w_a, w_r = 0.35, 0.30, 0.20, 0.15

st.sidebar.markdown("**Gewichtung der Kriterien (0.0 bis 1.0):**")
w_empf = st.sidebar.slider("1. Empfehlung bevorzugen", 0.0, 1.0, w_e, 0.05)
w_pass = st.sidebar.slider("2. Passgenauigkeit (Belegung)", 0.0, 1.0, w_p, 0.05)
w_anm = st.sidebar.slider("3. Frühe Anmeldung", 0.0, 1.0, w_a, 0.05)
w_prio = st.sidebar.slider("4. Erstwunsch-Bonus", 0.0, 1.0, w_r, 0.05)

# Normalisierung der Gewichtungen auf Summe = 1
total_w = w_empf + w_pass + w_anm + w_prio
if total_w > 0:
    w_empf, w_pass, w_anm, w_prio = w_empf/total_w, w_pass/total_w, w_anm/total_w, w_prio/total_w

# Berechne Matching
df_matches, df_cand = calculate_matching(df_w, df_m, w_empf, w_pass, w_anm, w_prio)

# KPI SPALTE OBEN
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.metric("Anzahl Wohnungen", len(df_w))
col_kpi2.metric("Anzahl Bewerber", len(df_m))
col_kpi3.metric("Vergebene Wohnungen", len(df_matches))
col_kpi4.metric("Offene Bewerber", len(df_m) - len(df_matches))

st.markdown("---")

# TABS FÜR UNTERSCHIEDLICHE ANSICHTEN
tab1, tab2, tab3 = st.tabs(["🏢 Wohnungs-Liste (Hauptansicht)", "📊 Szenario-Vergleich", "📄 Mieter-Gesamtübersicht"])

# ---------------------------------------------------------
# TAB 1: LISTE ALLER WOHNUNGEN MIT MIETERN
# ---------------------------------------------------------
with tab1:
    st.subheader(f"Ergebnis-Übersicht für Szenario: '{szenario_preset}'")
    st.caption("Hier siehst du jede Wohnung, wer sie erhalten hat und welche Alternativen es gab.")
    
    search_term = st.text_input("🔍 Wohnung suchen (nach ID oder Adresse):", "")
    
    for _, w in df_w.iterrows():
        w_id = w['Wohnungs-ID']
        w_adresse = w.get('Adresse', f'Wohnung {w_id}')
        
        if search_term and (search_term.lower() not in w_id.lower() and search_term.lower() not in w_adresse.lower()):
            continue
            
        # Match für diese Wohnung
        match_info = df_matches[df_matches['Wohnungs_ID'] == w_id] if not df_matches.empty else pd.DataFrame()
        
        with st.expander(f"🏠 **{w_id}** – {w_adresse} (Zimmer: {w.get('Zimmer', '-')}, Max. Pers: {w.get('Max_Personen', '-')})", expanded=True):
            if not match_info.empty:
                m_curr = match_info.iloc[0]
                col_m1, col_m2, col_m3, col_m4 = st.columns([3, 2, 2, 2])
                col_m1.markdown(f"✅ **Zugewiesener Mieter:** `{m_curr['Name']}` ({m_curr['Mieter_ID']})")
                col_m2.markdown(f"⭐ **Gesamt-Score:** `{m_curr['Score']} Pkt`")
                col_m3.markdown(f"🎯 **Wunsch-Rang:** `{m_curr['Wunsch_Rang']}. Wahl`")
                col_m4.markdown(f"👍 **Empfehlung:** `{'Ja' if m_curr['Score_Empf'] == 100 else 'Nein'}`")
            else:
                st.warning("⚠️ **Status:** Noch keine Vergabe / Keine passenden Interessenten.")
            
            # Zeige weitere Interessenten für diese Wohnung
            if not df_cand.empty:
                other_cands = df_cand[df_cand['Wohnungs_ID'] == w_id].sort_values(by='Score', ascending=False)
                if len(other_cands) > 1:
                    st.markdown("**Weitere Bewerber für diese Wohnung:**")
                    st.dataframe(
                        other_cands[['Name', 'Wunsch_Rang', 'Score', 'Score_Empf', 'Score_Pass', 'Score_Anm']]
                        .rename(columns={
                            'Wunsch_Rang': 'Wahl-Rang',
                            'Score_Empf': 'Empfehlung-Pkt',
                            'Score_Pass': 'Passform-Pkt',
                            'Score_Anm': 'Anmelde-Pkt'
                        }),
                        hide_index=True,
                        use_container_width=True
                    )

# ---------------------------------------------------------
# TAB 2: SZENARIO-VERGLEICH
# ---------------------------------------------------------
with tab2:
    st.subheader("🔄 Szenario-Vergleich (Veränderungen analysieren)")
    st.markdown("Vergleiche das aktuell eingestellte Szenario mit einem alternativen Szenario, um zu sehen, welche Mieter die Wohnung wechseln.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"**Szenario A (Aktuell):** `{szenario_preset}`")
    with col_s2:
        szenario_b = st.selectbox("Wähle Szenario B zum Vergleich:", ["Fairness / Schnelligkeit", "Sozial & Bevorzugt", "Maximale Auslastung"])
        
    # Berechne Szenario B
    if szenario_b == "Sozial & Bevorzugt":
        wb_e, wb_p, wb_a, wb_r = 0.50, 0.20, 0.10, 0.20
    elif szenario_b == "Fairness / Schnelligkeit":
        wb_e, wb_p, wb_a, wb_r = 0.00, 0.20, 0.60, 0.20
    else:
        wb_e, wb_p, wb_a, wb_r = 0.10, 0.60, 0.10, 0.20
        
    df_matches_b, _ = calculate_matching(df_w, df_m, wb_e, wb_p, wb_a, wb_r)
    
    # Tabelle zusammenstellen
    comparison = []
    for _, w in df_w.iterrows():
        w_id = w['Wohnungs-ID']
        mA = df_matches[df_matches['Wohnungs_ID'] == w_id]['Name'].values if not df_matches.empty else []
        mB = df_matches_b[df_matches_b['Wohnungs_ID'] == w_id]['Name'].values if not df_matches_b.empty else []
        
        nameA = mA[0] if len(mA) > 0 else "— Nicht vergeben —"
        nameB = mB[0] if len(mB) > 0 else "— Nicht vergeben —"
        
        comparison.append({
            "Wohnung": w_id,
            "Adresse": w.get('Adresse', ''),
            f"Mieter in Szenario A ({szenario_preset})": nameA,
            f"Mieter in Szenario B ({szenario_b})": nameB,
            "Veränderung": "🔴 Abweichend" if nameA != nameB else "🟢 Identisch"
        })
        
    df_comp = pd.DataFrame(comparison)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 3: MIETER GESAMTÜBERSICHT & EXPORT
# ---------------------------------------------------------
with tab3:
    st.subheader("📄 Vollständige Vergabe-Liste")
    
    if not df_matches.empty:
        # Merge mit Mieterdaten
        full_overview = pd.merge(df_m, df_matches[['Mieter_ID', 'Wohnungs_ID', 'Wunsch_Rang', 'Score']], left_on='Mieter-ID', right_on='Mieter_ID', how='left')
        full_overview['Status'] = full_overview['Wohnungs_ID'].apply(lambda x: "Zugewiesen" if pd.notna(x) else "Warteliste")
        
        st.dataframe(
            full_overview[['Mieter-ID', 'Name', 'Status', 'Wohnungs_ID', 'Wunsch_Rang', 'Score', 'Empfehlung', 'Anmeldedatum']],
            use_container_width=True,
            hide_index=True
        )
        
        # EXCEL DOWNLOAD
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            full_overview.to_excel(writer, sheet_name='Vergabe_Ergebnis', index=False)
            df_matches.to_excel(writer, sheet_name='Zuweisungen_Detail', index=False)
            
        st.download_button(
            label="📥 Vergabeliste als Excel herunterladen",
            data=buffer.getvalue(),
            file_name=f"Wohnungsvergabe_Ergebnis_{szenario_preset}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )