import sqlite3

import pandas as pd
import utility

# AA Soglia Di Affidabilita Per Le Misurazioni Corporee
# BB Le Misurazioni Precedenti A Questa Data Sono State Rilevate Con Minore Rigore
SOGLIA_AFFIDABILITA_MISURE = "2026-06-01"


# AA Creazione Delle Tabelle Del Database Dashboard, Se Non Esistono Ancora
def initializeDashboardDB(DASHBOARD_DB_PATH):
    conn = sqlite3.connect(DASHBOARD_DB_PATH)
    cursor = conn.cursor()

    # BB Dominio Smartwatch (Dati Ad Alta Frequenza Da Gadgetbridge)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_activity_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            ora TEXT NOT NULL,
            data_ora TEXT NOT NULL,
            passi INTEGER,
            frequenza_cardiaca INTEGER,
            spo2 REAL,
            livello_stress INTEGER,
            calorie_attive REAL,
            distanza_m REAL,
            tipo_attivita INTEGER
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_raw_data ON smartwatch_activity_raw(data);")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_daily_summary (
            data TEXT PRIMARY KEY,
            passi_totali INTEGER,
            calorie_totali REAL,
            calorie_attive REAL,
            frequenza_riposo INTEGER,
            frequenza_media INTEGER,
            frequenza_minima INTEGER,
            ora_battito_min TEXT,
            frequenza_massima INTEGER,
            ora_battito_max TEXT,
            stress_medio INTEGER,
            stress_massimo INTEGER,
            stress_minimo INTEGER,
            spo2_medio REAL,
            ore_in_piedi REAL,
            indice_vitalita INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_sleep_sessions (
            data TEXT PRIMARY KEY,
            inizio_sonno TEXT,
            fine_sonno TEXT,
            durata_totale_min INTEGER,
            sonno_profondo_min INTEGER,
            sonno_leggero_min INTEGER,
            sonno_rem_min INTEGER,
            tempo_sveglio_min INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_sleep_stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            inizio_fase TEXT NOT NULL,
            fase TEXT,
            durata_min REAL
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sleep_stages_data ON smartwatch_sleep_stages(data);")

    # BB Dominio Tracking (Specchio Dei Fogli Excel)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misure (
            data_misurazione TEXT PRIMARY KEY,
            peso_kg REAL,
            circ_collo_cm REAL,
            circ_vita_cm REAL,
            circ_fianchi_cm REAL,
            circ_braccio_cm REAL,
            circ_coscia_cm REAL,
            massa_grassa_pct REAL,
            massa_magra_kg REAL,
            metabolismo_basale REAL,
            fabbisogno_giornaliero REAL,
            affidabile INTEGER NOT NULL DEFAULT 1
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dieta (
            data_inizio TEXT PRIMARY KEY,
            data_fine TEXT,
            durata INTEGER,
            kcal INTEGER,
            deficit_teorico INTEGER,
            carbo_g INTEGER,
            grassi_g INTEGER,
            proteine_g INTEGER,
            proteine_g_kg REAL,
            pct_carbo REAL,
            pct_grassi REAL,
            pct_proteine REAL,
            note TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personale (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            sesso TEXT,
            altezza_cm REAL,
            data_nascita TEXT,
            eta INTEGER,
            peso_corrente_kg REAL,
            massa_magra_corrente_kg REAL,
            bmr_mifflin REAL,
            bmr_katch REAL,
            tdee_corrente REAL,
            deficit_corrente REAL,
            ultimo_aggiornamento TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allenamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            durata_allenamento REAL,
            nome_scheda TEXT,
            nome_esercizio TEXT,
            indice_serie INTEGER,
            ripetizioni_serie INTEGER,
            peso_serie REAL,
            volume_serie INTEGER,
            massimale_stimato_serie INTEGER,
            note TEXT
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_allenamento_data ON allenamento(data);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_allenamento_esercizio ON allenamento(nome_esercizio);")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS palestra (
            nome_esercizio TEXT PRIMARY KEY,
            schema TEXT,
            volume_totale_kg INTEGER,
            data TEXT,
            numero_serie INTEGER,
            ripetizioni_medie INTEGER,
            peso_medio REAL,
            massimale_stimato_1rm INTEGER,
            note TEXT
        );
    """)

    # BB Tabella Derivata (Calcolata Durante La Sync A Partire Da Misure, Dieta E Personale)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profilo_storico (
            data TEXT PRIMARY KEY,
            eta INTEGER,
            bmr_mifflin REAL,
            bmr_katch REAL,
            tdee REAL,
            deficit_teorico INTEGER,
            affidabile INTEGER NOT NULL DEFAULT 1
        );
    """)

    conn.commit()
    conn.close()


# AA Sincronizzazione Dei Dati Smartwatch (Attivita, Riepilogo Giornaliero, Sonno) Verso Il Database Dashboard
def syncSmartwatchData(DASHBOARD_DB_PATH, activityData, dailySummary, sleepSessions, sleepStages):
    tagDashboard = f"{utility.CLR_DASHBOARD}[DASHBOARD]{utility.CLR_RESET}"

    conn = sqlite3.connect(DASHBOARD_DB_PATH)

    # BB Specchio Dell'Attivita Al Minuto
    if not activityData.empty:
        activityDf = activityData.copy()
        activityDf["Data"] = pd.to_datetime(activityDf["Data"]).dt.strftime("%Y-%m-%d")
        activityDf["Data Ora"] = pd.to_datetime(activityDf["Data Ora"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        renameMapActivity = {
            "Data": "data",
            "Ora": "ora",
            "Data Ora": "data_ora",
            "Passi": "passi",
            "Frequenza Cardiaca (bpm)": "frequenza_cardiaca",
            "SpO2 (%)": "spo2",
            "Livello Stress": "livello_stress",
            "Calorie Attive (kcal)": "calorie_attive",
            "Distanza (m)": "distanza_m",
            "Tipo Attivita": "tipo_attivita",
        }
        activityDf = activityDf.rename(columns=renameMapActivity)

        conn.execute("DELETE FROM smartwatch_activity_raw;")
        activityDf.to_sql("smartwatch_activity_raw", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Attivita Specchiata: {utility.CLR_BOLD}{len(activityDf)}{utility.CLR_RESET} Righe.")

    # BB Specchio Del Riepilogo Giornaliero
    if not dailySummary.empty:
        summaryDf = dailySummary.copy()
        summaryDf["Data"] = pd.to_datetime(summaryDf["Data"]).dt.strftime("%Y-%m-%d")

        renameMapSummary = {
            "Data": "data",
            "Passi Totali": "passi_totali",
            "Calorie Totali (kcal)": "calorie_totali",
            "Calorie Attive (kcal)": "calorie_attive",
            "Frequenza Riposo (bpm)": "frequenza_riposo",
            "Frequenza Media (bpm)": "frequenza_media",
            "Frequenza Minima (bpm)": "frequenza_minima",
            "Ora Battito Min": "ora_battito_min",
            "Frequenza Massima (bpm)": "frequenza_massima",
            "Ora Battito Max": "ora_battito_max",
            "Stress Medio": "stress_medio",
            "Stress Massimo": "stress_massimo",
            "Stress Minimo": "stress_minimo",
            "SpO2 Medio (%)": "spo2_medio",
            "Ore In Piedi": "ore_in_piedi",
            "Indice Vitalita": "indice_vitalita",
        }
        summaryDf = summaryDf.rename(columns=renameMapSummary)

        conn.execute("DELETE FROM smartwatch_daily_summary;")
        summaryDf.to_sql("smartwatch_daily_summary", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Riepilogo Giornaliero Specchiato: {utility.CLR_BOLD}{len(summaryDf)}{utility.CLR_RESET} Righe.")

    # BB Specchio Delle Sessioni Di Sonno
    if not sleepSessions.empty:
        sessionsDf = sleepSessions.copy()
        sessionsDf["Data"] = pd.to_datetime(sessionsDf["Data"]).dt.strftime("%Y-%m-%d")
        sessionsDf["Inizio Sonno"] = pd.to_datetime(sessionsDf["Inizio Sonno"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        sessionsDf["Fine Sonno"] = pd.to_datetime(sessionsDf["Fine Sonno"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        renameMapSessions = {
            "Data": "data",
            "Inizio Sonno": "inizio_sonno",
            "Fine Sonno": "fine_sonno",
            "Durata Totale (min)": "durata_totale_min",
            "Sonno Profondo (min)": "sonno_profondo_min",
            "Sonno Leggero (min)": "sonno_leggero_min",
            "Sonno REM (min)": "sonno_rem_min",
            "Tempo Sveglio (min)": "tempo_sveglio_min",
        }
        sessionsDf = sessionsDf.rename(columns=renameMapSessions)

        conn.execute("DELETE FROM smartwatch_sleep_sessions;")
        sessionsDf.to_sql("smartwatch_sleep_sessions", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Sessioni Sonno Specchiate: {utility.CLR_BOLD}{len(sessionsDf)}{utility.CLR_RESET} Notti.")

    # BB Specchio Della Timeline Delle Fasi Di Sonno
    if not sleepStages.empty:
        stagesDf = sleepStages.copy()
        stagesDf["Data"] = pd.to_datetime(stagesDf["Data"]).dt.strftime("%Y-%m-%d")
        stagesDf["Inizio Fase"] = pd.to_datetime(stagesDf["Inizio Fase"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        renameMapStages = {
            "Data": "data",
            "Inizio Fase": "inizio_fase",
            "Fase": "fase",
            "Durata (min)": "durata_min",
        }
        stagesDf = stagesDf.rename(columns=renameMapStages)

        conn.execute("DELETE FROM smartwatch_sleep_stages;")
        stagesDf.to_sql("smartwatch_sleep_stages", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Fasi Sonno Specchiate: {utility.CLR_BOLD}{len(stagesDf)}{utility.CLR_RESET} Righe.")

    conn.commit()
    conn.close()

    print(f"\n{tagDashboard} {utility.CLR_BOLD}Sincronizzazione Smartwatch Completata!{utility.CLR_RESET}\n")


# AA Sincronizzazione Dei Dati Excel (Misure, Dieta, Personale, Allenamento, Palestra) Verso Il Database Dashboard
def syncTrackingMirror(DASHBOARD_DB_PATH, excelData):
    tagDashboard = f"{utility.CLR_DASHBOARD}[DASHBOARD]{utility.CLR_RESET}"

    conn = sqlite3.connect(DASHBOARD_DB_PATH)

    # BB Specchio Della Scheda Dati Misure
    misureDf = excelData["Dati Misure"].copy()
    if not misureDf.empty:
        misureDf["Data Misurazione"] = pd.to_datetime(misureDf["Data Misurazione"]).dt.strftime("%Y-%m-%d")
        misureDf["affidabile"] = (misureDf["Data Misurazione"] >= SOGLIA_AFFIDABILITA_MISURE).astype(int)

        renameMapMisure = {
            "Data Misurazione": "data_misurazione",
            "Peso (Kg)": "peso_kg",
            "Circonferenza Collo (cm)": "circ_collo_cm",
            "Circonferenza Vita (cm)": "circ_vita_cm",
            "Circonferenza Fianchi (cm)": "circ_fianchi_cm",
            "Circonferenza Braccio (cm)": "circ_braccio_cm",
            "Circonferenza Coscia (cm)": "circ_coscia_cm",
            "Massa Grassa (%)": "massa_grassa_pct",
            "Massa Magra (Kg)": "massa_magra_kg",
            "Metabolismo Basale": "metabolismo_basale",
            "Fabbisogno Giornaliero": "fabbisogno_giornaliero",
        }
        misureDf = misureDf.rename(columns=renameMapMisure)

        colonneMisure = [
            "data_misurazione", "peso_kg", "circ_collo_cm", "circ_vita_cm", "circ_fianchi_cm",
            "circ_braccio_cm", "circ_coscia_cm", "massa_grassa_pct", "massa_magra_kg",
            "metabolismo_basale", "fabbisogno_giornaliero", "affidabile"
        ]
        misureDf = misureDf[colonneMisure]

        conn.execute("DELETE FROM misure;")
        misureDf.to_sql("misure", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Misure Specchiate: {utility.CLR_BOLD}{len(misureDf)}{utility.CLR_RESET} Righe.")

    # BB Specchio Della Scheda Dati Dieta
    dietaDf = excelData["Dati Dieta"].copy()
    if not dietaDf.empty:
        dietaDf["Data Inizio"] = pd.to_datetime(dietaDf["Data Inizio"]).dt.strftime("%Y-%m-%d")

        # CC La Fase Ancora Aperta Non Ha Data Fine: Deve Restare Nulla, Non Diventare La Stringa "NaT"
        dataFineOBJ = pd.to_datetime(dietaDf["Data Fine"])
        dietaDf["Data Fine"] = dataFineOBJ.dt.strftime("%Y-%m-%d")
        dietaDf.loc[dataFineOBJ.isna(), "Data Fine"] = None

        renameMapDieta = {
            "Data Inizio": "data_inizio",
            "Data Fine": "data_fine",
            "Durata": "durata",
            "Kcal": "kcal",
            "Deficit Teorico": "deficit_teorico",
            "Carbo (g)": "carbo_g",
            "Grassi (g)": "grassi_g",
            "Proteine (g)": "proteine_g",
            "Proteine (g/Kg)": "proteine_g_kg",
            "% Carbo": "pct_carbo",
            "% Grassi": "pct_grassi",
            "% Proteine": "pct_proteine",
            "Note": "note",
        }
        dietaDf = dietaDf.rename(columns=renameMapDieta)

        conn.execute("DELETE FROM dieta;")
        dietaDf.to_sql("dieta", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Dieta Specchiata: {utility.CLR_BOLD}{len(dietaDf)}{utility.CLR_RESET} Fasi.")

    # BB Specchio Della Scheda Dati Personali (Riga Singola, Layout Verticale Parametro/Valore)
    personalDf = excelData["Dati Personali"]

    # CC Piccola Funzione Di Appoggio Per Leggere Un Valore Dato Il Nome Del Parametro
    def getParam(nome):
        match = personalDf.loc[personalDf["Parametro"] == nome, "Valore"]
        if match.empty:
            return None
        return match.iloc[0]

    sesso = getParam("Sesso")
    altezza = getParam("Altezza (cm)")
    dataNascita = getParam("Data Di Nascita")
    eta = getParam("Età")
    pesoCorrente = getParam("Peso Corrente (Kg)")
    massaMagraCorrente = getParam("Massa Magra Corrente (Kg)")
    bmrMifflinCorrente = getParam("BMR Mifflin-St Jeor (Kcal)")
    bmrKatchCorrente = getParam("BMR Katch-McArdle (Kcal)")
    tdeeCorrente = getParam("TDEE Corrente Pesato (Kcal)")
    deficitCorrente = getParam("Deficit Corrente (Kcal)")
    ultimoAggiornamento = getParam("Ultimo Aggiornamento")

    if dataNascita is not None:
        dataNascita = pd.to_datetime(dataNascita).strftime("%Y-%m-%d")

    if ultimoAggiornamento is not None:
        # CC Normalizzazione Difensiva: Rimuove Eventuale Timezone E Uniforma Il Formato
        # DD Stesso Tipo Di Valore "Sporco" Che Ha Gia' Causato Il Crash Di Salvataggio In personal.py
        ultimoAggiornamentoOBJ = pd.to_datetime(ultimoAggiornamento)
        if ultimoAggiornamentoOBJ.tzinfo is not None:
            ultimoAggiornamentoOBJ = ultimoAggiornamentoOBJ.tz_localize(None)
        ultimoAggiornamento = ultimoAggiornamentoOBJ.strftime("%Y-%m-%d %H:%M:%S")

    conn.execute("DELETE FROM personale;")
    conn.execute("""
        INSERT INTO personale (
            id, sesso, altezza_cm, data_nascita, eta, peso_corrente_kg,
            massa_magra_corrente_kg, bmr_mifflin, bmr_katch, tdee_corrente,
            deficit_corrente, ultimo_aggiornamento
        ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        sesso, altezza, dataNascita, eta, pesoCorrente,
        massaMagraCorrente, bmrMifflinCorrente, bmrKatchCorrente, tdeeCorrente,
        deficitCorrente, ultimoAggiornamento
    ))
    print(f"{tagDashboard} Profilo Personale Specchiato.")

    # BB Specchio Della Scheda Dati Allenamento
    allenamentoDf = excelData["Dati Allenamento"].copy()
    if not allenamentoDf.empty:
        allenamentoDf["Data"] = pd.to_datetime(allenamentoDf["Data"]).dt.strftime("%Y-%m-%d")

        renameMapAllenamento = {
            "Data": "data",
            "Durata Allenamento": "durata_allenamento",
            "Nome Scheda": "nome_scheda",
            "Nome Esercizio": "nome_esercizio",
            "Indice Serie": "indice_serie",
            "Ripetizioni Serie": "ripetizioni_serie",
            "Peso Serie": "peso_serie",
            "Volume Serie": "volume_serie",
            "Massimale Stimato Serie": "massimale_stimato_serie",
            "Note Post Allenamento": "note",
        }
        allenamentoDf = allenamentoDf.rename(columns=renameMapAllenamento)

        conn.execute("DELETE FROM allenamento;")
        allenamentoDf.to_sql("allenamento", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Allenamenti Specchiati: {utility.CLR_BOLD}{len(allenamentoDf)}{utility.CLR_RESET} Serie.")

    # BB Specchio Della Scheda Dati Palestra
    palestraDf = excelData["Dati Palestra"].copy()
    if not palestraDf.empty:
        palestraDf["Data"] = pd.to_datetime(palestraDf["Data"]).dt.strftime("%Y-%m-%d")

        renameMapPalestra = {
            "Nome Esercizio": "nome_esercizio",
            "Schema": "schema",
            "Volume Totale (Kg)": "volume_totale_kg",
            "Data": "data",
            "Numero Serie": "numero_serie",
            "Ripetizioni Medie": "ripetizioni_medie",
            "Peso Medio": "peso_medio",
            "Massimale Stimato (1RM)": "massimale_stimato_1rm",
            "Note Post Allenamento": "note",
        }
        palestraDf = palestraDf.rename(columns=renameMapPalestra)

        conn.execute("DELETE FROM palestra;")
        palestraDf.to_sql("palestra", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Bacheca Record Specchiata: {utility.CLR_BOLD}{len(palestraDf)}{utility.CLR_RESET} Esercizi.")

    # BB Calcolo Della Tabella Derivata Profilo Storico (Eta, BMR Mifflin E Deficit Per Ogni Misurazione)
    # CC Serve Sesso, Altezza E Data Di Nascita Dal Profilo Personale, Gia Estratti Sopra
    if not misureDf.empty and dataNascita is not None and altezza is not None and sesso is not None:
        dobOBJ = pd.to_datetime(dataNascita)
        altezzaFloat = float(altezza)

        profiloRows = []
        for _, riga in misureDf.iterrows():
            dataMisurazioneOBJ = pd.to_datetime(riga["data_misurazione"])
            pesoRiga = riga["peso_kg"]

            # DD Calcolo Dell'Eta Alla Data Della Misurazione (Stessa Logica Di personal.py)
            etaRiga = dataMisurazioneOBJ.year - dobOBJ.year - (
                (dataMisurazioneOBJ.month, dataMisurazioneOBJ.day) < (dobOBJ.month, dobOBJ.day)
            )

            # DD Calcolo Del BMR Mifflin-St Jeor Alla Data Della Misurazione
            if sesso == "M":
                bmrMifflinRiga = (10 * pesoRiga) + (6.25 * altezzaFloat) - (5 * etaRiga) + 5
            else:
                bmrMifflinRiga = (10 * pesoRiga) + (6.25 * altezzaFloat) - (5 * etaRiga) - 161

            # DD Ricerca Della Fase Dieta Attiva Alla Data Della Misurazione, Se Presente
            deficitRiga = None
            if not dietaDf.empty:
                faseAttiva = dietaDf[
                    (dietaDf["data_inizio"] <= riga["data_misurazione"]) &
                    ((dietaDf["data_fine"].isna()) | (dietaDf["data_fine"] >= riga["data_misurazione"]))
                ]
                if not faseAttiva.empty:
                    deficitRiga = int(faseAttiva.iloc[-1]["deficit_teorico"])

            profiloRows.append({
                "data": riga["data_misurazione"],
                "eta": int(etaRiga),
                "bmr_mifflin": round(bmrMifflinRiga, 0),
                "bmr_katch": riga["metabolismo_basale"],
                "tdee": riga["fabbisogno_giornaliero"],
                "deficit_teorico": deficitRiga,
                "affidabile": riga["affidabile"],
            })

        profiloDf = pd.DataFrame(profiloRows)

        conn.execute("DELETE FROM profilo_storico;")
        profiloDf.to_sql("profilo_storico", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Profilo Storico Calcolato: {utility.CLR_BOLD}{len(profiloDf)}{utility.CLR_RESET} Righe.")

    conn.commit()
    conn.close()

    print(f"\n{tagDashboard} {utility.CLR_BOLD}Sincronizzazione Dati Tracking Completata!{utility.CLR_RESET}\n")


# AA Blocco Di Test Diretto Dello Script
if __name__ == "__main__":
    EXCEL_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/trackingProgressi.xlsx"
    SMARTWATCH_DB = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/gadgetBridgeSync/Gadgetbridge.db"
    DASHBOARD_DB_PATH = "/home/lag/privateDashboard/dashboardData.db"

    excelData = {
        "Dati Personali": pd.read_excel(EXCEL_PATH, sheet_name="Dati Personali"),
        "Dati Misure": pd.read_excel(EXCEL_PATH, sheet_name="Dati Misure"),
        "Dati Dieta": pd.read_excel(EXCEL_PATH, sheet_name="Dati Dieta"),
        "Dati Allenamento": pd.read_excel(EXCEL_PATH, sheet_name="Dati Allenamento"),
        "Dati Palestra": pd.read_excel(EXCEL_PATH, sheet_name="Dati Palestra"),
    }

    initializeDashboardDB(DASHBOARD_DB_PATH)

    syncTrackingMirror(DASHBOARD_DB_PATH, excelData)