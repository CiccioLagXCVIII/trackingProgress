# Dashboard Personale

Sistema personale per il tracciamento di dati fisici, alimentari, di allenamento e di attività fisica (smartwatch), con una dashboard web locale per la visualizzazione grafica.

## Panoramica

Il progetto è composto da due parti che lavorano insieme ma restano indipendenti tra loro:

1. **Tool CLI di tracciamento** (`trackingProgress/`) — funzionante. Da terminale permette di inserire nuove misurazioni corporee, registrare fasi alimentari, importare sessioni di allenamento da OpenGym, sincronizzare i dati dello smartwatch (attività e sonno), e calcola automaticamente metriche derivate (BMR, TDEE, deficit calorico, massimali stimati, ecc.), salvando tutto in un file Excel (`trackingProgressi.xlsx`).
2. **Dashboard web locale** (`dashboardWeb/`) — in sviluppo. Applicazione Flask che leggerà i dati da un database SQLite dedicato, generato dal tool CLI, e li presenterà in più pagine con grafici interattivi.

Le due parti non condividono mai l'accesso in scrittura agli stessi file: il tool CLI scrive su Excel e su `dashboardData.db`, la dashboard leggerà solo da `dashboardData.db`.

## Architettura

```
 Fonti dati grezze              Motore di sync                 Dashboard Web
 ─────────────────              ───────────────                ─────────────
 trackingProgressi.xlsx  ──►    dashboardSync.py         ──►    Flask + Jinja2
 (Excel, scritto dal CLI)       - legge Excel in memoria        legge SOLO
                                - legge/elabora smartwatch       dashboardData.db
 Gadgetbridge.db         ──►    - scrive dashboardData.db       (mai Excel o
 (SQLite smartwatch,                                            Gadgetbridge.db
  sincronizzato dal telefono    lanciato dal menu CLI            direttamente)
  via Syncthing su cartella     ("4. Sincronizza Dashboard")
  Windows nativa)
```

Perché questa separazione:

- Il file Excel resta la fonte "curata", leggibile e modificabile a mano — non viene mai appesantito con i dati dello smartwatch, che sono ad alta frequenza (al minuto) e renderebbero il file lento da aprire e a rischio di conflitti di lock.
- La dashboard web non aprirà mai né l'Excel né il database Gadgetbridge direttamente: legge solo `dashboardData.db`, rigenerato ogni volta che scegli l'opzione di sincronizzazione dal CLI.

**Nota sul sync smartwatch**: il file `Gadgetbridge.db` viene esportato dal telefono verso una cartella nativa Windows (`Documents\Appunti_E_Personale\trackingProgressi\gadgetBridgeSync\`) tramite Syncthing, e letto da WSL tramite `/mnt/c/`. Non usare percorsi di rete `\\wsl.localhost\...` per la cartella sincronizzata: quel percorso esiste solo mentre la VM di WSL è attiva e causa errori intermittenti di sincronizzazione.

## Struttura del repository

```
.
├── gadgetBridgeSync/                 # Cartella storica, non più usata per il sync (vedi nota sopra)
│
├── dashboardData.db                  # DB SQLite dedicato alla dashboard, generato dalla sync (escluso da Git)
│
├── trackingProgress/                 # Tool CLI di tracciamento
│   ├── diet.py                       # Gestione fasi alimentari
│   ├── measures.py                   # Gestione misurazioni corporee
│   ├── personal.py                   # Calcolo profilo personale (BMR, TDEE, età...)
│   ├── updateTracking.py             # Entry point del menu CLI
│   ├── utility.py                    # Costanti colori terminale, helper
│   ├── workout.py                    # Import allenamenti da OpenGym + record palestra
│   ├── smartwatch.py                 # Estrazione dati Gadgetbridge (Xiaomi/Redmi/Poco: attività + sonno)
│   ├── dashboardSync.py              # Motore di sincronizzazione verso dashboardData.db
│   └── openGymData/
│       ├── downloadCatalog.py        # Scarica il catalogo esercizi
│       └── exercisesCatalog.json     # Mappa ID esercizio -> nome
│
├── XiaomiTokenExtractor/              # Utility per estrazione token account Xiaomi (escluso da Git)
│
├── requirements.txt                   # Dipendenze Python del progetto
│
└── dashboardWeb/                      # Applicazione web (in sviluppo)
    ├── app.py                        # Entry point Flask
    ├── routes/                       # Una route per pagina
    ├── services/                     # Query verso dashboardData.db
    ├── templates/                    # Jinja2 + Bootstrap
    └── static/
        ├── css/
        └── js/                       # Grafici Plotly.js
```

**Nota sui percorsi assoluti**: i percorsi verso l'Excel e verso `Gadgetbridge.db`, dentro `trackingProgress/updateTracking.py`, sono attualmente hardcoded per questa specifica macchina (nome utente Windows incluso). Chiunque cloni/forki questo repository dovrà adattarli al proprio ambiente.

**Il supporto smartwatch copre solo la famiglia Xiaomi/Redmi/Poco** (stesso protocollo Xiaomi Wear): è una scelta deliberata per tenere il codice semplice, dato l'uso personale. Essendo il repository pubblico, chi usa un altro smartwatch è libero di fare un fork e aggiungere il proprio parser seguendo lo stesso schema di `smartwatch.py`.

## Stack tecnologico

| Livello | Tecnologia |
| --- | --- |
| Elaborazione dati / CLI | Python, pandas, openpyxl, sqlite3 |
| Storage dashboard | SQLite (`dashboardData.db`) |
| Backend web | Flask + Jinja2 |
| Frontend | HTML, CSS, Bootstrap |
| Grafici | Plotly.js |
| Fonte dati smartwatch | Database Gadgetbridge (SQLite) |

## Flusso di lavoro

Non esiste nessuna sincronizzazione automatica: l'aggiornamento dei dati è sempre un'azione manuale, in due passi separati.

1. **Aggiorna i dati** — lancia `python updateTracking.py` (dall'interno di `trackingProgress/`, con il venv attivo) e usa il menu per inserire nuove misure corporee, registrare una nuova fase dieta, importare gli allenamenti, oppure sincronizzare la dashboard. Quest'ultima opzione legge `Gadgetbridge.db`, elabora attività e sonno, e aggiorna `dashboardData.db` insieme a uno specchio coerente dei dati Excel correnti (misure, dieta, profilo, allenamento, palestra).
2. **Guarda i dati** — apri la dashboard con `python dashboardWeb/app.py` (quando sarà pronta) e naviga tra le pagine dal browser.

## Pagine della dashboard (pianificate)

| Pagina | Contenuto principale |
| --- | --- |
| **Home** | Riepilogo profilo corrente (età, peso, massa magra, BMR Mifflin-St Jeor e Katch-McArdle, TDEE, deficit attivo), con i relativi trend nel tempo ricavati dallo storico di Misure e Dieta |
| **Dieta** | Timeline delle fasi alimentari (kcal e durata), ripartizione macronutrienti, proteine per kg corporeo, deficit teorico nel tempo, grafico incrociato target kcal/deficit vs peso reale |
| **Misure** | Peso, massa grassa %, massa magra, circonferenze corporee e BMR/TDEE nel tempo |
| **Allenamento** | Volume e durata per sessione, heatmap calendario (stile GitHub) della frequenza allenamenti, filtro per esercizio con andamento di peso/ripetizioni/volume/massimale stimato |
| **Palestra** | Bacheca record personali (massimale stimato 1RM per esercizio), tabella ordinabile e confronto tra esercizi |
| **Smartwatch** | Passi, frequenza cardiaca, SpO2, stress, calorie e sonno (fasi leggero/profondo/REM/sveglio), con selettore Giorno/Settimana/Mese e drill-down sui dati al minuto per una giornata specifica |

**Nota sull'affidabilità dei dati:** le misurazioni corporee precedenti all'1 giugno 2026 vengono comunque mostrate nei grafici, ma segnalate visivamente come meno affidabili, poiché raccolte con minore rigore rispetto al metodo adottato da quella data in poi. Il flag `affidabile` è già calcolato e presente in `dashboardData.db`.

## Sicurezza e dati sensibili

Questo repository gestisce dati sanitari e personali. I seguenti elementi **non vengono mai versionati** (vedi `.gitignore`):

- `Gadgetbridge.db` — dati grezzi di battito cardiaco, sonno e attività (sia l'eventuale copia locale in `gadgetBridgeSync/`, sia la fonte reale sulla cartella Windows sincronizzata)
- `XiaomiTokenExtractor/` — può contenere token o credenziali dell'account Xiaomi
- `dashboardData.db` — copia derivata dei dati personali, rigenerabile in qualsiasi momento tramite la sync
- `venv/`, `__pycache__/` — ambiente Python locale

Anche trattandosi di una repository privata al momento, nessuno di questi file dovrebbe mai entrare nella storia di Git.

## Requisiti e installazione

```bash
python -m venv venv
source venv/bin/activate        # su Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Contenuto attuale di `requirements.txt`:

```
pandas>=2.0
numpy>=1.24
openpyxl>=3.1
```

Flask e le eventuali altre dipendenze web verranno aggiunte quando `dashboardWeb/` sarà implementata.

## Stato del progetto

- [x] Tool CLI di tracciamento (misure, dieta, allenamento, profilo)
- [x] Estrazione dati smartwatch da Gadgetbridge — attività, riepilogo giornaliero e **sonno** (fasi leggero/profondo/REM/sveglio), verificata su dati reali
- [x] Schema `dashboardData.db` e motore di sincronizzazione (`dashboardSync.py`)
- [x] Menu CLI collegato alla sincronizzazione reale (opzione "4. Sincronizza Dashboard")
- [x] `requirements.txt`
- [ ] Applicazione web Flask (routes, template, grafici Plotly)
- [ ] Supporto ad altri smartwatch (fuori scope per questo progetto, ma il codice è pubblico e forkabile)

Progetto per uso strettamente personale — nessuna licenza pubblica prevista.
