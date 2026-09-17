import os
import sqlite3

import pandas as pd
import utility


# AA Funzione Helper Per Rilevare I Dispositivi Associati Nel Database Gadgetbridge
def getAvailableDevices(conn):
    # BB Estrazione Della Lista Dispositivi Dalla Tabella DEVICE
    queryDevices = """
        SELECT _id, NAME, MANUFACTURER, TYPE_NAME 
        FROM DEVICE 
        ORDER BY _id ASC;
    """
    try:
        return pd.read_sql_query(queryDevices, conn)
    except Exception:
        return pd.DataFrame()


# AA Mappa Dei Codici Fase Sonno Specifici Per Xiaomi
# BB Corrispondenza Verificata Confrontando Le Durate Calcolate Con I Totali Ufficiali Di XIAOMI_SLEEP_TIME_SAMPLE
XIAOMI_SLEEP_STAGE_MAP = {
    2: "Sonno Profondo",
    3: "Sonno Leggero",
    4: "Sonno REM",
    5: "Sveglio",
}


# AA Parser Per I Dati Del Sonno Della Famiglia Xiaomi
def parseXiaomiSleep(conn, deviceId):
    # BB Estrazione Delle Sessioni Di Sonno Aggregate (Una Riga Per Notte)
    querySessions = f"""
        SELECT
            TIMESTAMP,
            WAKEUP_TIME,
            TOTAL_DURATION,
            DEEP_SLEEP_DURATION,
            LIGHT_SLEEP_DURATION,
            REM_SLEEP_DURATION,
            AWAKE_DURATION
        FROM XIAOMI_SLEEP_TIME_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    sleepSessions = pd.read_sql_query(querySessions, conn)

    # BB Estrazione Della Timeline Dettagliata Delle Fasi (Per Il Drill-Down Giornaliero)
    queryStages = f"""
        SELECT
            TIMESTAMP,
            STAGE
        FROM XIAOMI_SLEEP_STAGE_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    stageRows = pd.read_sql_query(queryStages, conn)

    sleepStages = pd.DataFrame()

    if not sleepSessions.empty:
        # CC Associazione Di Ogni Fase Alla Sessione Di Appartenenza
        # DD Necessario Perche' XIAOMI_SLEEP_STAGE_SAMPLE Non Ha Un ID Di Sessione Esplicito
        # EE Il Confronto Avviene Sui Millisecondi Grezzi, Prima Di Qualsiasi Conversione Di Fuso Orario
        stageBlocks = []
        for _, session in sleepSessions.iterrows():
            sessionStartMs = session["TIMESTAMP"]
            sessionEndMs = session["WAKEUP_TIME"]

            mask = (stageRows["TIMESTAMP"] >= sessionStartMs) & (stageRows["TIMESTAMP"] < sessionEndMs)
            sessionStages = stageRows[mask].copy()

            if sessionStages.empty:
                continue

            # EE Calcolo Della Durata Di Ogni Fase Come Differenza Con La Fase Successiva
            # EE L'Ultima Fase Della Notte Dura Fino All'Orario Di Sveglia Della Sessione
            sessionStages["NEXT_TIMESTAMP"] = sessionStages["TIMESTAMP"].shift(-1)
            sessionStages.loc[sessionStages.index[-1], "NEXT_TIMESTAMP"] = sessionEndMs
            sessionStages["Durata (min)"] = ((sessionStages["NEXT_TIMESTAMP"] - sessionStages["TIMESTAMP"]) / 1000 / 60).round(1)
            sessionStages["SESSION_WAKEUP_TIME"] = sessionEndMs

            stageBlocks.append(sessionStages)

        if stageBlocks:
            sleepStages = pd.concat(stageBlocks, ignore_index=True)

            sleepStages["Inizio Fase"] = (
                pd.to_datetime(sleepStages["TIMESTAMP"], unit="ms", utc=True)
                .dt.tz_convert("Europe/Rome")
                .dt.tz_localize(None)
            )
            # EE La Fase Viene Attribuita Alla Data Di Sveglia Della Sessione Di Appartenenza
            sleepStages["Data"] = (
                pd.to_datetime(sleepStages["SESSION_WAKEUP_TIME"], unit="ms", utc=True)
                .dt.tz_convert("Europe/Rome")
                .dt.date
            )
            sleepStages["Fase"] = sleepStages["STAGE"].map(XIAOMI_SLEEP_STAGE_MAP)

            # EE Segnalazione Di Eventuali Codici Fase Non Ancora Mappati, Senza Interrompere Lo Script
            unknownStages = sleepStages.loc[sleepStages["Fase"].isna(), "STAGE"].unique()
            if len(unknownStages) > 0:
                print(f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET} Codici Fase Sonno Non Riconosciuti: {list(unknownStages)}")
                sleepStages["Fase"] = sleepStages["Fase"].fillna("Sconosciuto")

            sleepStages = sleepStages[["Data", "Inizio Fase", "Fase", "Durata (min)"]]

        # CC Conversione Delle Colonne Di Sessione In Orario Locale (Fatta Dopo Aver Usato I Millisecondi Grezzi Sopra)
        sleepSessions["Inizio Sonno"] = (
            pd.to_datetime(sleepSessions["TIMESTAMP"], unit="ms", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.tz_localize(None)
        )
        sleepSessions["Fine Sonno"] = (
            pd.to_datetime(sleepSessions["WAKEUP_TIME"], unit="ms", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.tz_localize(None)
        )
        # CC La Notte Viene Attribuita Alla Data Della Sveglia (Convenzione Standard Di Sleep-Tracking)
        sleepSessions["Data"] = sleepSessions["Fine Sonno"].dt.date

        renameMapSleep = {
            "TOTAL_DURATION": "Durata Totale (min)",
            "DEEP_SLEEP_DURATION": "Sonno Profondo (min)",
            "LIGHT_SLEEP_DURATION": "Sonno Leggero (min)",
            "REM_SLEEP_DURATION": "Sonno REM (min)",
            "AWAKE_DURATION": "Tempo Sveglio (min)",
        }
        sleepSessions = sleepSessions.rename(columns=renameMapSleep)

        columnsSessions = [
            "Data", "Inizio Sonno", "Fine Sonno", "Durata Totale (min)",
            "Sonno Profondo (min)", "Sonno Leggero (min)", "Sonno REM (min)", "Tempo Sveglio (min)"
        ]
        sleepSessions = sleepSessions[columnsSessions]

    return sleepSessions, sleepStages


# AA Parser Specifico Per La Famiglia Xiaomi / Redmi / Poco (Stesso Protocollo, Stesse Tabelle)
def parseXiaomiFamily(conn, deviceId):
    # BB Estrazione Delle Rilevazioni Al Minuto Filtrate Per DEVICE_ID
    queryActivity = f"""
        SELECT 
            TIMESTAMP,
            STEPS,
            HEART_RATE,
            RAW_KIND,
            SPO2,
            STRESS,
            DISTANCE_CM,
            ACTIVE_CALORIES
        FROM XIAOMI_ACTIVITY_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    activityData = pd.read_sql_query(queryActivity, conn)

    if not activityData.empty:
        # CC Conversione Del Timestamp Unix In UTC E Localizzazione Su Fuso Orario Locale
        activityData["Data Ora"] = (
            pd.to_datetime(activityData["TIMESTAMP"], unit="s", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.tz_localize(None)
        )
        activityData["Data"] = activityData["Data Ora"].dt.date
        activityData["Ora"] = activityData["Data Ora"].dt.strftime("%H:%M:%S")

        # CC Conversione Della Distanza Da Centimetri A Metri
        activityData["Distanza (m)"] = (activityData["DISTANCE_CM"] / 100).round(1)

        # CC Ridenominazione Delle Metriche Biometriche E Di Movimento
        renameMapActivity = {
            "STEPS": "Passi",
            "HEART_RATE": "Frequenza Cardiaca (bpm)",
            "RAW_KIND": "Tipo Attivita",
            "SPO2": "SpO2 (%)",
            "STRESS": "Livello Stress",
            "ACTIVE_CALORIES": "Calorie Attive (kcal)",
        }
        activityData = activityData.rename(columns=renameMapActivity)
        activityData["SpO2 (%)"] = activityData["SpO2 (%)"].replace(0, pd.NA)

        columnsActivity = [
            "Data", "Ora", "Data Ora", "Passi", "Frequenza Cardiaca (bpm)",
            "SpO2 (%)", "Livello Stress", "Calorie Attive (kcal)", "Distanza (m)", "Tipo Attivita"
        ]
        activityData = activityData[columnsActivity]

    # BB Estrazione Delle Metriche Aggregate Giornaliere Filtrate Per DEVICE_ID
    querySummary = f"""
        SELECT 
            TIMESTAMP,
            STEPS,
            CALORIES,
            ACTIVE_CALORIES,
            HR_RESTING,
            HR_AVG,
            HR_MIN,
            HR_MIN_TS,
            HR_MAX,
            HR_MAX_TS,
            STRESS_AVG,
            STRESS_MAX,
            STRESS_MIN,
            SPO2_AVG,
            STANDING,
            VITALITY_CURRENT
        FROM XIAOMI_DAILY_SUMMARY_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    dailySummary = pd.read_sql_query(querySummary, conn)

    if not dailySummary.empty:
        dailySummary["Data"] = (
            pd.to_datetime(dailySummary["TIMESTAMP"], unit="ms", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.date
        )

        hrMinValid = dailySummary["HR_MIN_TS"].replace(0, pd.NA)
        hrMaxValid = dailySummary["HR_MAX_TS"].replace(0, pd.NA)
        dailySummary["Ora Battito Min"] = (
            pd.to_datetime(hrMinValid, unit="s", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.strftime("%H:%M:%S")
        )
        dailySummary["Ora Battito Max"] = (
            pd.to_datetime(hrMaxValid, unit="s", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.strftime("%H:%M:%S")
        )

        renameMapSummary = {
            "STEPS": "Passi Totali",
            "CALORIES": "Calorie Totali (kcal)",
            "ACTIVE_CALORIES": "Calorie Attive (kcal)",
            "HR_RESTING": "Frequenza Riposo (bpm)",
            "HR_AVG": "Frequenza Media (bpm)",
            "HR_MIN": "Frequenza Minima (bpm)",
            "HR_MAX": "Frequenza Massima (bpm)",
            "STRESS_AVG": "Stress Medio",
            "STRESS_MAX": "Stress Massimo",
            "STRESS_MIN": "Stress Minimo",
            "SPO2_AVG": "SpO2 Medio (%)",
            "STANDING": "Secondi In Piedi",
            "VITALITY_CURRENT": "Indice Vitalita",
        }
        dailySummary = dailySummary.rename(columns=renameMapSummary)
        dailySummary["Ore In Piedi"] = (dailySummary["Secondi In Piedi"] / 3600).round(1)

        columnsDaily = [
            "Data", "Passi Totali", "Calorie Totali (kcal)", "Calorie Attive (kcal)",
            "Frequenza Riposo (bpm)", "Frequenza Media (bpm)", "Frequenza Minima (bpm)", "Ora Battito Min",
            "Frequenza Massima (bpm)", "Ora Battito Max", "Stress Medio", "Stress Massimo",
            "Stress Minimo", "SpO2 Medio (%)", "Ore In Piedi", "Indice Vitalita"
        ]
        dailySummary = dailySummary[columnsDaily]

    # BB Estrazione Dei Dati Del Sonno
    sleepSessions, sleepStages = parseXiaomiSleep(conn, deviceId)

    return activityData, dailySummary, sleepSessions, sleepStages


# AA Funzione Master Per Elaborare I Dati Smartwatch
# BB Supporta Solo Dispositivi Xiaomi / Redmi / Poco (Stesso Protocollo Xiaomi Wear)
# CC Per Aggiungere Altre Marche: Fork Del Progetto, Il Codice E Pubblico Su GitHub
def processSmartwatchData(DB_PATH, targetDevice=None):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagSmartwatch = f"{utility.CLR_SMARTWATCH}[SMARTWATCH]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # AA Verifica Esistenza Del Database Gadgetbridge
    if not os.path.exists(DB_PATH):
        print(f"\n{tagSmartwatch} File Database Non Trovato Nel Percorso Specificato: {DB_PATH}\n")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # BB Apertura Connessione Verso Il Database SQLite
    conn = sqlite3.connect(DB_PATH)

    # AA Rilevamento Dei Dispositivi Registrati Nel Database
    devicesDf = getAvailableDevices(conn)
    if devicesDf.empty:
        print(f"\n{tagErrore} Nessun Dispositivo Rilevato Nella Tabella DEVICE Di Gadgetbridge.\n")
        conn.close()
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # BB Selezione Del Dispositivo Target (Automatica O Tramite Input Utente)
    selectedDevice = None
    if targetDevice is None:
        # Selezione Automatica Del Primo Dispositivo Disponibile
        selectedDevice = devicesDf.iloc[0]
    else:
        # Ricerca Tramite Nome O Produttore
        matched = devicesDf[
            devicesDf["NAME"].astype(str).str.contains(str(targetDevice), case=False, na=False) |
            devicesDf["MANUFACTURER"].astype(str).str.contains(str(targetDevice), case=False, na=False) |
            devicesDf["TYPE_NAME"].astype(str).str.contains(str(targetDevice), case=False, na=False)
        ]
        if not matched.empty:
            selectedDevice = matched.iloc[0]
        else:
            print(f"\n{tagErrore} Dispositivo '{targetDevice}' Non Trovato. Verrà Utilizzato: {devicesDf.iloc[0]['NAME']}\n")
            selectedDevice = devicesDf.iloc[0]

    deviceId = int(selectedDevice["_id"])
    deviceName = selectedDevice["NAME"]
    manufacturer = str(selectedDevice["MANUFACTURER"]).upper()
    typeName = str(selectedDevice["TYPE_NAME"]).upper()

    print(f"\n{tagSmartwatch} Dispositivo Selezionato: {utility.CLR_BOLD}{deviceName}{utility.CLR_RESET} (ID: {deviceId}, Produttore: {manufacturer})")

    # AA Solo Famiglia Xiaomi / Redmi / Poco E Supportata
    activityData = pd.DataFrame()
    dailySummary = pd.DataFrame()
    sleepSessions = pd.DataFrame()
    sleepStages = pd.DataFrame()

    if manufacturer in ["XIAOMI", "REDMI", "POCO"] or "XIAOMI" in typeName or "REDMI" in typeName:
        activityData, dailySummary, sleepSessions, sleepStages = parseXiaomiFamily(conn, deviceId)
    else:
        print(f"{tagErrore} Produttore '{manufacturer}' Non Supportato. Questo Script Gestisce Solo Dispositivi Xiaomi/Redmi/Poco.")

    # BB Chiusura Connessione Database
    conn.close()

    # AA Notifica Di Completamento Estrazione Dati
    if not activityData.empty or not dailySummary.empty:
        print(
            f"{tagSmartwatch} Dati Smartwatch Estratti Con Successo: "
            f"{utility.CLR_BOLD}{len(activityData)}{utility.CLR_RESET} Rilevazioni, "
            f"{utility.CLR_BOLD}{len(dailySummary)}{utility.CLR_RESET} Giorni Di Sintesi, "
            f"{utility.CLR_BOLD}{len(sleepSessions)}{utility.CLR_RESET} Notti Registrate.\n"
        )

    return activityData, dailySummary, sleepSessions, sleepStages


# AA Blocco Di Test Diretto Dello Script
if __name__ == "__main__":
    DB_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/gadgetBridgeSync/Gadgetbridge.db"

    if not os.path.exists(DB_PATH):
        print(f"File Non Trovato: {DB_PATH}")
    else:
        activityData, dailySummary, sleepSessions, sleepStages = processSmartwatchData(DB_PATH)

        if not activityData.empty:
            print(f"Attivita: {len(activityData)} righe, dal {activityData['Data'].min()} al {activityData['Data'].max()}")
        else:
            print("Nessun Dato Di Attivita Trovato.")

        if not dailySummary.empty:
            print(f"Riepilogo Giornaliero: {len(dailySummary)} righe, dal {dailySummary['Data'].min()} al {dailySummary['Data'].max()}")
        else:
            print("Nessun Riepilogo Giornaliero Trovato.")

        if not sleepSessions.empty:
            print("\n--- Sessioni Di Sonno ---")
            print(sleepSessions.to_string(index=False))

        if not sleepStages.empty:
            print("\n--- Timeline Fasi Sonno ---")
            print(sleepStages.to_string(index=False))