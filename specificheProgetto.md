# Specifiche di Progetto — Dashboard Personale

Documento di riferimento tecnico: descrive cosa esiste già, le decisioni architetturali prese durante la progettazione, e cosa resta da implementare. Ad uso interno, complementare al `README.md` (più discorsivo e pensato per chi guarda il repository dall'esterno).

---

## 1. Obiettivo del progetto

Costruire una dashboard web multi-pagina, **da eseguire in locale**, che visualizzi graficamente tutti i dati raccolti nel tempo su: profilo fisico, misurazioni corporee, fasi alimentari, allenamenti in palestra, record personali e attività dello smartwatch (inclusi sonno e parametri vitali). I dati sono già raccolti e calcolati da un tool CLI Python esistente e funzionante; la dashboard è un livello di visualizzazione aggiuntivo, non sostituisce il tool CLI.

---

## 2. Cosa esiste già (componenti attuali)

### 2.1 Tool CLI — `trackingProgress/`

Applicazione a menu testuale (`updateTracking.py`), funzionante, che carica in memoria i fogli di un file Excel (`trackingProgressi.xlsx`) come DataFrame pandas e li aggiorna in base alle scelte dell'utente, preservando stili e formattazione con `openpyxl`.

| Modulo | Funzione | Output |
|---|---|---|
| `measures.py` | Inserisce nuove misurazioni corporee (peso, circonferenze), calcola massa grassa (formula US Navy), massa magra, BMR Katch-McArdle e TDEE pesato (allenamento/riposo) | Foglio Dati Misure |
| `diet.py` | Chiude la fase alimentare precedente (se aperta), registra una nuova fase con kcal/macro, verifica coerenza energetica, calcola deficit teorico e percentuali macro | Foglio Dati Dieta |
| `personal.py` | Ricalcola il profilo corrente (età, BMR Mifflin-St Jeor e Katch-McArdle, TDEE, deficit attivo) a partire dall'ultima riga di Misure e Dieta; sovrascrive sempre la stessa riga. Include una **bonifica difensiva** che rimuove eventuali timezone residue da qualsiasi cella del workbook prima del salvataggio (vedi § 8) | Foglio Dati Personali |
| `workout.py` | Importa sessioni da un export JSON di OpenGym, calcola volume e massimale stimato (Epley) per serie, filtra il riscaldamento e le serie a corpo libero, aggiorna lo storico allenamenti e ricalcola la bacheca record assoluti per esercizio | Fogli Dati Allenamento, Dati Palestra |
| `smartwatch.py` | Legge `Gadgetbridge.db`, rileva il dispositivo, ed estrae attività al minuto, riepiloghi giornalieri e **sonno** (sessioni + timeline fasi) per la famiglia Xiaomi/Redmi/Poco. File singolo, non un package — supporto limitato deliberatamente a questa famiglia (vedi § 3) | In memoria, passato a `dashboardSync.py` |
| `dashboardSync.py` | Crea lo schema di `dashboardData.db` (`initializeDashboardDB`), specchia i dati smartwatch (`syncSmartwatchData`) e i dati Excel (`syncTrackingMirror`), calcolando anche la tabella derivata `profilo_storico` | `dashboardData.db` |
| `utility.py` | Costanti colore per il terminale, funzione di input opzionale | — |
| `openGymData/downloadCatalog.py` | Scarica e salva localmente il catalogo esercizi (ID → nome) da una fonte online | `exercisesCatalog.json` |

### 2.2 Schema dati Excel esistente (5 fogli)

Invariato rispetto all'origine del progetto:
- **Dati Personali** (layout verticale parametro/valore): Sesso, Altezza, Data di Nascita, Età, Peso Corrente, Massa Magra Corrente, BMR Mifflin-St Jeor, BMR Katch-McArdle, TDEE Corrente Pesato, Deficit Corrente, Ultimo Aggiornamento.
- **Dati Misure** (una riga per misurazione): Data Misurazione, Peso, Circonferenza Collo/Vita/Fianchi/Braccio/Coscia, Massa Grassa %, Massa Magra, Metabolismo Basale (Katch-McArdle), Fabbisogno Giornaliero (TDEE pesato).
- **Dati Dieta** (una riga per fase alimentare): Data Inizio, Data Fine, Durata, Kcal, Deficit Teorico, Carbo/Grassi/Proteine (g), Proteine (g/Kg), % Carbo/Grassi/Proteine, Note.
- **Dati Allenamento** (una riga per serie): Data, Durata Allenamento, Nome Scheda, Nome Esercizio, Indice Serie, Ripetizioni Serie, Peso Serie, Volume Serie, Massimale Stimato Serie, Note.
- **Dati Palestra** (una riga per esercizio, solo il record storico): Nome Esercizio, Schema, Volume Totale, Data del record, Numero Serie, Ripetizioni Medie, Peso Medio, Massimale Stimato (1RM), Note.

### 2.3 Dati smartwatch (`Gadgetbridge.db`) — verificato su dati reali

**Attività e riepilogo** (già noto dall'origine del progetto): `XIAOMI_ACTIVITY_SAMPLE` (dati al minuto: passi, battito, SpO2, stress, distanza, calorie attive) e `XIAOMI_DAILY_SUMMARY_SAMPLE` (aggregati giornalieri).

**Sonno** (individuato e verificato durante lo sviluppo, ispezionando lo schema reale del DB — non erano nomi noti a priori):
- `XIAOMI_SLEEP_TIME_SAMPLE` — una riga per notte: `TIMESTAMP` (inizio sonno), `WAKEUP_TIME` (sveglia), `TOTAL_DURATION`, `DEEP_SLEEP_DURATION`, `LIGHT_SLEEP_DURATION`, `REM_SLEEP_DURATION`, `AWAKE_DURATION` (tutti in minuti, timestamp in millisecondi).
- `XIAOMI_SLEEP_STAGE_SAMPLE` — una riga per ogni cambio di fase: `TIMESTAMP`, `STAGE` (codice numerico). Nessuna colonna durata: si calcola come differenza tra un `TIMESTAMP` e il successivo (l'ultima fase dura fino al `WAKEUP_TIME` della sessione).

**Mapping dei codici `STAGE`**, verificato per confronto numerico tra le durate calcolate dalla timeline e i totali ufficiali di `XIAOMI_SLEEP_TIME_SAMPLE` sui dati reali del progetto (non un'ipotesi):

| Codice | Fase |
|---|---|
| 2 | Sonno Profondo |
| 3 | Sonno Leggero |
| 4 | Sonno REM |
| 5 | Sveglio |

Il codice `1` non è mai comparso nei dati raccolti finora — il parser lo gestisce comunque, segnalando in console qualsiasi codice non mappato invece di ignorarlo silenziosamente o andare in errore.

### 2.4 Bug corretti durante lo sviluppo

- **Menu CLI, opzione "Sincronizza Dashboard"**: era un placeholder che non faceva nulla — ora richiama davvero `smartwatch.processSmartwatchData()` e le funzioni di `dashboardSync.py`. **Corretto e verificato.**
- **Persistenza dati smartwatch**: prima non esisteva alcuna persistenza tra un'esecuzione e l'altra — ora tutto finisce in `dashboardData.db`. **Corretto e verificato.**
- **Corruzione Excel per timezone in fase di salvataggio**: `personal.py` andava in crash (`TypeError: Excel does not support timezones in datetimes`) durante il salvataggio, perché una cella del workbook conteneva un datetime con `tzinfo` non `None` — probabilmente inserita manualmente o da un giro precedente di uno script. Il salvataggio a metà ha corrotto il file `.xlsx` (openpyxl scrive direttamente sul file di destinazione, non su un temporaneo), richiedendo un ripristino da OneDrive. **Corretto** con una bonifica difensiva in `personal.py` che, prima di ogni salvataggio, scansiona tutte le celle del workbook (escludendo le `MergedCell`, che non permettono scrittura diretta di `.value`) e rimuove qualsiasi timezone residua. Vedi § 8 per il dettaglio.
- **Percorso `SMARTWATCH_DB` in `updateTracking.py`**: era rimasto sul vecchio percorso WSL locale invece del percorso Windows sincronizzato via Syncthing (già corretto altrove nel codice). **Fix identificato, da verificare con un'esecuzione reale dell'opzione 4 dal menu** (finora testato solo lanciando `dashboardSync.py` in isolamento).

### 2.5 Cosa è stato preparato e verificato finora

- Repository Git **privata**, `.gitignore` con dati sensibili esclusi.
- Mi Fitness + Gadgetbridge configurati e funzionanti; dispositivo (Redmi Watch 5 Active) sincronizzato con successo, incluso il tracciamento del sonno.
- Sincronizzazione `Gadgetbridge.db` dal telefono al PC via Syncthing, su cartella Windows nativa (non più su percorso di rete WSL, che causava errori intermittenti).
- `smartwatch.py`: file singolo, solo famiglia Xiaomi/Redmi/Poco (il pattern a registry multi-marca è stato scartato deliberatamente — vedi § 3), testato su dati reali: attività, riepilogo giornaliero e sonno tutti corretti.
- `dashboardData.db`: schema completo (11 tabelle) creato e popolato, verificato riga per riga — inclusa la logica più delicata (collegamento tra le misurazioni e la fase dieta attiva in quella data, dentro `profilo_storico`).
- `dashboardSync.py`: motore di sincronizzazione completo e testato.
- `updateTracking.py`: aggiornato e collegato a `dashboardSync.py`, verificato senza crash dopo la correzione del bug timezone.
- `requirements.txt` creato (pandas, numpy, openpyxl).
- `README.md` e questo documento, aggiornati allo stato corrente.

---

## 3. Decisioni architetturali prese

| Argomento | Decisione |
|---|---|
| Frontend | HTML + CSS + Bootstrap, nessun framework JS |
| Grafici | Plotly.js |
| Backend | Flask + Jinja2 |
| Storage dashboard | **Un solo file** SQLite (`dashboardData.db`), con due famiglie di tabelle (dominio Smartwatch + dominio Tracking/specchio Excel) — non due file fisici separati |
| Excel esistente | Resta **invariato** nel funzionamento |
| Storicizzazione Dati Personali | Nessuna tabella di log separata: BMR/TDEE/Deficit nel tempo derivati durante la sync direttamente dallo storico già presente in Misure e Dieta, calcolati nella tabella derivata `profilo_storico` |
| Affidabilità dati storici | Misurazioni precedenti all'1 giugno 2026 mostrate ma segnalate come meno affidabili (colonna `affidabile` già calcolata in `dashboardData.db`) |
| Flusso di aggiornamento | Nessuna sincronizzazione automatica: azione manuale dal menu CLI, poi apertura separata della dashboard |
| **Supporto smartwatch multi-dispositivo** | **Scartato.** Inizialmente pianificato un pattern a registry per più marche (Amazfit, Garmin, Huawei); deciso di semplificare a **solo Xiaomi/Redmi/Poco**, dato l'uso strettamente personale. Il repository sarà pubblico: chi usa altri dispositivi può fare fork e aggiungere il proprio parser |
| **Strategia di scrittura in `dashboardData.db`** | **Cancella e riscrivi per intero**, per ogni tabella, ad ogni sync — non un merge/upsert incrementale. Scelta perché sia `excelData` (in memoria) sia `processSmartwatchData()` restituiscono sempre il quadro completo, non solo le righe nuove: nessun bisogno di logica di deduplica, stesso approccio già usato da `workout.py` per la scheda Palestra |
| Aggregati temporali Smartwatch (giorno/settimana/mese) | Nessuna tabella di rollup pre-calcolata: dati reali (~1000 righe/giorno) restano piccoli abbastanza per aggregare al volo in query SQL indicizzate su `data`, senza bisogno di duplicare dati |
| Sonno | Incluso, tabelle e mapping fasi verificati su dati reali (vedi § 2.3) |
| Grafico incrociato Dieta/Misure | Sì: target kcal/deficit sovrapposto al peso reale nel tempo |
| Frequenza allenamenti | Heatmap calendario in stile GitHub |
| Convenzioni di stile codice | Python: camelCase, commenti in italiano, coerente col resto del progetto. Identificatori SQL (tabelle/colonne): snake_case minuscolo, convenzione standard per SQL indipendentemente dallo stile del codice Python circostante |

---

## 4. Specifica dettagliata per pagina (pianificate, non ancora implementate)

### Home
Card di stato con i valori correnti di Dati Personali, trend storico di TDEE/BMR/deficit da `profilo_storico`, card di richiamo dalle altre pagine.

### Dieta
Timeline delle fasi (kcal per fase), ripartizione macro, proteine g/kg nel tempo, deficit teorico nel tempo, grafico incrociato target kcal/deficit vs peso reale (da Misure).

### Misure
Peso, massa grassa %, massa magra, circonferenze corporee, BMR/TDEE nel tempo. Dati precedenti all'1 giugno 2026 segnalati come meno affidabili.

### Allenamento
Volume totale per sessione, durata allenamento, heatmap calendario stile GitHub, filtro per esercizio con andamento di peso/ripetizioni/volume/massimale stimato.

### Palestra
Tabella ordinabile dei record assoluti per esercizio, grafico a barre comparativo dei massimali stimati.

### Smartwatch
Selettore Giorno/Settimana/Mese, metriche di attività (passi, frequenza cardiaca, SpO2, stress, calorie, ore in piedi, indice vitalità) e **sonno** (durata totale, fasi leggero/profondo/REM/sveglio, timeline). Drill-down sui dati al minuto/fase per una giornata specifica.

---

## 5. Struttura del repository

Vedi `README.md` per l'albero completo e aggiornato delle cartelle e dei file.

---

## 6. Cosa manca da fare (roadmap)

- [x] ~~Fase 1 — Smartwatch generico~~ → **Semplificata**: solo Xiaomi, attività + sonno, funzionante su dati reali
- [x] ~~Fase 2 — Fix menu CLI~~ → Opzione "Sincronizza Dashboard" collegata e funzionante
- [x] ~~Fase 3 — Schema `dashboardData.db`~~ → 11 tabelle create, verificate
- [x] ~~Fase 4 — `dashboardSync.py`~~ → Scritto, testato, dato reale verificato riga per riga
- [x] ~~Fase 7 — Setup~~ → `requirements.txt` creato
- [ ] **Fase 5 — Scaffolding Flask**: `app.py`, blueprint delle routes, layout Bootstrap comune (`base.html` con navbar)
- [ ] **Fase 6 — Implementazione pagine**: una alla volta — service di query, template, script Plotly — per Home, Misure, Dieta, Allenamento, Palestra, Smartwatch
- [ ] Verifica finale del fix al percorso `SMARTWATCH_DB` in `updateTracking.py`, testando l'opzione 4 dal menu reale (non solo `dashboardSync.py` isolato)

## 7. Punti da verificare durante l'implementazione

- Volume reale di righe in `smartwatch_activity_raw` su un periodo più lungo (settimane/mesi), per confermare che l'aggregazione al volo resti performante anche a lungo termine.
- La cartella `gadgetBridgeSync/` dentro il repository (lato WSL) non è più il percorso realmente usato per il sync (ora su cartella Windows nativa, letta via `/mnt/c/`) — da valutare se ripulirla o lasciarla come riferimento storico.
- Verificare nel tempo se in `profilo_storico` compaiono altre misurazioni con `bmr_katch`/`tdee` vuoti (probabile per righe inserite manualmente in Excel prima di usare `measures.py`) e decidere se serve un trattamento specifico per quei casi nei grafici.

## 8. Incidente documentato: corruzione Excel per timezone

Durante lo sviluppo, un salvataggio di `personal.py` è andato in crash a causa di un valore datetime con timezone (`tzinfo` non `None`) presente in una cella del workbook, di origine non identificata (probabilmente inserimento manuale, o un giro precedente di uno script). Poiché `openpyxl` scrive lo zip del file `.xlsx` direttamente sul file di destinazione (non su un temporaneo da rinominare dopo), l'interruzione a metà scrittura ha lasciato il file in uno stato corrotto, richiedendo il ripristino da una versione precedente (OneDrive/Cronologia versioni).

**Lezione operativa**: fare sempre una copia di sicurezza del file Excel prima di testare modifiche al codice che lo salvano.

**Fix strutturale applicato** in `personal.py`: prima di ogni `excelFile.save(EXCEL_PATH)`, una bonifica scansiona tutte le celle di tutti i fogli del workbook e rimuove qualsiasi timezone residua (`cell.value.replace(tzinfo=None)`), escludendo esplicitamente le `MergedCell` (che non permettono la scrittura diretta di `.value` e avrebbero causato un `AttributeError` se non gestite). Questo rende il salvataggio resistente a questo tipo di dato "sporco", indipendentemente da dove sia stato introdotto.