import logging
import os
import sys
from datetime import datetime, timezone

# AA Importazione Dei Moduli Del Sistema
import diet
import measures
import pandas as pd
import personal
import smartwatch
import utility
import workout

logger = logging.getLogger(__name__)

# AA Percorsi Assoluti Per Il File System Di Windows Tramite WSL
EXCEL_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/trackingProgressi.xlsx"
OPENGYM_DATA = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/workoutData.json"
SMARTWATCH_DB = "/home/lag/privateDashboard/gadgetBridgeSync/Gadgetbridge.db"

# BB Inizializzazione E Sincronizzazione All Avvio Del Programma Lineare
os.system('clear')

# CC Definizione Dei Tag Colorati Per La Visualizzazione
tagSistema = "\033[97m[SISTEMA]\033[0m"
tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

print(f"{tagSistema} {utility.CLR_BOLD}Avvio Del Sistema Di Tracciamento Progressi...{utility.CLR_RESET}")
print(f"{tagSistema} Caricamento Dei Fogli Excel In Memoria...")

# DD Caricamento Dei Fogli Di Lavoro In Un Dizionario Di DataFrame Pandas
# EE Gestione Degli Errori In Caso Di File Excel Mancante O Aperto
try:
    excelData = {
        'Dati Personali': pd.read_excel(EXCEL_PATH, sheet_name='Dati Personali'),
        'Dati Misure': pd.read_excel(EXCEL_PATH, sheet_name='Dati Misure'),
        'Dati Dieta': pd.read_excel(EXCEL_PATH, sheet_name='Dati Dieta'),
        'Dati Allenamento': pd.read_excel(EXCEL_PATH, sheet_name='Dati Allenamento'),
        'Dati Palestra': pd.read_excel(EXCEL_PATH, sheet_name='Dati Palestra')
    }
except (OSError, ValueError) as e:
    print(f"\n{tagErrore} Impossibile Caricare Il File Excel. Verifica Che Non Sia Aperto O Che Il Percorso Sia Corretto.")
    print(f"{tagErrore} Errore Rilevato: {e}\n")
    sys.exit()

# AA Sincronizzazione Silenziosa Iniziale Del Profilo
# DD Esecuzione Della Sincronizzazione Silenziosa Iniziale Senza Output
# EE Soppressione Temporanea Dei Print Per Avviare Direttamente Il Menu
oldStdout = sys.stdout
with open(os.devnull, 'w') as suppressedStdout:
    try:
        sys.stdout = suppressedStdout
        personal.updatePersonalData(excelData, EXCEL_PATH)
    finally:
        sys.stdout = oldStdout

# AA Ciclo Principale Dell Interfaccia Utente A Livello Root
while True:
    os.system('clear')
    
    # CC Stampa Del Menu Principale Con I Colori Identificativi
    print("==========================================================")
    print(f" {utility.CLR_BOLD}SISTEMA DI TRACCIAMENTO PROGRESSI - MENU PRINCIPALE{utility.CLR_RESET}")
    print("==========================================================")
    print(f" {utility.CLR_MISURE}1. Inserisci Nuova Misura Corporea{utility.CLR_RESET}")
    print(f" {utility.CLR_DIETA}2. Registra Nuova Fase Alimentare{utility.CLR_RESET}")
    print(f" {utility.CLR_ALLENAMENTO}3. Sincronizza Allenamenti{utility.CLR_RESET}")
    print(f" {utility.CLR_SMARTWATCH}4. Sincronizza Smartwatch{utility.CLR_RESET}")
    print(f" {utility.CLR_PROFILO}5. Mostra Riepilogo Profilo Corrente{utility.CLR_RESET}")
    print(" 6. Esci Dal Programma")
    print("==========================================================")
    
    scelta = input(f"{tagSistema} Inserisci Il Numero Della Scelta: ").strip()
    
    if scelta == "1":
        os.system('clear')
        # DD Esecuzione Inserimento Misure
        measures.updateMeasuresData(excelData, EXCEL_PATH)
        # EE Sincronizzazione Automatica Del Profilo A Cascata
        personal.updatePersonalData(excelData, EXCEL_PATH)
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")
        
    elif scelta == "2":
        os.system('clear')
        
        # DD Controllo Fuori Soglia Mensile Per Misurazioni Corporee (Overdue Check)
        measureData = excelData['Dati Misure']
        if len(measureData) > 0:
            latestDate = pd.to_datetime(measureData['Data Misurazione'].iloc[-1]).date()
            daysElapsed = (datetime.now(timezone.utc).date() - latestDate).days
            
            if daysElapsed > 40:
                print(f"{utility.CLR_ERRORE}[ATTENZIONE]{utility.CLR_RESET} L'Ultima Misura Corporea Risale A {utility.CLR_BOLD}{daysElapsed} Giorni Fa{utility.CLR_RESET} (Soglia: 40).")
                sceltaMisure = input(f"{utility.CLR_MISURE}[MISURE]{utility.CLR_RESET} Vuoi Inserire Una Nuova Misura Adesso Prima Della Dieta? (S/N): ").strip().upper()
                
                if sceltaMisure == 'S':
                    os.system('clear')
                    # EE Avvio Esecuzione Misure In Caso Di Risposta Affermativa
                    measures.updateMeasuresData(excelData, EXCEL_PATH)
                    # AA Sincronizzazione Del Profilo Post Misure
                    personal.updatePersonalData(excelData, EXCEL_PATH)
                    input(f"\n{tagSistema} Misurazioni Salvate. Premi Invio Per Continuare Con L Inserimento Della Dieta...")
                    os.system('clear')
                    
        # EE Esecuzione Inserimento Dieta
        diet.updateDietData(excelData, EXCEL_PATH)
        # AA Sincronizzazione Automatica Del Profilo A Cascata
        personal.updatePersonalData(excelData, EXCEL_PATH)
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")
        
    elif scelta == "3":
        os.system('clear')
        # DD Avvio Processamento Dei Dati Allenamento Da JSON
        try:
            workoutData, gymSummary = workout.processWorkoutData(OPENGYM_DATA, excelData)
            # EE Aggiornamento Delle Due Schede Allenamento E Palestra
            workout.updateTrainData(workoutData, excelData, EXCEL_PATH)
            workout.updateGymData(gymSummary, excelData, EXCEL_PATH)
        except (OSError, ValueError, KeyError, TypeError) as e:
            print(f"\n{tagErrore} Si È Verificato Un Errore Durante L'Importazione.")
            print(f"{tagErrore} Dettaglio Errore: {e}")
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")

    elif scelta == "4":
        os.system('clear')
        print(f"\n{tagSistema} {utility.CLR_SMARTWATCH}Sincronizzazione Del Profilo Con Lo Smartwatch.{utility.CLR_RESET}\n")
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")

    elif scelta == "5":
        os.system('clear')
        # DD Visualizzazione Dei Dati Personali
        print("==========================================================")
        print(f" {utility.CLR_PROFILO}{utility.CLR_BOLD}RIEPILOGO PROFILO UTENTE{utility.CLR_RESET}")
        print("==========================================================")
        personalDf = excelData['Dati Personali']
        for idx, row in personalDf.iterrows():
            param = row['Parametro']
            val = row['Valore']
            
            # EE Formattazione Delle Date Nel Formato Lineare GG-MM-AAAA HH-MM
            valFormatted = val
            if isinstance(val, (pd.Timestamp, datetime)):
                valFormatted = val.strftime("%d-%m-%Y %H:%M")
            elif param in ['Data Di Nascita', 'Ultimo Aggiornamento']:
                try:
                    valFormatted = pd.to_datetime(val).strftime("%d-%m-%Y %H:%M")
                except (ValueError, TypeError) as exc:
                    logger.debug("Impossibile Formattare Il Valore Di %s: %r", param, val, exc_info=exc)
            
            # EE Formattazione Allineata Per Le Righe Del Cruscotto
            print(f" {utility.CLR_PROFILO}{param:<30}{utility.CLR_RESET} : {utility.CLR_BOLD}{valFormatted}{utility.CLR_RESET}")
        print("==========================================================")
        input(f"\n{tagSistema} Premi Invio Per Tornare Al Menu...")

    elif scelta == "6":
        os.system('clear')
        print(f"\n{tagSistema} {utility.CLR_BOLD}Chiusura Del Programma Di Tracciamento Progressi. Alla Prossima!{utility.CLR_RESET}\n")
        break
        
    else:
        input(f"\n{tagErrore} Scelta Non Valida. Premi Invio Per Riprovare...")