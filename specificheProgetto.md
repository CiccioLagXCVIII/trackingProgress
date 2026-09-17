# Specifiche di Progetto — Dashboard Personale

Documento di riferimento tecnico: descrive cosa esiste già, le decisioni architetturali prese durante la progettazione, e cosa resta da implementare. Ad uso interno, complementare al `README.md` (più discorsivo e pensato per chi guarda il repository dall'esterno).

---

## 1. Obiettivo del progetto

Costruire una dashboard web multi-pagina, **da eseguire in locale**, che visualizzi graficamente tutti i dati raccolti nel tempo su: profilo fisico, misurazioni corporee, fasi alimentari, allenamenti in palestra, record personali e attività dello smartwatch (inclusi sonno e parametri vitali). I dati sono già raccolti e calcolati da un tool CLI Python esistente e funzionante; la dashboard è un livello di visualizzazione aggiuntivo, non sostituisce il tool CLI.

---

## 2. Cosa esiste già (componenti attuali)

### 2.1 Tool CLI — `trackingProgress/`

Applicazione a menu testuale (`updateTracking.py`), già funzionante, che carica in memoria i fogli di un file Excel (`trackingProgressi.xlsx`) come DataFrame pandas e li aggiorna in base alle scelte dell'utente, preservando stili e formattazione con `openpyxl`.

| Modulo | Funzione | Foglio Excel scritto |
|---|---|---|
| `measures.py` | Inserisce nuove misurazioni corporee (peso, circonferenze), calcola massa grassa (formula US Navy), massa magra, BMR Katch-McArdle e TDEE pesato (allenamento/riposo) | Dati Misure |
| `diet.py` | Chiude la fase alimentare precedente (se aperta), registra una nuova fase con kcal/macro, verifica coerenza energetica (kcal dichiarate vs calcolate), calcola deficit teorico e percentuali macro | Dati Dieta |
| `personal.py` | Ricalcola il profilo corrente (età, BMR Mifflin-St Jeor e Katch-McArdle, TDEE, deficit attivo) a partire dall'ultima riga di Misure e Dieta; **sovrascrive sempre la stessa riga**, quindi non mantiene storico proprio | Dati Personali |
| `workout.py` | Importa sessioni da un export JSON di OpenGym, calcola volume e massimale stimato (Epley) per serie, filtra il riscaldamento e le serie a corpo libero, aggiorna lo storico allenamenti e ricalcola la bacheca record assoluti per esercizio | Dati Allenamento, Dati Palestra |
| `smartwatch.py` | Legge `Gadgetbridge.db`, rileva il dispositivo associato, e per la famiglia Xiaomi/Redmi/Poco estrae 4 DataFrame: attività al minuto, riepilogo giornaliero, sessioni sonno e timeline dettagliata fasi sonno. **Non ancora collegato a salvataggio permanente** | Nessuno (solo in memoria) |
| `utility.py` | Costanti colore per il terminale, funzione di input opzionale | — |
| `openGymData/downloadCatalog.py` | Scarica e salva localmente il catalogo esercizi (ID → nome) da una fonte online | `exercisesCatalog.json` |

### 2.2 Schema dati Excel esistente (5 fogli)

- **Dati Personali** (layout verticale parametro/valore): Sesso, Altezza, Data di Nascita, Età, Peso Corrente, Massa Magra Corrente, BMR Mifflin-St Jeor, BMR Katch-McArdle, TDEE Corrente Pesato, Deficit Corrente, Ultimo Aggiornamento.
- **Dati Misure** (una riga per misurazione): Data Misurazione, Peso, Circonferenza Collo/Vita/Fianchi/Braccio/Coscia, Massa Grassa %, Massa Magra, Metabolismo Basale (Katch-McArdle), Fabbisogno Giornaliero (TDEE pesato).
- **Dati Dieta** (una riga per fase alimentare): Data Inizio, Data Fine, Durata, Kcal, Deficit Teorico, Carbo/Grassi/Proteine (g), Proteine (g/Kg), % Carbo/Grassi/Proteine, Note.
- **Dati Allenamento** (una riga per serie): Data, Durata Allenamento, Nome Scheda, Nome Esercizio, Indice Serie, Ripetizioni Serie, Peso Serie, Volume Serie, Massimale Stimato Serie, Note.
- **Dati Palestra** (una riga per esercizio, solo il record storico): Nome Esercizio, Schema (es. "3x10x80kg"), Volume Totale, Data del record, Numero Serie, Ripetizioni Medie, Peso Medio, Massimale Stimato (1RM), Note.

### 2.3 Dati smartwatch (`Gadgetbridge.db`)

Il modulo `smartwatch.py` interroga le tabelle del protocollo Xiaomi Wear:
- `DEVICE` — rilevamento e matching del dispositivo.
- `XIAOMI_ACTIVITY_SAMPLE` — dati al minuto: passi, battito, SpO2, stress, distanza, calorie attive, tipo attività.
- `XIAOMI_DAILY_SUMMARY_SAMPLE` — riepiloghi giornalieri: passi totali, calorie, battito (riposo/medio/min/max con orari), stress (medio/max/min), SpO2 medio, ore in piedi, indice vitalità.
- `XIAOMI_SLEEP_TIME_SAMPLE` — sessioni aggregate di sonno per notte: ora inizio, ora fine, durata totale, sonno profondo, sonno leggero, sonno REM, tempo sveglio.
- `XIAOMI_SLEEP_STAGE_SAMPLE` — timeline dettagliata delle fasi notturne (Deep, Light, REM, Awake) calcolate per intervalli temporali.

Restituisce 4 DataFrame pronti per la sincronizzazione: `activityData`, `dailySummary`, `sleepSessions`, `sleepStages`.

### 2.4 Bug/lacune da completare

- Nel menu di `updateTracking.py`, l'opzione **"4. Sincronizza Smartwatch" non chiama `processSmartwatchData()`**: stampa solo un messaggio segnaposto. Va implementata per invocare `dashboardSync.py`.
- I dati estratti da `smartwatch.py` vivono solo in memoria durante l'esecuzione del test: serve il salvataggio persistente nel database `dashboardData.db`.

### 2.5 Cosa è stato preparato finora per la nuova parte del progetto

- Repository Git **privata** creata, con `.gitignore` che esclude `Gadgetbridge.db`, `XiaomiTokenExtractor/`, `dashboardData.db`, `venv/`.
- Cartella `smartwatch/` eliminata e consolidata nel file unico flat `trackingProgress/smartwatch.py`.
- Scaffold di cartelle e file vuoti pronto per `dashboardSync.py` e per l'intera cartella `dashboardWeb/` (`routes/`, `services/`, `templates/`, `static/`).

---

## 3. Decisioni architetturali prese

| Argomento | Decisione |
|---|---|
| Frontend | HTML + CSS + Bootstrap, nessun framework JS (no React/Vue/Svelte, no build tool) |
| Grafici | Plotly.js, per l'interattività su zoom/pan/drill-down temporale |
| Backend | Flask + Jinja2 (server-side rendering, niente API pubblica necessaria) |
| Storage dashboard | Nuovo SQLite dedicato (`dashboardData.db`), generato/aggiornato da uno script di sync, mai scritto/letto da Excel direttamente dal lato web |
| Excel esistente | Resta **invariato** nel funzionamento: continua ad essere l'unica fonte scritta dal tool CLI |
| Storicizzazione Dati Personali | **Non serve** una tabella di log separata: TDEE, BMR (Katch-McArdle e Mifflin-St Jeor) e Deficit nel tempo si derivano durante la sync direttamente dallo storico già presente in Dati Misure (che salva già BMR/TDEE per ogni riga) e Dati Dieta (che salva già il deficit per fase), più le costanti da Dati Personali (altezza, sesso, data di nascita) per ricalcolare l'età storica |
| Affidabilità dati storici | Le misurazioni corporee precedenti all'1 giugno 2026 vengono mostrate nei grafici ma segnalate visivamente come meno affidabili |
| Flusso di aggiornamento | Nessuna sincronizzazione automatica: si lancia manualmente `updateTracking.py`, si usa l'opzione smartwatch per eseguire `dashboardSync.py`, poi si apre la dashboard separatamente per guardare i dati |
| Supporto dispositivi | Esclusivo per la famiglia Xiaomi / Redmi / Poco in un unico file `smartwatch.py`. Eventuali altri brand saranno gestiti tramite modifiche/fork futuri della community |
| Sonno | Completamente integrato nell'estrazione (sessioni e timeline fasi) e pronto per la visualizzazione nella pagina Smartwatch |
| Grafico incrociato Dieta/Misure | Sì, previsto: target kcal/deficit sovrapposto al peso reale nel tempo |
| Frequenza allenamenti | Heatmap calendario in stile GitHub (contribution graph) |
| Convenzioni di stile codice | Si mantiene lo stile già presente nel progetto (camelCase, commenti/nomi in italiano) anche nei file nuovi |

---

## 4. Specifica dettagliata per pagina

### Home
Card di stato con i valori correnti di Dati Personali (età, peso, massa magra, BMR Mifflin-St Jeor, BMR Katch-McArdle, TDEE, deficit attivo, data ultimo aggiornamento), più un piccolo trend storico di TDEE/BMR/deficit calcolato durante la sync, e card di richiamo dalle altre pagine (peso recente, sessioni allenamento recenti, fase dieta attiva).

### Dieta
Timeline delle fasi (kcal per fase, a gradini/barre), ripartizione macro (torta per la fase attiva, barre impilate per lo storico), proteine g/kg nel tempo, deficit teorico nel tempo, grafico incrociato target kcal/deficit vs peso reale (da Misure). Tabella fasi con note.

### Misure
Peso nel tempo, massa grassa % nel tempo, massa magra nel tempo, circonferenze corporee (collo/vita/fianchi/braccio/coscia) come multi-linea, BMR/TDEE nel tempo. Dati precedenti all'1 giugno 2026 mostrati con segnalazione di minore affidabilità.

### Allenamento
Volume totale per sessione nel tempo, durata allenamento nel tempo, heatmap calendario stile GitHub per la frequenza delle sessioni, filtro per esercizio specifico con andamento di peso/ripetizioni/volume/massimale stimato nelle sessioni (progressione nel tempo).

### Palestra
Tabella ordinabile dei record assoluti per esercizio (schema, volume totale, data, 1RM), grafico a barre comparativo dei massimali stimati tra esercizi.

### Smartwatch
Selettore Giorno / Settimana / Mese che cambia la granularità di aggregazione dei grafici. Metriche: passi, frequenza cardiaca (media/min/max/riposo), SpO2, stress, calorie (totali/attive), ore in piedi, indice vitalità, sonno (durata totale e ripartizione fasi profondo/leggero/REM/veglia). Drill-down sui dati al minuto (attività e sequenza fasi sonno) per una specifica giornata selezionata.

---

## 5. Struttura del repository

Vedi `README.md` per l'albero completo aggiornato dei file e cartelle.

---

## 6. Cosa manca da fare (roadmap)

- [x] **Fase 1 — Smartwatch & Sonno**: completata l'estrazione per la famiglia Xiaomi (attività, daily summary, sessioni sonno e timeline fasi) e consolidamento nel modulo `smartwatch.py`.
- [ ] **Fase 2 — Fix menu CLI**: collegare l'opzione "Sincronizza Smartwatch" di `updateTracking.py` all'esecuzione del motore di sincronizzazione.
- [ ] **Fase 3 — Schema `dashboardData.db`**: definire lo schema delle tabelle SQLite dedicate alla dashboard (Misure, Dieta, Allenamento, Palestra, Personali, Smartwatch grezzo e aggregati Giorno/Settimana/Mese).
- [ ] **Fase 4 — `dashboardSync.py`**: realizzare lo script che legge da memoria Excel + le 4 matrici di `smartwatch.py` e scrive in modo transazionale su `dashboardData.db`, derivando le metriche storiche e applicando i flag di affidabilità pre 1 giugno 2026.
- [ ] **Fase 5 — Scaffolding Flask**: realizzare `app.py`, blueprint delle rotte, layout Bootstrap unificato (`base.html` con navbar).
- [ ] **Fase 6 — Implementazione pagine**: implementare service query, template HTML e script Plotly per ciascuna vista: Home, Misure, Dieta, Allenamento, Palestra, Smartwatch.
- [ ] **Fase 7 — Setup e verifica**: finalizzare `requirements.txt` e testare il flusso completo da terminale a browser.

---

## 7. Punti da verificare durante l'implementazione

- Volume effettivo di righe in `XIAOMI_ACTIVITY_SAMPLE` per dimensionare correttamente gli indici su SQLite in `dashboardData.db`.
- Gestione corretta dei valori mancanti o anomali nelle misurazioni storiche precedenti all'1 giugno 2026 all'interno dei grafici Plotly.