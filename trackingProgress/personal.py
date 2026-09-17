import pandas as pd
import numpy as np
from datetime import datetime
import openpyxl
from copy import copy
import utility

def updatePersonalData(excelData, EXCEL_PATH):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagProfilo = f"{utility.CLR_PROFILO}[PROFILO]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # BB Verifica Presenza Dei Dati Di Misurazione Essenziali
    measureData = excelData['Dati Misure']
    
    # CC Controllo Se La Scheda Dati Misure È Vuota
    if len(measureData) == 0:
        print(f"\n{tagErrore} Nessuna Misurazione Trovata Nella Scheda Dati Misure.")
        print(f"{tagErrore} Inserisci Almeno Una Misurazione Prima Di Aggiornare Il Profilo.\n")
        return

    print(f"\n{tagProfilo} Avvio Sincronizzazione Dei Dati Personali...")

    # DD Accesso Alla Scheda Dati Personali
    personalDf = excelData['Dati Personali']
    
    # EE Pulizia Spazi Bianchi Nelle Etichette Per Evitare Errori Di Corrispondenza
    personalDf['Parametro'] = personalDf['Parametro'].astype(str).str.strip()

    # AA Estrazione Dei Dati Statici Inseriti Dall'Utente
    gender = personalDf.loc[personalDf['Parametro'] == 'Sesso', 'Valore'].values[0]
    heightValue = personalDf.loc[personalDf['Parametro'] == 'Altezza (cm)', 'Valore'].values[0]
    height = float(heightValue)
    dobValue = personalDf.loc[personalDf['Parametro'] == 'Data Di Nascita', 'Valore'].values[0]
    dobDate = pd.to_datetime(dobValue)

    # BB Recupero Delle Informazioni Fisiche Più Recenti Dallo Storico Misure
    latestMeasure = measureData.iloc[-1]
    currentWeight = float(latestMeasure['Peso (Kg)'])
    currentLbm = float(latestMeasure['Massa Magra (Kg)'])
    currentTdee = float(latestMeasure['Fabbisogno Giornaliero'])

    # CC Recupero Del Deficit Energetico Corrente Dalla Scheda Dieta
    dietData = excelData['Dati Dieta']
    
    # DD Gestione Caso Scheda Dieta Vuota O Assenza Di Fasi Attive
    if len(dietData) > 0:
        latestDiet = dietData.iloc[-1]
        currentDeficit = float(latestDiet['Deficit Teorico'])
    else:
        currentDeficit = 0.0

    # EE Calcolo Della Età Attuale Dell'Utente
    currentDate = datetime.now()
    calculatedAge = currentDate.year - dobDate.year - ((currentDate.month, currentDate.day) < (dobDate.month, dobDate.day))

    # AA Calcolo Del Metabolismo Basale Con Formula Mifflin St Jeor
    if gender == "M":
        bmrMifflin = (10 * currentWeight) + (6.25 * height) - (5 * calculatedAge) + 5
    else:
        bmrMifflin = (10 * currentWeight) + (6.25 * height) - (5 * calculatedAge) - 161

    # BB Calcolo Del Metabolismo Basale Con Formula Katch McArdle
    bmrKatch = 370 + (21.6 * currentLbm)

    # CC Visualizzazione Dei Dati Estratti E Dei Calcoli Nel Terminale
    print(f"{tagProfilo}   - Età Rilevata:                 {utility.CLR_BOLD}{calculatedAge} Anni{utility.CLR_RESET}")
    print(f"{tagProfilo}   - Peso Corrente Rilevato:       {utility.CLR_BOLD}{currentWeight:.2f} Kg{utility.CLR_RESET}")
    print(f"{tagProfilo}   - Massa Magra Rilevata:         {utility.CLR_BOLD}{currentLbm:.2f} Kg{utility.CLR_RESET}")
    print(f"{tagProfilo}   - TDEE Corrente Rilevato:       {utility.CLR_BOLD}{int(currentTdee)} Kcal{utility.CLR_RESET}")
    print(f"{tagProfilo}   - Deficit Attivo Rilevato:      {utility.CLR_BOLD}{int(currentDeficit)} Kcal{utility.CLR_RESET}")
    print(f"{tagProfilo}   - BMR Mifflin-St Jeor:          {utility.CLR_BOLD}{int(bmrMifflin)} Kcal{utility.CLR_RESET}")
    print(f"{tagProfilo}   - BMR Katch-McArdle:            {utility.CLR_BOLD}{int(bmrKatch)} Kcal{utility.CLR_RESET}")

    # DD Aggiornamento Del File Excel Fisico Tramite Openpyxl
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    personalSheet = excelFile['Dati Personali']

    # EE Scrittura Valori Nella Colonna B Per Il Profilo Verticale
    personalSheet['B6'].value = int(calculatedAge)
    personalSheet['B7'].value = round(currentWeight, 2)
    personalSheet['B8'].value = round(currentLbm, 2)
    personalSheet['B9'].value = round(bmrMifflin, 0)
    personalSheet['B10'].value = round(bmrKatch, 0)
    personalSheet['B11'].value = round(currentTdee, 0)
    personalSheet['B12'].value = round(currentDeficit, 0)
    
    # AA Inserimento Timestamp Di Esecuzione Nella Nuova Cella B13
    executionTime = datetime.now()
    personalSheet['B13'].value = executionTime
    personalSheet['B13'].number_format = 'YYYY-MM-DD HH:MM:SS'

    # BB Salvataggio Delle Modifiche Nel File Excel
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Sessione
    personalDf.loc[personalDf['Parametro'] == 'Età', 'Valore'] = int(calculatedAge)
    personalDf.loc[personalDf['Parametro'] == 'Peso Corrente (Kg)', 'Valore'] = round(currentWeight, 2)
    personalDf.loc[personalDf['Parametro'] == 'Massa Magra Corrente (Kg)', 'Valore'] = round(currentLbm, 2)
    personalDf.loc[personalDf['Parametro'] == 'BMR Mifflin-St Jeor (Kcal)', 'Valore'] = round(bmrMifflin, 0)
    personalDf.loc[personalDf['Parametro'] == 'BMR Katch-McArdle (Kcal)', 'Valore'] = round(bmrKatch, 0)
    personalDf.loc[personalDf['Parametro'] == 'TDEE Corrente Pesato (Kcal)', 'Valore'] = round(currentTdee, 0)
    personalDf.loc[personalDf['Parametro'] == 'Deficit Corrente (Kcal)', 'Valore'] = round(currentDeficit, 0)
    personalDf.loc[personalDf['Parametro'] == 'Ultimo Aggiornamento', 'Valore'] = executionTime

    excelData['Dati Personali'] = personalDf

    print(f"\n{tagProfilo} {utility.CLR_BOLD}Scheda Dati Personali Aggiornata Con Successo!{utility.CLR_RESET}\n")