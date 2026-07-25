import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(
    page_title="Wohnungsvergabe Cockpit",
    page_icon="🏠",
    layout="wide"
)

# ---------------------------------------------------------
# HILFSFUNKTIONEN & STANDARDS
# ---------------------------------------------------------

def get_default_data():
    """Erstellt Standard-Daten basierend auf den 50 Wohnungen aus der Tabelle."""
    df_w = pd.DataFrame([
        {"Wohnungsnummer": "Wohnung 1  EG Bestand", "Zimmer": 3, "Nutzfläche": 76.00, "Max_Personen": 4},
        {"Wohnungsnummer": "Wohnung 49 neu EG", "Zimmer": 2, "Nutzfläche": 43.56, "Max_Personen": 2},
        {"Wohnungsnummer": "Wohnung 50 neu EG", "Zimmer": 2, "Nutzfläche": 43.56, "Max_Personen": 2},
        {"Wohnungsnummer": "Wohnung 2 1. OG", "Zimmer": 2, "Nutzfläche": 49.32, "Max_Personen": 2},
        {"Wohnungsnummer": "Wohnung 3 1. OG", "Zimmer": 2, "Nutzfläche": 42.14, "Max_Personen": 2},
        {"Wohnungsnummer": "Wohnung 4 1. OG", "Zimmer": 2, "Nutzfläche": 47.46, "Max_Personen": 2},
        {"Wohnungsnummer": "Wohnung 7 1. OG", "Zimmer": 3, "Nutzfläche": 65.97, "Max_Personen": 4},
        {"Wohnungsnummer": "Wohnung 9 1. OG", "Zimmer": 3, "Nutzfläche": 64.92, "Max_Personen": 4},
        {"Wohnungsnummer": "Wohnung 11 1. OG", "Zimmer": 3, "Nutzfläche": 69.92, "Max_Personen": 4},
        {"Wohnungsnummer": "Wohnung 23 2. OG", "Zimmer": 3, "Nutzfläche": 65.97, "Max_Personen": 4},
        {"Wohnungsnummer": "Wohnung 27 2. OG", "Zimmer": 3, "Nutzfläche": 69.92, "Max_Personen": 4},
        {"Wohnungsnummer": "Wohnung 39 DG", "Zimmer": 3, "Nutzfläche": 62.16, "Max_Personen": 4},
        {"Wohnungsnummer": "Wohnung 43 DG", "Zimmer": 3, "Nutzfläche": 66.48, "Max_Personen": 4},
    ])
    
    df_m = pd.DataFrame([
        {
            "Mieter-ID": "M01", "Name": "Familie Huber", "Personenanzahl": 4, 
            "Empfehlung (Ja/Nein)": "Ja", "Anmeldedatum": "2026-01-02", 
            "1. Wahl": "Wohnung 7 1. OG", "2. Wahl": "Wohnung 9 1. OG", 
            "3. Wahl": "Wohnung 23 2. OG", "4. Wahl": "Wohnung 39 DG"
        },
        {
            "Mieter-ID": "M02", "Name": "Anna Schmidt", "Personenanzahl": 2, 
            "Empfehlung (Ja/Nein)": "Nein", "Anmeldedatum": "2026-01-01", 
            "1. Wahl": "Wohnung 2 1. OG", "2. Wahl": "Wohnung 3 1. OG", 
            "3. Wahl": "Wohnung 4 1. OG", "4. Wahl": ""
        },
        {
            "Mieter-ID": "M03", "Name": "Markus Gruber", "Personenanzahl": 1, 
            "Empfehlung (Ja/Nein)": "Ja", "Anmeldedatum": "2026-01-05", 
            "1. Wahl": "Wohnung 1  EG Bestand", "2. Wahl": "Wohnung 49 neu EG", 
            "3. Wahl": "Wohnung 50 neu EG", "4. Wahl": "Wohnung 2 1. OG"
        },
        {
            "Mieter-ID": "M04", "Name": "Familie Weber", "Personenanzahl": 3, 
            "Empfehlung (Ja/Nein)": "Ja", "Anmeldedatum": "2026-01-03", 
            "1. Wahl": "Wohnung 11 1. OG", "2. Wahl": "Wohnung 27 2. OG", 
            "3. Wahl": "Wohnung 43 DG", "4. Wahl": "Wohnung 7 1. OG"
        },
        {
            "Mieter-ID": "M05", "Name": "Julia Steiner", "Personenanzahl": 2, 
            "Empfehlung (Ja/Nein)": "Nein", "Anmeldedatum": "2026-01-04", 
            "1. Wahl": "Wohnung 49 neu EG", "2. Wahl": "Wohnung 50 neu EG", 
            "3. Wahl": "Wohnung 2 1. OG", "4. Wahl": "Wohnung 3 1. OG"
        }
    ])
    return df_w, df_m

def clean_column_names(df, df_type="wohnungen"):
    """Harmonisiert Spaltennamen für flexible Dateneingaben sehr robust."""
    if df.empty:
        return df
        
    df = df.copy()
    col_map = {}
    
    for col in df.columns:
        c_str = str(col).strip().lower()
        
        if df_type == "wohnungen":
            # Erkennt 'WOHNUNGSNUMMER', 'Wohnungs-ID', 'Wohnung', 'Top', 'ID'
            if any(k in c_str for k in ["wohnung", "nummer", "top", "id"]):
                col_map[col] = "Wohnungsnummer"
            elif "zimmer" in c_str:
                col_map[col] = "Zimmer"
            elif "max" in c_str or "person" in c_str:
                col_map[col] = "Max_Personen"
                
        elif df_type == "mieter":
            if "mieter" in c_str and "id" in c_str:
                col_map[col] = "Mieter-ID"
            elif "name" in c_str:
                col_map[col] = "Name"
            elif "person" in c_str:
                col_map[col] = "Personenanzahl"
            elif "empfehl" in c_str:
                col_map[col] = "Empfehlung (Ja/Nein)"
            elif "anmeld" in c_str or "datum" in c_str:
                col_map[col] = "Anmeldedatum"
            elif "1" in c_str and "wahl" in c_str:
                col_map[col] = "1. Wahl"
            elif "2" in c_str and "wahl" in c_str:
                col_map[col] = "2. Wahl"
            elif "3" in c_str and "wahl" in c_str:
                col_map[col] = "3. Wahl"
            elif "4" in c_str and "wahl" in c_str:
                col_map[col] = "4. Wahl"
                
    df_renamed = df.rename(columns=col_map)
    
    # Fallback: Falls 'Wohnungsnummer' noch nicht existiert, nimm die erste Spalte
    if df_type == "wohnungen" and "Wohnungsnummer" not in df_renamed.columns and len(df_renamed.columns) > 0:
        first_col = df_renamed.columns[0]
        df_renamed = df_renamed.rename(columns={first_col: "Wohnungsnummer"})
        
    return df_renamed

def calculate_matching(df_w, df_m, w_empf, w_pass, w_anm, w_prio):
    """Berechnet die Zuordnung von Mietern zu Wohnungen basierend auf den Szenario-Faktoren."""
    if df_w.empty or df_m.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    df_w_clean = clean_column_names(df_w, "wohnungen")
    df_m_clean = clean_column_names(df_m, "mieter")
    
    if "Wohnungsnummer" not in df_w_clean.columns:
        return pd.DataFrame(), pd.DataFrame()
    
    # Anmeldedatum parsen
    if 'Anmeldedatum' in df_m_clean.columns:
        df_m_clean['Anmeldedatum_dt'] = pd.to_datetime(df_m_clean['Anmeldedatum'], errors='coerce')
    else:
        df_m_clean['Anmeldedatum_dt'] = pd.Timestamp('2026-01-01')
        
    min_date = df_m_clean['Anmeldedatum_dt'].min()
    max_date = df_m_clean['Anmeldedatum_dt'].max()
    date_range = (max_date - min_date).days if pd.notna(max_date) and pd.notna(min_date) and max_date != min_date else 1
    
    candidates = []
    
    # Präferenzen auswerten (1. bis 4. Wahl)
    pref_cols = [c for c in ['1. Wahl', '2. Wahl', '3. Wahl', '4. Wahl'] if c in df_m_clean.columns]
    
    for idx, m in df_m_clean.iterrows():
        m_id = m.get('Mieter-ID', f"M{idx+1:02d}")
        m_name = m.get('Name', f"Bewerber {idx+1}")
        
        # Empfehlungs-Score
        empf_val = str(m.get('Empfehlung (Ja/Nein)', '')).strip().lower()
        score_empf = 100 if empf_val in ['ja', 'true', '1'] else 0
        
        # Anmelde-Score
        if pd.notna(m['Anmeldedatum_dt']):
            days_diff = (max_date - m['Anmeldedatum_dt']).days
            score_anm = (days_diff / date_range) * 100
        else:
            score_anm = 50
            
        for rank_idx, p_col in enumerate(pref_cols, start=1):
            w_id = m.get(p_col)
            if pd.isna(w_id) or not str(w_id).strip():
                continue
                
            w_id_str = str(w_id).strip()
            
            # Suche nach passender Wohnung
            w_match = df_w_clean[df_w_clean['Wohnungsnummer'].astype(str).str.strip() == w_id_str]
            if w_match.empty:
                continue
            w_info = w_match.iloc[0]
            
            # Passform
            max_p = w_info.get('Max_Personen', w_info.get('Zimmer', 2))
            try:
                pers = float(m.get('Personenanzahl', 1))
            except (ValueError, TypeError):
                pers = 1.0
                
            diff = abs(float(max_p) - pers)
            score_pass = max(0, 100 - (diff * 30))
            
            # Prioritäts-Bonus
            score_prio = 100 if rank_idx == 1 else (75 if rank_idx == 2 else (50 if rank_idx == 3 else 25))
            
            # Gesamter gewichteter Score
            total_score = (
                (score_empf * w_empf) +
                (score_pass * w_pass) +
                (score_anm * w_anm) +
                (score_prio * w_prio)
            )
            
            candidates.append({
                'Mieter_ID': m_id,
                'Name': m_name,
                'Wohnungs_ID': w_id_str,
                'Wunsch_Rang': rank_idx,
                'Score': round(total_score, 1),
                'Score_Empf': score_empf,
                'Score_Pass': score_pass,
                'Score_Anm': round(score_anm, 1),
            })
            
    df_cand = pd.DataFrame(candidates)
    if df_cand.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    # Zuordnung (Deferred Acceptance / Maximum Score Matching)
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
# SESSION STATE INITIALISIERUNG
# ---------------------------------------------------------
if "df_w" not in st.session_state or "df_m" not in st.session_state:
    st.session_state.df_w, st.session_state.df_m = get_default_data()

# ---------------------------------------------------------
# GUI & LAYOUT
# ---------------------------------------------------------

st.title("🏠 Wohnungsvergabe – Interaktives Szenario-Cockpit")
st.markdown("Vergleiche Kriterien, verwalte Wohnungen & Mieter und simuliere die optimale Vergabe.")

# SIDEBAR: DATEN-QUELLE (MANUELLE EINGABE AN ERSTER STELLE)
st.sidebar.header("📁 1. Datenbasis")

input_mode = st.sidebar.radio(
    "Datenquelle wählen:",
    ["Manuell eingeben / In der App bearbeiten", "Excel-Datei hochladen"],
    index=0
)

if input_mode == "Excel-Datei hochladen":
    uploaded_file = st.sidebar.file_uploader(
        "Excel-Datei hochladen (.xlsx)", 
        type=["xlsx"], 
        key="excel_uploader_sidebar"
    )
    if uploaded_file is not None:
        try:
            st.session_state.df_w = pd.read_excel(uploaded_file, sheet_name="Wohnungsdaten")
            st.session_state.df_m = pd.read_excel(uploaded_file, sheet_name="Mieterdaten")
            st.sidebar.success("Excel-Datei erfolgreich geladen!")
        except Exception as e:
            st.sidebar.error("Fehler beim Lesen der Sheets 'Wohnungsdaten' & 'Mieterdaten'.")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 2. Szenario-Gewichtung")

szenario_preset = st.sidebar.selectbox(
    "Vordefiniertes Szenario wählen:",
    ["Ausgewogen (Standard)", "Sozial & Bevorzugt", "Fairness / Schnelligkeit", "Maximale Auslastung", "Individuell"]
)

if szenario_preset == "Sozial & Bevorzugt":
    w_e, w_p, w_a, w_r = 0.50, 0.20, 0.10, 0.20
elif szenario_preset == "Fairness / Schnelligkeit":
    w_e, w_p, w_a, w_r = 0.00, 0.20, 0.60, 0.20
elif szenario_preset == "Maximale Auslastung":
    w_e, w_p, w_a, w_r = 0.10, 0.60, 0.10, 0.20
else:
    w_e, w_p, w_a, w_r = 0.35, 0.30, 0.20, 0.15

st.sidebar.markdown("**Gewichtung der Kriterien (0.0 bis 1.0):**")
w_empf = st.sidebar.slider("1. Empfehlung bevorzugen", 0.0, 1.0, w_e, 0.05)
w_pass = st.sidebar.slider("2. Passgenauigkeit (Belegung)", 0.0, 1.0, w_p, 0.05)
w_anm = st.sidebar.slider("3. Frühe Anmeldung", 0.0, 1.0, w_a, 0.05)
w_prio = st.sidebar.slider("4. Erstwunsch-Bonus", 0.0, 1.0, w_r, 0.05)

# Normalisieren
total_w = w_empf + w_pass + w_anm + w_prio
if total_w > 0:
    w_empf, w_pass, w_anm, w_prio = w_empf/total_w, w_pass/total_w, w_anm/total_w, w_prio/total_w

# BERECHNUNG MIT AKTUELLEN SESSION-DATEN
df_w_active = st.session_state.df_w
df_m_active = st.session_state.df_m

df_matches, df_cand = calculate_matching(df_w_active, df_m_active, w_empf, w_pass, w_anm, w_prio)

# KPI SPALTE
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.metric("Anzahl Wohnungen", len(df_w_active))
col_kpi2.metric("Anzahl Bewerber", len(df_m_active))
col_kpi3.metric("Vergebene Wohnungen", len(df_matches))
col_kpi4.metric("Offene Bewerber", max(0, len(df_m_active) - len(df_matches)))

st.markdown("---")

# TABS FÜR ANSICHTEN
tab1, tab2, tab3, tab4 = st.tabs([
    "🏢 Wohnungs-Liste (Hauptansicht)", 
    "📝 Dateneingabe / Bearbeiten", 
    "📊 Szenario-Vergleich", 
    "📄 Mieter-Gesamtübersicht & Export"
])

# ---------------------------------------------------------
# TAB 1: HAUPTANSICHT
# ---------------------------------------------------------
with tab1:
    st.subheader(f"Ergebnis-Übersicht für Szenario: '{szenario_preset}'")
    st.caption("Hier siehst du jede Wohnung, wer sie erhalten hat und welche Alternativen es gab.")
    
    search_term = st.text_input("🔍 Wohnung suchen (nach ID / Name):", "")
    
    df_w_clean = clean_column_names(df_w_active, "wohnungen")
    
    for _, w in df_w_clean.iterrows():
        w_id = str(w.get('Wohnungsnummer', 'Unbekannt')).strip()
        
        if search_term and search_term.lower() not in w_id.lower():
            continue
            
        match_info = df_matches[df_matches['Wohnungs_ID'] == w_id] if not df_matches.empty else pd.DataFrame()
        
        with st.expander(f"🏠 **{w_id}** (Zimmer: {w.get('Zimmer', '-')})", expanded=True):
            if not match_info.empty:
                m_curr = match_info.iloc[0]
                col_m1, col_m2, col_m3, col_m4 = st.columns([3, 2, 2, 2])
                col_m1.markdown(f"✅ **Zugewiesener Mieter:** `{m_curr['Name']}` ({m_curr['Mieter_ID']})")
                col_m2.markdown(f"⭐ **Gesamt-Score:** `{m_curr['Score']} Pkt`")
                col_m3.markdown(f"🎯 **Wunsch-Rang:** `{m_curr['Wunsch_Rang']}. Wahl`")
                col_m4.markdown(f"👍 **Empfehlung:** `{'Ja' if m_curr['Score_Empf'] == 100 else 'Nein'}`")
            else:
                st.warning("⚠️ **Status:** Noch keine Vergabe / Keine passenden Interessenten.")
            
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
# TAB 2: DATENEINGABE / BEARBEITEN
# ---------------------------------------------------------
with tab2:
    st.subheader("📝 Daten direkt in der App bearbeiten")
    st.caption("Ändere Werte direkt in den Zellen oder füge unten über das '+'-Symbol neue Reihen hinzu.")
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        st.markdown("### 🏢 Wohnungsdaten")
        edited_w = st.data_editor(
            st.session_state.df_w,
            num_rows="dynamic",
            use_container_width=True,
            key="editor_wohnungsdaten"
        )
        st.session_state.df_w = edited_w

    with col_e2:
        st.markdown("### 👥 Mieterdaten")
        edited_m = st.data_editor(
            st.session_state.df_m,
            num_rows="dynamic",
            use_container_width=True,
            key="editor_mieterdaten"
        )
        st.session_state.df_m = edited_m

# ---------------------------------------------------------
# TAB 3: SZENARIO-VERGLEICH
# ---------------------------------------------------------
with tab3:
    st.subheader("🔄 Szenario-Vergleich (Gegenüberstellung)")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"**Szenario A (Aktuell):** `{szenario_preset}`")
    with col_s2:
        szenario_b = st.selectbox("Wähle Szenario B zum Vergleich:", ["Fairness / Schnelligkeit", "Sozial & Bevorzugt", "Maximale Auslastung"])
        
    if szenario_b == "Sozial & Bevorzugt":
        wb_e, wb_p, wb_a, wb_r = 0.50, 0.20, 0.10, 0.20
    elif szenario_b == "Fairness / Schnelligkeit":
        wb_e, wb_p, wb_a, wb_r = 0.00, 0.20, 0.60, 0.20
    else:
        wb_e, wb_p, wb_a, wb_r = 0.10, 0.60, 0.10, 0.20
        
    df_matches_b, _ = calculate_matching(df_w_active, df_m_active, wb_e, wb_p, wb_a, wb_r)
    
    comparison = []
    df_w_clean = clean_column_names(df_w_active, "wohnungen")
    
    for _, w in df_w_clean.iterrows():
        w_id = str(w.get('Wohnungsnummer', 'Unbekannt')).strip()
        mA = df_matches[df_matches['Wohnungs_ID'] == w_id]['Name'].values if not df_matches.empty else []
        mB = df_matches_b[df_matches_b['Wohnungs_ID'] == w_id]['Name'].values if not df_matches_b.empty else []
        
        nameA = mA[0] if len(mA) > 0 else "— Nicht vergeben —"
        nameB = mB[0] if len(mB) > 0 else "— Nicht vergeben —"
        
        comparison.append({
            "Wohnung": w_id,
            f"Mieter in Szenario A ({szenario_preset})": nameA,
            f"Mieter in Szenario B ({szenario_b})": nameB,
            "Veränderung": "🔴 Abweichend" if nameA != nameB else "🟢 Identisch"
        })
        
    df_comp = pd.DataFrame(comparison)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 4: GESAMTÜBERSICHT & EXPORT
# ---------------------------------------------------------
with tab4:
    st.subheader("📄 Vollständige Vergabe-Liste & Export")
    
    df_m_clean = clean_column_names(df_m_active, "mieter")
    
    if not df_matches.empty:
        full_overview = pd.merge(
            df_m_clean, 
            df_matches[['Mieter_ID', 'Wohnungs_ID', 'Wunsch_Rang', 'Score']], 
            left_on='Mieter-ID', 
            right_on='Mieter_ID', 
            how='left'
        )
        full_overview['Status'] = full_overview['Wohnungs_ID'].apply(lambda x: "Zugewiesen" if pd.notna(x) else "Warteliste")
        
        display_cols = [c for c in ['Mieter-ID', 'Name', 'Status', 'Wohnungs_ID', 'Wunsch_Rang', 'Score', 'Empfehlung (Ja/Nein)', 'Anmeldedatum'] if c in full_overview.columns]
        
        st.dataframe(
            full_overview[display_cols],
            use_container_width=True,
            hide_index=True
        )
        # EXPORT-OPTION: CSV & EXCEL (Sicherer Fallback)
        try:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                full_overview.to_excel(writer, sheet_name='Vergabe_Ergebnis', index=False)
                df_matches.to_excel(writer, sheet_name='Zuweisungen_Detail', index=False)
                
            st.download_button(
                label="📥 Vergabeliste als Excel herunterladen (.xlsx)",
                data=buffer.getvalue(),
                file_name=f"Wohnungsvergabe_Ergebnis_{szenario_preset}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception:
            # Fallback auf CSV, falls openpyxl auf dem Server blockiert ist
            csv_data = full_overview.to_csv(index=False, sep=";").encode('utf-8-sig')
            st.download_button(
                label="📥 Vergabeliste als CSV herunterladen (.csv)",
                data=csv_data,
                file_name=f"Wohnungsvergabe_Ergebnis_{szenario_preset}.csv",
                mime="text/csv"
            )
    else:
        st.info("Keine aktiven Zuweisungen berechnet.")