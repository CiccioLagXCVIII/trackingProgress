from copy import copy
from datetime import datetime, timezone

import numpy as np
import openpyxl
import pandas as pd
import utility


def updateMeasuresData(excelData, EXCEL_PATH):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagMisure = f"{utility.CLR_MISURE}[MISURE]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # AA Recupero Delle Misurazioni Più Recenti
    personalData = excelData['Dati Personali']
    
    # BB Estrazione Dei Valori Dal Layout Verticale Usando .loc
    gender = personalData.loc[personalData['Parametro'] == 'Sesso', 'Valore'].iloc[0]
    heightRaw = personalData.loc[personalData['Parametro'] == 'Altezza (cm)', 'Valore'].iloc[0]
    
    # CC Conversione Protetta Dell'Altezza In Valore Numerico Decimale
    height = float(heightRaw)
    
    # BB Accesso Alla Scheda "Dati Misure"
    measureData = excelData['Dati Misure']

    # AA Inserimento Misurazioni Data Odierna O Specifica
    # BB Controllo Se La Scheda Dati Misure È Vuota Per Evitare Errori Di Indice
    if len(measureData) == 0:
        print(f"{tagMisure} Nessuna Misurazione Precedente Rilevata.\n")
        ultimaDataOBJ = None
        ultimaData = "Nessuna"
    else:
        # BB Stampa Data Ultima Misurazione
        ultimaDataOBJ = pd.to_datetime(measureData['Data Misurazione'].iloc[-1])
        ultimaData = ultimaDataOBJ.strftime("%d-%m-%Y")
        print(f"\n{tagMisure} Ultima Misurazione Registrata: {utility.CLR_BOLD}{ultimaData}{utility.CLR_RESET}\n")

    # BB Chiedi Se Vuoi Aggiungere Misurazioni Oggi O In Data Specifica
    print(f"{tagMisure} Seleziona Cosa Vuoi Fare:")
    print(f"{tagMisure}   1. Inserimento Misurazioni Oggi")
    if ultimaDataOBJ is not None:
        print(f"{tagMisure}   2. Inserimento Data Specifica (Successiva A {ultimaData})\n")
    else:
        print(f"{tagMisure}   2. Inserimento Data Specifica\n")
        
    scelta = input(f"{tagMisure} Inserisci Numero Corrispondente: ")

    if scelta == "1":
        dataOBJ = datetime.now(timezone.utc).date()
        data = dataOBJ.strftime("%d-%m-%Y")
        print(f"\n{tagMisure} Inserimento Misurazioni Data: {utility.CLR_BOLD}{data}{utility.CLR_RESET}\n")

    elif scelta == "2":
        dataInput = input(f"\n{tagMisure} Inserisci Data Specifica (GG-MM-AAAA): ")
        dataOBJ = pd.to_datetime(dataInput, format='%d-%m-%Y').date()
        if ultimaDataOBJ is not None and dataOBJ <= ultimaDataOBJ.date():
            print(f"\n{tagErrore} La Data Inserita Deve Essere Successiva A {ultimaData}\n")
            return
        data = dataOBJ.strftime("%d-%m-%Y")
        print(f"{tagMisure} Inserimento Misurazioni Data: {utility.CLR_BOLD}{data}{utility.CLR_RESET}\n")

    pesoNew = float(input(f"{tagMisure} Inserisci Peso (Kg):                  "))
    colloNew = float(input(f"{tagMisure} Inserisci Circonferenza Collo (cm):   "))
    vitaNew = float(input(f"{tagMisure} Inserisci Circonferenza Vita (cm):    "))
    fianchiNew = float(input(f"{tagMisure} Inserisci Circonferenza Fianchi (cm): "))
    braccioNew = utility.optionalInput(f"{tagMisure} Inserisci Circonferenza Braccio (cm) [Opzionale]: ")
    cosciaNew = utility.optionalInput(f"{tagMisure} Inserisci Circonferenza Coscia (cm)  [Opzionale]: ")
    
    # AA Calcolo Valori Scheda Con Dati Aggiornati

    # BB Massa Grassa, Massa Magra E Metabolismo Basale (BMR)
    # CC Massa Grassa E Massa Magra Tramite Formula US Navy Dinamica Per Sesso
    if gender == "M":
        usNavyBF = ( 495 / (1.0324 - 0.19077 * np.log10(vitaNew - colloNew) + 0.15456 * np.log10(height)) ) - 450
    else:
        usNavyBF = ( 495 / (1.29579 - 0.35004 * np.log10(vitaNew + fianchiNew - colloNew) + 0.22100 * np.log10(height)) ) - 450

    massaGrassa = pesoNew * (usNavyBF / 100)
    massaMagra = pesoNew - massaGrassa

    # CC Metabolismo Basale (BMR) - Formula Katch-McArdle
    metabolismoBasale = 370 + (21.6 * massaMagra)

    # DD Fabbisogno Energetico Giornaliero (TDEE)
    tdeeAllenamento = metabolismoBasale * 1.55  # Moderato
    tdeeRiposo = metabolismoBasale * 1.2        # Sedentario
    tdeeMedio = (tdeeAllenamento * 3 + tdeeRiposo * 4) / 7

    # AA Inserimento Dei Valori Calcolati Nella Scheda "Dati Misure"
    # BB Creazione Della Lista Ordinata Dei Nuovi Valori
    # Se In Excel Hai Impostato La Cella Come "Percentuale" Si Deve Dividere Per 100, Perché Excel Gestisce Le Percentuali Come Decimali.
    newValue = [
        dataOBJ,                        # Data Misurazione
        round(pesoNew, 2),              # Peso (Kg)
        round(colloNew, 2),             # Circonferenza Collo (cm)
        round(vitaNew, 2),              # Circonferenza Vita (cm)
        round(fianchiNew, 2),           # Circonferenza Fianchi (cm)
        braccioNew,                     # Circonferenza Braccio (cm)
        cosciaNew,                      # Circonferenza Coscia (cm)
        round(usNavyBF / 100, 4),       # Massa Grassa (%)
        round(massaMagra, 2),           # Massa Magra (Kg)
        round(metabolismoBasale, 0),    # Metabolismo Basale
        round(tdeeMedio, 0)             # Fabbisogno Giornaliero
    ]

    # BB Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Aggiunta Nuova Riga
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    measureSheet = excelFile['Dati Misure']

    measureSheet.append(newValue)

    # CC Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data E Percentuale)
    lastRowIdx = measureSheet.max_row

    if lastRowIdx > 2: # Riga 1 = Intestazioni, Riga 2 = Primo Dato (Se Esiste, Copiamo Da Lì)
        for col_idx in range(1, len(newValue) + 1):
            sourceCell = measureSheet.cell(row=lastRowIdx - 1, column=col_idx)
            targetCell = measureSheet.cell(row=lastRowIdx, column=col_idx)
            
            # Copiamo Gli Stili E Il Formato Numerico Se Presenti (Silenziando I Falsi Positivi Di Pylance)
            if sourceCell.has_style:
                targetCell.font = copy(sourceCell.font)  # type: ignore
                targetCell.border = copy(sourceCell.border)  # type: ignore
                targetCell.fill = copy(sourceCell.fill)  # type: ignore
                targetCell.alignment = copy(sourceCell.alignment)  # type: ignore
                targetCell.number_format = sourceCell.number_format
    else:
        # DD Formattazione Manuale Solo Se È La Prima Riga Di Dati In Assoluto
        # Formato Data Per La Colonna 1 (Data Misurazione)
        measureSheet.cell(row=lastRowIdx, column=1).number_format = 'DD-MM-YYYY'
        # Formato Percentuale Per La Colonna 8 (Massa Grassa (%))
        measureSheet.cell(row=lastRowIdx, column=8).number_format = '0.0%'

    # BB Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    dfToAppend = pd.DataFrame([{
        'Data Misurazione': pd.to_datetime(dataOBJ),
        'Peso (Kg)': round(pesoNew, 2),
        'Circonferenza Collo (cm)': round(colloNew, 2),
        'Circonferenza Vita (cm)': round(vitaNew, 2),
        'Circonferenza Fianchi (cm)': round(fianchiNew, 2),
        'Circonferenza Braccio (cm)': braccioNew,
        'Circonferenza Coscia (cm)': cosciaNew,
        'Massa Grassa (%)': round(usNavyBF / 100, 4),
        'Massa Magra (Kg)': round(massaMagra, 2),
        'Metabolismo Basale': round(metabolismoBasale, 0),
        'Fabbisogno Giornaliero': round(tdeeMedio, 0)
    }])
    
    excelData['Dati Misure'] = pd.concat([excelData['Dati Misure'], dfToAppend], ignore_index=True)

    print(f"\n{tagMisure} {utility.CLR_BOLD}Misurazioni E Calcoli Salvati Con Successo Nel File Excel!{utility.CLR_RESET}\n")