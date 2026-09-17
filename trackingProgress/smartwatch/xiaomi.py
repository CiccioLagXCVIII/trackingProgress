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


# AA Parser Specifico Per La Famiglia Xiaomi / Redmi / Poco
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

    return activityData, dailySummary


# AA Funzione Master Per Elaborare I Dati Smartwatch Supportando Più Modelli
# BB targetDevice Può Essere: None (Auto-Detect), Oppure Una Stringa Con Il Nome/Produttore Del Dispositivo
def processSmartwatchData(DB_PATH, targetDevice=None):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagSmartwatch = f"{utility.CLR_SMARTWATCH}[SMARTWATCH]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # AA Verifica Esistenza Del Database Gadgetbridge
    if not os.path.exists(DB_PATH):
        print(f"\n{tagSmartwatch} File Database Non Trovato Nel Percorso Specificato: {DB_PATH}\n")
        return pd.DataFrame(), pd.DataFrame()

    # BB Apertura Connessione Verso Il Database SQLite
    conn = sqlite3.connect(DB_PATH)

    # AA Rilevamento Dei Dispositivi Registrati Nel Database
    devicesDf = getAvailableDevices(conn)
    if devicesDf.empty:
        print(f"\n{tagErrore} Nessun Dispositivo Rilevato Nella Tabella DEVICE Di Gadgetbridge.\n")
        conn.close()
        return pd.DataFrame(), pd.DataFrame()

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

    # AA Smistamento Al Parser Dedicato In Base Al Produttore/Famiglia
    activityData = pd.DataFrame()
    dailySummary = pd.DataFrame()

    # BB Famiglia Xiaomi / Redmi / Poco
    if manufacturer in ["XIAOMI", "REDMI", "POCO"] or "XIAOMI" in typeName or "REDMI" in typeName:
        activityData, dailySummary = parseXiaomiFamily(conn, deviceId)

    # BB Segnaposto Per Future Famiglie (Amazfit/Huami, Huawei, Garmin, CMF, ecc.)
    elif manufacturer in ["HUAMI", "AMAZFIT"]:
        print(f"{tagErrore} Il Supporto Per Amazfit / Huami È In Fase Di Predisposizione.")
    elif manufacturer in ["HUAWEI", "HONOR"]:
        print(f"{tagErrore} Il Supporto Per Huawei / Honor È In Fase Di Predisposizione.")
    elif manufacturer in ["GARMIN"]:
        print(f"{tagErrore} Il Supporto Per Garmin È In Fase Di Predisposizione.")
    else:
        print(f"{tagErrore} Famiglia Produttore '{manufacturer}' Non Ancora Supportata.")

    # BB Chiusura Connessione Database
    conn.close()

    # AA Notifica Di Completamento Estrazione Dati
    if not activityData.empty or not dailySummary.empty:
        print(
            f"{tagSmartwatch} Dati Smartwatch Estratti Con Successo: "
            f"{utility.CLR_BOLD}{len(activityData)}{utility.CLR_RESET} Rilevazioni, "
            f"{utility.CLR_BOLD}{len(dailySummary)}{utility.CLR_RESET} Giorni Di Sintesi.\n"
        )

    return activityData, dailySummary


# AA Blocco Di Test Diretto Dello Script
if __name__ == "__main__":
    DB_PATH = "/home/lag/privateDashboard/gadgetBridgeSync/Gadgetbridge.db"

    # Test 1: Rilevamento automatico (consigliato per la maggior parte dei casi)
    activityData, dailySummary = processSmartwatchData(DB_PATH)

    # Test 2: Selezionando esplicitamente un modello/brand
    # activityData, dailySummary = processSmartwatchData(DB_PATH, targetDevice="Redmi")

    if not dailySummary.empty and not activityData.empty:
        print("Date presenti in activityData:", activityData["Data"].unique())
        print("Date presenti in dailySummary:", dailySummary["Data"].unique())