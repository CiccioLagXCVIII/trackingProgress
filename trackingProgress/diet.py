import pandas as pd
import numpy as np
import openpyxl
from copy import copy
import utility


def updateDietData(excelData, EXCEL_PATH):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagDieta = f"{utility.CLR_DIETA}[DIETA]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # AA Caricamento E Inizializzazione Dei Dati Da Excel
    dietData = excelData['Dati Dieta']
    measureData = excelData['Dati Misure']

    # BB Controllo Di Sicurezza Sulla Presenza Di Misurazioni Corporee Precedenti
    # CC Impedisce L'Inserimento Se Non Abbiamo Peso E TDEE Di Riferimento
    if len(measureData) == 0:
        print(f"\n{tagErrore} Nessuna Misurazione Rilevata Nella Scheda 'Dati Misure'.")
        print(f"{tagErrore} Inserisci Almeno Una Misurazione Corporea Prima Di Configurare La Dieta.\n")
        return

    # BB Controllo Se La Scheda Dati Dieta È Vuota Per Evitare Errori Di Indice
    if len(dietData) == 0:
        print(f"{tagDieta} Nessun Record Dieta Precedente Rilevato.\n")
    else:
        # BB Recupero E Stampa Dell'Ultimo Record Dieta Registrato
        # CC Lettura Dei Valori Dell'Ultima Riga Nel Foglio Excel
        lastRow = dietData.iloc[-1]
        dataInizioLastOBJ = pd.to_datetime(lastRow['Data Inizio'])

        # CC Controllo Se La Data Fine Dell'Ultimo Record È Vuota (Piano Ancora Attivo)
        if pd.isna(lastRow['Data Fine']):
            print(f"\n{tagDieta} Rilevato Un Piano Alimentare Precedente Ancora Attivo (Senza Data Fine).")
            print(f"{tagDieta} Data Inizio Del Piano Attivo: {utility.CLR_BOLD}{dataInizioLastOBJ.strftime('%d-%m-%Y')}{utility.CLR_RESET}")
            
            # DD Richiesta Obbligatoria Della Data Fine Per Chiudere Il Piano Precedente
            while True:
                dataFineLastStr = input(f"{tagDieta} Inserisci La Data Fine Per Chiudere Questo Piano (GG-MM-AAAA): ")
                try:
                    dataFineLastOBJ = pd.to_datetime(dataFineLastStr, format='%d-%m-%Y')
                    if dataFineLastOBJ.date() < dataInizioLastOBJ.date():
                        print(f"{tagErrore} La Data Fine Deve Essere Successiva O Uguale Alla Data Inizio ({dataInizioLastOBJ.strftime('%d-%m-%Y')}).")
                        continue
                    break
                except ValueError:
                    print(f"{tagErrore} Formato Data Non Valido. Riprova.")
            
            # DD Calcolo Della Durata Per Il Piano Precedente
            durataLast = (dataFineLastOBJ.date() - dataInizioLastOBJ.date()).days + 1
            
            # EE Scrittura Della Chiusura Nel File Excel Fisico Con Openpyxl
            excelFile = openpyxl.load_workbook(EXCEL_PATH)
            dietSheet = excelFile['Dati Dieta']
            lastRowIdx = dietSheet.max_row
            
            # EE Colonna 2 Per Data Fine E Colonna 3 Per Durata
            dietSheet.cell(row=lastRowIdx, column=2).value = dataFineLastOBJ.date() # type: ignore
            dietSheet.cell(row=lastRowIdx, column=3).value = int(durataLast)        # type: ignore
            
            excelFile.save(EXCEL_PATH)
            excelFile.close()
            
            # EE Sincronizzazione Del DataFrame In Memoria
            dietData.loc[dietData.index[-1], 'Data Fine'] = dataFineLastOBJ
            dietData.loc[dietData.index[-1], 'Durata'] = int(durataLast)
            excelData['Dati Dieta'] = dietData
            
            print(f"{tagDieta} {utility.CLR_BOLD}Piano Precedente Chiuso Con Successo!{utility.CLR_RESET}\n")
            
            # EE Ricarica Della Riga Aggiornata Per La Stampa Successiva
            lastRow = dietData.iloc[-1]

        # CC Recupero E Stampa Dell'Ultimo Record Dieta Registrato (Ora Sicuramente Chiuso)
        dataInizioOBJ = pd.to_datetime(lastRow['Data Inizio'])
        dataFineOBJ = pd.to_datetime(lastRow['Data Fine'])
        
        # DD Formattazione Protetta Delle Date In Stringhe Per La Stampa A Video
        dataInizio = dataInizioOBJ.strftime("%d-%m-%Y") if not pd.isna(dataInizioOBJ) else "Non Specificata"
        dataFine = dataFineOBJ.strftime("%d-%m-%Y") if not pd.isna(dataFineOBJ) else "In Corso"
        
        kcal = lastRow['Kcal']
        carbo = lastRow['Carbo (g)']
        grassi = lastRow['Grassi (g)']
        proteine = lastRow['Proteine (g)']

        print(f"{tagDieta} Ultima Entry: {utility.CLR_BOLD}{dataInizio} - {dataFine}{utility.CLR_RESET} | "
              f"Kcal: {utility.CLR_BOLD}{kcal}{utility.CLR_RESET} | "
              f"C: {utility.CLR_BOLD}{carbo}g{utility.CLR_RESET} | "
              f"G: {utility.CLR_BOLD}{grassi}g{utility.CLR_RESET} | "
              f"P: {utility.CLR_BOLD}{proteine}g{utility.CLR_RESET}\n")
    
    print(f"{tagDieta} Inserisci I Nuovi Dati Dieta:")

    # BB Richiesta Input All Utente Per I Nuovi Record Alimentari
    # CC Parsing Delle Date Con Formato Giorno Primo E Ciclo Di Validazione
    while True:
        inizioNewStr = input(f"{tagDieta} Inserisci Data Inizio (DD-MM-YYYY): ")
        try:
            inizioNew = pd.to_datetime(inizioNewStr, format='%d-%m-%Y')
            break
        except ValueError:
            print(f"{tagErrore} Formato Data Non Valido. Riprova.")

    # CC Richiesta Data Fine Opzionale Con Ciclo Di Validazione
    while True:
        dataFineNewStr = input(f"{tagDieta} Inserisci Data Fine (DD-MM-YYYY) [Opzionale, premi Invio per lasciare aperto]: ")
        if dataFineNewStr.strip() == "":
            dataFineNew = None
            break
        try:
            dataFineNew = pd.to_datetime(dataFineNewStr, format='%d-%m-%Y')
            if dataFineNew.date() < inizioNew.date():
                print(f"{tagErrore} La Data Fine Deve Essere Successiva O Uguale Alla Data Inizio.")
                continue
            break
        except ValueError:
            print(f"{tagErrore} Formato Data Non Valido. Riprova.")

    # BB Richiesta Input All'Utente Per I Nuovi Record Alimentari
    # CC Parsing Delle Date Con Formato Giorno Primo Per Evitare Errori Di Conversione
    kcalNew = int(input(f"{tagDieta} Inserisci Kcal:                     "))
    carboNew = int(input(f"{tagDieta} Inserisci Carboidrati (g):           "))
    grassiNew = int(input(f"{tagDieta} Inserisci Grassi (g):                 "))
    proteineNew = int(input(f"{tagDieta} Inserisci Proteine (g):               "))
    noteNew = input(f"{tagDieta} Inserisci Note (Opzionale):          ")

    # BB Calcolo Dei Parametri Temporali E Confronto Con La Scheda Misure
    # CC Calcolo Della Durata Complessiva Della Nuova Fase Dieta (Solo Se Presente)
    if dataFineNew is not None:
        durataNew = (dataFineNew - inizioNew).days + 1
        dataFineValueExcel = dataFineNew.date()
        durataValueExcel = int(durataNew)
    else:
        durataNew = None
        dataFineValueExcel = None
        durataValueExcel = None

    # CC Recupero Dei Dati Antropometrici Più Recenti Dalla Scheda Misure
    pesoMeasure = measureData['Peso (Kg)'].iloc[-1]

    # DD Calcolo Delle Proteine Giornaliere Rapportate Al Peso Corporeo Dell'Atleta
    proteinePerPeso = proteineNew / pesoMeasure

    # DD Recupero Del Fabbisogno Corretto Dalla Colonna Esistente In Excel
    fabbisognoMeasure = measureData['Fabbisogno Giornaliero'].iloc[-1]

    # DD Calcolo Del Deficit Energetico Rispetto Al Fabbisogno Stimato
    deficitTeorico = fabbisognoMeasure - kcalNew

    # BB Calcolo Delle Percentuali Dei Macronutrienti Rispetto Alle Calorie Totali
    # DD Calcolo Dei Rapporti Decimali Per La Gestione Delle Celle Percentuali In Excel
    percentualeCarbo = (carboNew * 4) / kcalNew
    percentualeGrassi = (grassiNew * 9) / kcalNew
    percentualeProteine = (proteineNew * 4) / kcalNew

    # BB Controllo Di Coerenza Energetica Tra Calorie Inserite E Calcolate
    # DD Calcolo Energetico Tramite Moltiplicatori Standard Dei Macronutrienti
    kcalCalcolate = (carboNew * 4) + (grassiNew * 9) + (proteineNew * 4)

    # CC Verifica Di Corrispondenza E Gestione Dello Script In Caso Di Errore
    if kcalCalcolate != kcalNew:
        # EE Errore Di Inserimento Con Arresto Di Sicurezza Dello Script
        print(f"\n{tagErrore} Le Kcal Calcolate ({kcalCalcolate}) Non Corrispondono A Quelle Inserite ({kcalNew}).\n")
        return
    else:
        # EE Messaggio Di Conferma Se Il Bilancio Energetico Risulta Corretto
        print(f"\n{tagDieta} Kcal Calcolate: {utility.CLR_BOLD}{kcalCalcolate}{utility.CLR_RESET} | "
          f"Kcal Inserite: {utility.CLR_BOLD}{kcalNew}{utility.CLR_RESET} | "
          f"{utility.CLR_BOLD}OK{utility.CLR_RESET}\n")

    # AA Inserimento Dei Valori Calcolati Nella Scheda "Dati Dieta"

    # BB Creazione Della Lista Ordinata Dei Nuovi Valori
    # CC Conversione Delle Date Di Pandas Nel Formato Data Nativo Per Excel
    if dataFineNew is not None:
        dataFineNew = dataFineNew.date()
    else:
        dataFineNew = None
    
    if durataNew is not None:
        durataNew = int(durataNew)
    else:
        durataNew = None
    newValue = [
        inizioNew.date(),               # Data Inizio (Colonna 1)
        dataFineNew,                    # Data Fine (Colonna 2)
        durataNew,                      # Durata (Colonna 3)
        int(kcalNew),                   # Kcal (Colonna 4)
        int(round(deficitTeorico, 0)),  # Deficit Teorico (Colonna 5)
        int(carboNew),                  # Carbo (g) (Colonna 6)
        int(grassiNew),                 # Grassi (g) (Colonna 7)
        int(proteineNew),               # Proteine (g) (Colonna 8)
        round(proteinePerPeso, 2),      # Proteine (g/Kg) (Colonna 9)
        round(percentualeCarbo, 4),     # % Carbo (Colonna 10)
        round(percentualeGrassi, 4),    # % Grassi (Colonna 11)
        round(percentualeProteine, 4),  # % Proteine (Colonna 12)
        noteNew                         # Note (Colonna 13)
    ]

    # BB Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Aggiunta Nuova Riga
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    dietSheet = excelFile['Dati Dieta']

    dietSheet.append(newValue)

    # CC Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data E Percentuale)
    # CC Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data E Percentuale)
    lastRowIdx = dietSheet.max_row

    if lastRowIdx > 2: # Riga 1 = Intestazioni, Riga 2 = Primo Dato (Se Esiste, Copiamo Da Lì)
        for col_idx in range(1, len(newValue) + 1):
            sourceCell = dietSheet.cell(row=lastRowIdx - 1, column=col_idx)
            targetCell = dietSheet.cell(row=lastRowIdx, column=col_idx)
            
            # Copiamo Gli Stili E Il Formato Numerico Se Presenti (Silenziando I Falsi Positivi Di Pylance)
            if sourceCell.has_style:
                targetCell.font = copy(sourceCell.font)  # type: ignore
                targetCell.border = copy(sourceCell.border)  # type: ignore
                targetCell.fill = copy(sourceCell.fill)  # type: ignore
                targetCell.alignment = copy(sourceCell.alignment)  # type: ignore
                targetCell.number_format = sourceCell.number_format
    else:
        # DD Formattazione Manuale Solo Se È La Prima Riga Di Dati In Assoluto
        # Formato Decimale Per La Colonna 9 (Proteine (g/Kg))
        dietSheet.cell(row=lastRowIdx, column=9).number_format = '0.0'
        # Formato Percentuale Per La Colonna 10 (% Carbo)
        dietSheet.cell(row=lastRowIdx, column=10).number_format = '0.0%'
        # Formato Percentuale Per La Colonna 11 (% Grassi)
        dietSheet.cell(row=lastRowIdx, column=11).number_format = '0.0%'
        # Formato Percentuale Per La Colonna 12 (% Proteine)
        dietSheet.cell(row=lastRowIdx, column=12).number_format = '0.0%'

    # EE Forza Esplicitamente Il Formato GG-MM-AAAA Sulle Colonne Delle Date
    # EE Questo Evita Che Openpyxl Ripristini Il Formato ISO Default AAAA-MM-GG
    dietSheet.cell(row=lastRowIdx, column=1).number_format = 'dd/mm/yy;@'
    dietSheet.cell(row=lastRowIdx, column=2).number_format = 'dd/mm/yy;@'

    # BB Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    dfToAppend = pd.DataFrame([{
        'Data Inizio': pd.to_datetime(inizioNew),
        'Data Fine': pd.to_datetime(dataFineNew) if dataFineNew is not None else pd.NaT,
        'Durata': int(durataNew) if durataNew is not None else np.nan,
        'Kcal': int(kcalNew),
        'Deficit Teorico': int(round(deficitTeorico, 0)),
        'Carbo (g)': int(carboNew),
        'Grassi (g)': int(grassiNew),
        'Proteine (g)': int(proteineNew),
        'Proteine (g/Kg)': round(proteinePerPeso, 2),
        '% Carbo': round(percentualeCarbo, 4),
        '% Grassi': round(percentualeGrassi, 4),
        '% Proteine': round(percentualeProteine, 4),
        'Note': noteNew
    }])

    excelData['Dati Dieta'] = pd.concat([excelData['Dati Dieta'], dfToAppend], ignore_index=True)

    print(f"\n{tagDieta} {utility.CLR_BOLD}Piano Alimentare E Calcoli Salvati Con Successo Nel File Excel!{utility.CLR_RESET}\n")