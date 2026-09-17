# Codice Progetto Dashboard Personale

## Cartella `privateDashboard/gadgetBridgeSync`

Contiene il file `Gadgetbridge.db`, ovvero il database SQLite generato e sincronizzato dall'applicazione Gadgetbridge per lo smartwatch.

## Cartella `privateDashboard/trackingProgress`

### File `diet.py`

```python
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
```

### File `measures.py`

```python
import pandas as pd
import numpy as np
from datetime import datetime
import openpyxl
import utility
from copy import copy

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
        dataOBJ = datetime.now().date()
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
```

### File `personal.py`

```python
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
```

### File `smartwatch.py`

```python
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
```

### File `updateTracking.py`

```python
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
```

### File `utility.py`

```python

# AA Codici Di Formattazione ANSI Per Il Terminale
# BB Colori Associati Ai Vari Moduli Del Sistema
CLR_MISURE = "\033[92m"    # Verde Chiaro Per Il Modulo Misure
CLR_ERRORE = "\033[91m"    # Rosso Chiaro Per Errori E Blocchi
CLR_RESET = "\033[0m"      # Ripristina Il Colore Di Default Del Terminale
CLR_BOLD = "\033[1m"       # Applica Il Grassetto Al Testo
CLR_PROFILO = "\033[96m"   # Azzurro/Ciano Chiaro Per Il Modulo Profilo
CLR_ALLENAMENTO = "\033[95m" # Magenta Chiaro Per Il Modulo Allenamento
CLR_PALESTRA = "\033[35m"    # Viola Per Il Modulo Della Bacheca Record Palestra
CLR_DIETA = "\033[93m"      # Giallo Chiaro Per Il Modulo Dieta
CLR_SMARTWATCH = "\033[94m" # Blu Chiaro Per Il Modulo Smartwatch

# AA Funzione Per Gestire Input Opzionali
def optionalInput(prompt):
    value = input(prompt)
    if value.strip() == "":
        return None
    else:
        # CC Conversione Diretta In Numero Se Presente
        return round(float(value), 2)

# AA Funzione Per Convertire Stringhe Di Data In Formato Standard
monthMap = {
    'gen': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'mag': '05', 'giu': '06', 'lug': '07', 'ago': '08',
    'set': '09', 'ott': '10', 'nov': '11', 'dic': '12'
}

def parseHeavyData(dateStr):
    for month, number in monthMap.items():
        dateStr = dateStr.replace(month, number)
    return dateStr
```

### File `workout.py`

```python
import json
import os
from copy import copy

import openpyxl
import pandas as pd
import utility


# AA Funzione Per Elaborare I Dati Allenamento E Generare Due DataFrame: workoutData E gymSummary
def processWorkoutData(OPENGYM_DATA, excelData):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagAllenamento = f"{utility.CLR_ALLENAMENTO}[ALLENAMENTO]{utility.CLR_RESET}"
    
    # AA Caricamento E Parsing Dati Iniziali
    # BB Caricamento Del Catalogo Esercizi Da File Locale (exercisesCatalog.json)
    baseDir = os.path.dirname(os.path.abspath(__file__))
    catalogPath = os.path.join(baseDir, "openGymData", "exercisesCatalog.json")

    exerciseCatalog = {}
    if os.path.exists(catalogPath):
        with open(catalogPath, 'r', encoding='utf-8') as f:
            exerciseCatalog = json.load(f)

    # BB Caricamento File JSON Di openGym
    with open(OPENGYM_DATA, 'r', encoding='utf-8') as f:
        openGymData = json.load(f)

    # CC Integrazione Degli Esercizi Personalizzati Presenti Nel Backup (customEx)
    for cEx in openGymData.get('customEx', []):
        exerciseCatalog[cEx['id']] = cEx.get('n', cEx['id']).title()

    # CC Estrazione Delle Sessioni E Appiattimento Dei Dati Delle Serie
    parsedRows = []
    for w in openGymData.get('workouts', []):
        wDate = w.get('d')
        wName = w.get('name', 'Allenamento')
        wNote = w.get('note', w.get('description', ''))
        startMs = w.get('start')
        endMs = w.get('end')

        for entry in w.get('entries', []):
            exId = entry.get('id')
            exTitle = exerciseCatalog.get(exId, f"Esercizio ({exId})")

            for s in entry.get('sets', []):
                # Escludiamo Eventuali Serie Non Concluse
                if not s.get('done', True):
                    continue

                parsedRows.append({
                    'start_ms': startMs,
                    'end_ms': endMs,
                    'data_str': wDate,
                    'Nome Scheda': wName,
                    'Nome Esercizio': exTitle,
                    'set_type': s.get('phase', 'normal'),
                    'Peso Serie': float(s.get('w', 0)),
                    'Ripetizioni Serie': int(s.get('r', 0)),
                    'Note Post Allenamento': wNote
                })

    workoutData = pd.DataFrame(parsedRows)

    if workoutData.empty:
        return pd.DataFrame(), pd.DataFrame()

    # BB Conversione Date E Calcolo Durata Sessione
    workoutData["Inizio Allenamento"] = pd.to_datetime(workoutData['start_ms'], unit='ms')
    workoutData["Fine Allenamento"] = pd.to_datetime(workoutData["end_ms"], unit='ms')
    workoutData["Data"] = pd.to_datetime(workoutData['data_str']).dt.date
    workoutData["Durata Allenamento"] = (workoutData["Fine Allenamento"] - workoutData["Inizio Allenamento"]).dt.total_seconds() / 60

    # BB Rimozione Colonne Non Necessarie Nel Flusso Iniziale
    columnsToRemove = ['start_ms', 'end_ms', 'data_str', 'Fine Allenamento']
    workoutData = workoutData.drop(columns=columnsToRemove)

    # BB Rimozione Righe Di Riscaldamento E Colonna Tipo Serie
    warmupMask = workoutData['set_type'] == 'warmup'
    rowToRemove = workoutData[warmupMask].index
    workoutData = workoutData.drop(rowToRemove)
    workoutData = workoutData.drop(columns=['set_type'])

    # BB Rimozione Automatica Di Cardio E Attività A Corpo Libero Senza Sovraccarico
    # CC Manteniamo Esclusivamente Le Righe Dove Viene Utilizzato Un Peso Maggiore Di Zero
    # DD Questo Filtro Esclude In Modo Dinamico Corsa, Bici, Plank, Crunch E Corpo Libero Non Zavorrato
    workoutData = workoutData[workoutData['Peso Serie'] > 0]

    # BB Adeguamento Indice Serie In Base 1 Con Ricalcolo Post-Warmup
    # CC Ricalcoliamo La Sequenza Delle Serie Allenanti Usando L'Ora Di Inizio Per Distinguere Le Sessioni Nello Stesso Giorno
    workoutData["Indice Serie"] = workoutData.groupby(['Inizio Allenamento', 'Nome Esercizio']).cumcount() + 1

    # CC Rimozione Della Colonna Di Servizio Temporale Non Più Necessaria Nel DataFrame
    workoutData = workoutData.drop(columns=['Inizio Allenamento'])

    # BB Calcolo Volume E Massimale Per Singola Serie (Espansione Dati Allenamento)
    # CC Calcolo Volume Della Singola Serie (Peso * Reps)
    workoutData["Volume Serie"] = workoutData["Peso Serie"] * workoutData["Ripetizioni Serie"]

    # CC Calcolo Massimale Stimato Di Riga Tramite Formula Epley
    # DD Formula Di Epley: Peso * (1 + Reps / 30)
    workoutData["Massimale Stimato Serie"] = workoutData["Peso Serie"] * (1 + workoutData["Ripetizioni Serie"] / 30)

    # CC Arrotondamento E Conversione In Intero Delle Nuove Metriche Di Riga
    # EE La Conversione In Int Non Genera Errori Poiché Non Vi Sono Più Valori NaN Nel Dataset
    workoutData["Volume Serie"] = workoutData["Volume Serie"].round().astype(int)
    workoutData["Massimale Stimato Serie"] = workoutData["Massimale Stimato Serie"].round().astype(int)


    # AA Setting Colonne DataFrame Per "Dati Palestra" (Bacheca Record Assoluti)
    # BB Copia Del DataFrame Master Espanso
    gymSummary = workoutData.copy()

    # BB Raggruppamento Temporaneo Per Data E Nome Esercizio (85 Sessioni)
    groupedSummary = gymSummary.groupby(['Data', 'Nome Esercizio'])

    gymSummary = groupedSummary.agg({
        'Indice Serie': 'count',
        'Ripetizioni Serie': 'mean',
        'Peso Serie': 'mean',
        'Volume Serie': 'sum',
        'Massimale Stimato Serie': 'max',
        'Note Post Allenamento': 'first'
    }).reset_index()

    # BB Rinomina Delle Metriche Aggregate Di Sessione
    renameMapGym = {
        'Indice Serie': 'Numero Serie',
        'Ripetizioni Serie': 'Ripetizioni Medie',
        'Peso Serie': 'Peso Medio',
        'Volume Serie': 'Volume Totale (Kg)',
        'Massimale Stimato Serie': 'Massimale Stimato (1RM)'
    }
    gymSummary = gymSummary.rename(columns=renameMapGym)

    # BB Approssimazione Medie E Arrotondamenti A Numeri Interi
    gymSummary['Ripetizioni Medie'] = gymSummary['Ripetizioni Medie'].round().astype(int)
    gymSummary['Peso Medio'] = gymSummary['Peso Medio'].round().astype(int)

    # BB Creazione Colonna Schema Riassuntivo Di Sessione
    # CC Utilizzo Di Una Funzione Lambda Per Formattare I Tre Parametri Chiave
    gymSummary['Schema'] = gymSummary.apply(lambda row: f"{row['Numero Serie']}x{row['Ripetizioni Medie']}x{row['Peso Medio']}kg", axis=1)

    # BB Riduzione A Un Record Assoluto Storico Per Ciascun Esercizio 
    # CC Identificazione Della Riga Con Il Massimo 1RM Storico Per Ogni Singolo Gruppo Esercizio
    gymSummary = gymSummary.loc[gymSummary.groupby('Nome Esercizio')['Massimale Stimato (1RM)'].idxmax()].reset_index(drop=True)

    # CC Ordinamento Alfabetico Degli Esercizi Per Una Migliore Resa Estetica Su Excel
    gymSummary = gymSummary.sort_values(by='Nome Esercizio').reset_index(drop=True)
    # DD -----------------------------------------------

    # EE -----------------------------------------------
    # AA Confronto Con Excel E Filtraggio Dati Allenamento Già Presenti
    existingWorkout = excelData['Dati Allenamento']

    # CC Definizione Delle Colonne Per Entrambi I DataFrame Per Garantire Coerenza Di Scrittura
    columnsWorkout = ['Data', 'Durata Allenamento', 'Nome Scheda', 'Nome Esercizio', 
                    'Indice Serie', 'Ripetizioni Serie', 'Peso Serie', 'Volume Serie', 
                    'Massimale Stimato Serie', 'Note Post Allenamento']

    columnsGym = ['Nome Esercizio', 'Schema', 'Volume Totale (Kg)', 'Data', 'Numero Serie', 
                'Ripetizioni Medie', 'Peso Medio', 'Massimale Stimato (1RM)', 'Note Post Allenamento']

    if existingWorkout.empty:
        print(f"\n{tagAllenamento} Nessun Dato Allenamento Precedente Trovato In Excel. Tutti I Dati Saranno Importati.\n")
    else:
        # CC Filtraggio Dati Allenamento Già Presenti In Excel Tramite Calcolo Della Data Massima
        existingWorkoutDate = pd.to_datetime(existingWorkout['Data']).dt.date
        lastExistingDate = existingWorkoutDate.max()
        print(f"\n{tagAllenamento} Ultima Data Allenamento Presente In Excel: {utility.CLR_BOLD}{lastExistingDate}{utility.CLR_RESET}\n")
        lastDateMask = workoutData['Data'] > lastExistingDate
        workoutData = workoutData[lastDateMask]

    # CC Riordino E Selezione Delle Colonne Eseguito In Ogni Caso (Sia Con Excel Vuoto Che Popolato)
    workoutData = workoutData[columnsWorkout]
    gymSummary = gymSummary[columnsGym]
    # EE -----------------------------------------------

    return workoutData, gymSummary

# AA Funzione Per Aggiornare Scheda Dati Allenamento In Excel Con I Nuovi Allenamenti
def updateTrainData(workoutData, excelData, EXCEL_PATH):
    # BB Definizione Dei Tag Colorati Per La Visualizzazione
    tagAllenamento = f"{utility.CLR_ALLENAMENTO}[ALLENAMENTO]{utility.CLR_RESET}"

    # BB Controllo Preliminare Se Ci Sono Nuovi Record Di Allenamento Rilevati
    if workoutData is None or len(workoutData) == 0:
        print(f"{tagAllenamento} Nessun Nuovo Allenamento Rilevato Da Inserire.\n")
        return
    else:
        print(f"{tagAllenamento} Rilevati {utility.CLR_BOLD}{len(workoutData)}{utility.CLR_RESET} Nuovi Record Da Salvare.\n")

    # CC Preparazione Dei Dati E Allineamento Colonne Per La Scheda Dati Allenamento
    dfToAppend = workoutData.copy()
    if 'Data Allenamento' in dfToAppend.columns and 'Data' not in dfToAppend.columns:
        dfToAppend = dfToAppend.rename(columns={'Data Allenamento': 'Data'})

    excelColumns = [
        'Data', 'Durata Allenamento', 'Nome Scheda', 'Nome Esercizio', 
        'Indice Serie', 'Ripetizioni Serie', 'Peso Serie', 'Volume Serie', 
        'Massimale Stimato Serie', 'Note Post Allenamento'
    ]
    dfToAppend = dfToAppend[excelColumns]

    # DD Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Aggiunta Nuove Righe
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    workoutSheet = excelFile['Dati Allenamento']

    # DD Scrittura Delle Nuove Righe Nel Foglio Di Lavoro
    for idx, row in dfToAppend.iterrows():
        # EE Creazione Della Lista Ordinata Dei Nuovi Valori Per Ciascuna Riga
        newValue = []
        for colName in excelColumns:
            val = row[colName]
            
            # Gestione Dei Valori Nulli O Incompatibili Con Excel
            if pd.isna(val):
                val = ""
                
            # Conversione Del Formato Data Di Pandas Per Evitare Errori Di Scrittura
            if colName == 'Data' and isinstance(val, pd.Timestamp):
                val = val.date()
                
            newValue.append(val)
            
        workoutSheet.append(newValue)
        lastRowIdx = workoutSheet.max_row
        
        # EE Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data, Carattere E Allineamenti)
        if lastRowIdx > 2: # Riga 1 = Intestazioni, Riga 2 = Primo Dato (Se Esiste, Copiamo Da Lì)
            for col_idx in range(1, len(newValue) + 1):
                sourceCell = workoutSheet.cell(row=lastRowIdx - 1, column=col_idx)
                targetCell = workoutSheet.cell(row=lastRowIdx, column=col_idx)
                
                # Copiamo Gli Stili E Il Formato Numerico Se Presenti (Silenziando I Falsi Positivi Di Pylance)
                if sourceCell.has_style:
                    targetCell.font = copy(sourceCell.font)  # type: ignore
                    targetCell.border = copy(sourceCell.border)  # type: ignore
                    targetCell.fill = copy(sourceCell.fill)  # type: ignore
                    targetCell.alignment = copy(sourceCell.alignment)  # type: ignore
                    targetCell.number_format = sourceCell.number_format

        else:
            # Formattazione Manuale Solo Se È La Prima Riga Di Dati In Assoluto
            # Formato Data Per La Colonna 1 (Data Allenamento)
            workoutSheet.cell(row=lastRowIdx, column=1).number_format = 'DD-MM-YYYY'
            
    # DD Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # DD Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    excelData['Dati Allenamento'] = pd.concat([excelData['Dati Allenamento'], dfToAppend], ignore_index=True)

    print(f"{tagAllenamento} {utility.CLR_BOLD}Dati Di Allenamento E Calcoli Salvati Con Successo Nel File Excel!{utility.CLR_RESET}\n")


# AA Funzione Per Ricreare La Scheda Dati Palestra In Excel Con I Nuovi Record
def updateGymData(gymSummary, excelData, EXCEL_PATH):
    # BB Definizione Dei Tag Colorati Per La Visualizzazione
    tagPalestra = f"{utility.CLR_PALESTRA}[PALESTRA]{utility.CLR_RESET}"

    # BB Controllo Preliminare Se Ci Sono Record Di Palestra Da Aggiornare
    if gymSummary is None or len(gymSummary) == 0:
        print(f"{tagPalestra} Nessun Record Rilevato Da Aggiornare.\n")
        return
    else:
        print(f"{tagPalestra} Aggiornamento Di {utility.CLR_BOLD}{len(gymSummary)}{utility.CLR_RESET} Record Storici In Corso...\n")

    # BB Preparazione Dei Dati E Allineamento Colonne Per La Scheda Dati Palestra
    dfToOverwrite = gymSummary.copy()
    
    excelColumns = [
        'Nome Esercizio', 'Schema', 'Volume Totale (Kg)', 'Data', 
        'Numero Serie', 'Ripetizioni Medie', 'Peso Medio', 
        'Massimale Stimato (1RM)', 'Note Post Allenamento'
    ]
    dfToOverwrite = dfToOverwrite[excelColumns]

    # CC Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Sovrascrittura
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    gymSheet = excelFile['Dati Palestra']

    # CC Salvataggio Degli Stili Esistenti Dalla Riga 2 Come Modello Per Il Popolamento
    styleTemplates = {}
    if gymSheet.max_row >= 2:
        for col_idx in range(1, len(excelColumns) + 1):
            cell = gymSheet.cell(row=2, column=col_idx)
            styleTemplates[col_idx] = {
                'font': copy(cell.font),
                'border': copy(cell.border),
                'fill': copy(cell.fill),
                'alignment': copy(cell.alignment),
                'number_format': cell.number_format
            }

    # CC Rimozione Di Tutti I Record Esistenti Dalla Scheda Per Consentire La Sovrascrittura Completa
    if gymSheet.max_row > 1:
        gymSheet.delete_rows(2, amount=gymSheet.max_row)

    # CC Scrittura Dei Nuovi Record Nel Foglio Di Lavoro
    for idx, row in dfToOverwrite.iterrows():
        # CC Creazione Della Lista Ordinata Dei Nuovi Valori Per Ciascuna Riga
        newValue = []
        for colName in excelColumns:
            val = row[colName]
            
            # EE Gestione Dei Valori Nulli O Incompatibili Con Excel
            if pd.isna(val):
                val = ""
                
            # EE Conversione Del Formato Data Di Pandas Per Evitare Errori Di Scrittura
            if colName == 'Data' and isinstance(val, pd.Timestamp):
                val = val.date()
                
            newValue.append(val)
            
        gymSheet.append(newValue)
        lastRowIdx = gymSheet.max_row
        
        # DD Copia Della Formattazione Tramite I Modelli Salvati In Precedenza
        if len(styleTemplates) > 0:
            for col_idx in range(1, len(newValue) + 1):
                targetCell = gymSheet.cell(row=lastRowIdx, column=col_idx)
                tpl = styleTemplates[col_idx]
                
                # Copiamo Gli Stili E Il Formato Numerico (Silenziando I Falsi Positivi Di Pylance)
                targetCell.font = copy(tpl['font'])  # type: ignore
                targetCell.border = copy(tpl['border'])  # type: ignore
                targetCell.fill = copy(tpl['fill'])  # type: ignore
                targetCell.alignment = copy(tpl['alignment'])  # type: ignore
                targetCell.number_format = tpl['number_format']
        else:
            # EE Formattazione Manuale Solo Se La Scheda Era Completamente Vuota
            # Formato Data Per La Colonna 4 (Data)
            gymSheet.cell(row=lastRowIdx, column=4).number_format = 'DD-MM-YYYY'

    # CC Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    excelData['Dati Palestra'] = dfToOverwrite

    print(f"{tagPalestra} {utility.CLR_BOLD}Record Storici Personali Aggiornati E Salvati Con Successo!{utility.CLR_RESET}\n")
```

## Cartella `privateDashboard/trackingProgress/openGymData`

### File `downloadCatalog.py`

```python
import json
import os
import urllib.request

print("Scaricamento Catalogo openGym In Corso...")

# 1. URL del database ufficiale degli esercizi
url = "https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/data/exercises.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

# 2. Richiesta HTTP e decodifica dei dati JSON
with urllib.request.urlopen(req, timeout=15) as response:
    raw_exercises = json.loads(response.read().decode('utf-8'))

# 3. Creazione immediata del dizionario ID -> Nome (con iniziale maiuscola)
catalog = {item['id']: item['name'].title() for item in raw_exercises}

# 4. Percorso della cartella dove si trova questo script
current_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(current_dir, "exercisesCatalog.json")

# 5. Salvataggio su file JSON locale
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print("Catalogo Salvato Con Successo!")
print(f"Totale Esercizi: {len(catalog)}")
print(f"File Salvato In: {output_path}")
```

### File `exercisesCatalog.json`

File che contiene il catalogo degli esercizi scaricato da openGym, mappando gli ID degli esercizi ai loro nomi. Ecco un esempio del contenuto del file:

```json
{
  "0001": "3/4 Sit-Up",
  "0002": "45° Side Bend",
  "0003": "Air Bike",
  "1512": "All Fours Squad Stretch",
  "0006": "Alternate Heel Touchers",
  "0007": "Alternate Lateral Pulldown",
  "1368": "Ankle Circles",
  "3293": "Archer Pull Up"
}
```