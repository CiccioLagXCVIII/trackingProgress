# Dashboard Personale

Sistema personale per il tracciamento di dati fisici, alimentari, di allenamento e di attività fisica (smartwatch), con una dashboard web locale per la visualizzazione grafica.

## Panoramica

Il progetto è composto da due parti che lavorano insieme ma restano indipendenti tra loro:

1. **Tool CLI di tracciamento** (`trackingProgress/`) — già esistente e funzionante. Da terminale permette di inserire nuove misurazioni corporee, registrare fasi alimentari, importare sessioni di allenamento da OpenGym e calcolare automaticamente metriche derivate (BMR, TDEE, deficit calorico, massimali stimati, ecc.), salvando tutto in un file Excel (`trackingProgressi.xlsx`).
2. **Dashboard web locale** (`dashboardWeb/`) — in sviluppo. Applicazione Flask che legge i dati, attraverso un motore di sincronizzazione dedicato, e li presenta in più pagine con grafici interattivi.

Le due parti non condividono mai l'accesso in scrittura agli stessi file: il tool CLI scrive su Excel, la dashboard legge solo da un database SQLite dedicato (`dashboardData.db`) generato appositamente ad ogni sincronizzazione.

## Architettura

```text
 Fonti dati grezze              Motore di sync                 Dashboard Web
 ─────────────────              ───────────────                ─────────────
 trackingProgressi.xlsx  ──►    dashboardSync.py         ──►    Flask + Jinja2
 (Excel, scritto dal CLI)       - legge Excel in memoria        legge SOLO
                                - elabora smartwatch            dashboardData.db
 Gadgetbridge.db         ──►    - scrive dashboardData.db       (mai Excel o
 (SQLite smartwatch)                                            Gadgetbridge.db
                                lanciato manualmente da          direttamente)
                                menu CLI (opzione dedicata)
```

Perché questa separazione:

- Il file Excel resta la fonte "curata", leggibile e modificabile a mano — non viene mai appesantito con i dati dello smartwatch, che sono ad alta frequenza (al minuto) e renderebbero il file lento da aprire e a rischio di conflitti di lock.
- La dashboard web non apre mai né l'Excel né il database Gadgetbridge direttamente: legge solo lo store dedicato, rigenerato ogni volta che lanci la sincronizzazione dal CLI. Questo elimina qualsiasi rischio di leggere un file a metà scrittura o bloccato da un'altra applicazione.

## Struttura del repository

```text
.
├── gadgetBridgeSync/
│   └── Gadgetbridge.db              # DB Gadgetbridge sincronizzato dallo smartwatch (escluso da Git)
│
├── dashboardData.db                 # DB SQLite dedicato alla dashboard, generato dalla sync (escluso da Git)
│
├── trackingProgress/                # Tool CLI di tracciamento (esistente)
│   ├── diet.py                      # Gestione fasi alimentari
│   ├── measures.py                  # Gestione misurazioni corporee
│   ├── personal.py                  # Calcolo profilo personale (BMR, TDEE, età...)
│   ├── smartwatch.py                # Parser Gadgetbridge per Xiaomi/Redmi/Poco (attività al minuto, riepilogo, sonno)
│   ├── updateTracking.py            # Entry point del menu CLI
│   ├── utility.py                   # Costanti colori terminale, helper
│   ├── workout.py                   # Import allenamenti da OpenGym + record palestra
│   ├── dashboardSync.py             # Motore di sincronizzazione verso dashboardData.db
│   └── openGymData/
│       ├── downloadCatalog.py       # Scarica il catalogo esercizi
│       └── exercisesCatalog.json    # Mappa ID esercizio -> nome
│
├── XiaomiTokenExtractor/             # Utility per estrazione token account Xiaomi (escluso da Git)
│
└── dashboardWeb/                     # Applicazione web (in sviluppo)
    ├── app.py                        # Entry point Flask
    ├── routes/                       # Una route per pagina (home, dieta, misure, allenamento, palestra, smartwatch)
    ├── services/                     # Query verso dashboardData.db, una per pagina
    ├── templates/                    # Jinja2 + Bootstrap (layout base + una pagina per sezione)
    └── static/
        ├── css/
        └── js/                       # Grafici Plotly.js, uno script per pagina
```

## Stack tecnologico

| Livello | Tecnologia |
| --- | --- |
| Elaborazione dati / CLI | Python, pandas, openpyxl, sqlite3 |
| Storage dashboard | SQLite (`dashboardData.db`) |
| Backend web | Flask + Jinja2 |
| Frontend | HTML, CSS, Bootstrap |
| Grafici | Plotly.js |
| Fonte dati smartwatch | Database Gadgetbridge (SQLite) — Famiglia Xiaomi / Redmi / Poco |

## Flusso di lavoro

Non esiste nessuna sincronizzazione automatica: l'aggiornamento dei dati è sempre un'azione manuale, in due passi separati.

1. **Aggiorna i dati** — lancia `python trackingProgress/updateTracking.py` e usa il menu per inserire nuove misure corporee, registrare una nuova fase dieta, importare gli allenamenti, oppure sincronizzare lo smartwatch. Quest'ultima opzione legge `Gadgetbridge.db`, elabora i dati (attività al minuto, sintesi giornaliere, sessioni e fasi del sonno) e aggiorna `dashboardData.db`, insieme a una copia coerente dei dati correnti presenti nell'Excel.
2. **Guarda i dati** — apri la dashboard con `python dashboardWeb/app.py` e naviga tra le pagine dal browser, all'indirizzo locale indicato all'avvio.

## Pagine della dashboard

| Pagina | Contenuto principale |
| --- | --- |
| **Home** | Riepilogo profilo corrente (età, peso, massa magra, BMR Mifflin-St Jeor e Katch-McArdle, TDEE, deficit attivo), con i relativi trend nel tempo ricavati dallo storico di Misure e Dieta |
| **Dieta** | Timeline delle fasi alimentari (kcal e durata), ripartizione macronutrienti, proteine per kg corporeo, deficit teorico nel tempo, grafico incrociato target kcal/deficit vs peso reale |
| **Misure** | Peso, massa grassa %, massa magra, circonferenze corporee e BMR/TDEE nel tempo |
| **Allenamento** | Volume e durata per sessione, heatmap calendario (stile GitHub) della frequenza allenamenti, filtro per esercizio con andamento di peso/ripetizioni/volume/massimale stimato |
| **Palestra** | Bacheca record personali (massimale stimato 1RM per esercizio), tabella ordinabile e confronto tra esercizi |
| **Smartwatch** | Passi, frequenza cardiaca, SpO2, stress, calorie e sonno (durate e fasi dettagliate), con selettore Giorno/Settimana/Mese e drill-down sui dati al minuto per una giornata specifica |

**Nota sull'affidabilità dei dati:** le misurazioni corporee precedenti all'1 giugno 2026 vengono comunque mostrate nei grafici, ma segnalate visivamente come meno affidabili, poiché raccolte con minore rigore rispetto al metodo adottato da quella data in poi.

## Sicurezza e dati sensibili

Questo repository gestisce dati sanitari e personali. I seguenti elementi **non vengono mai versionati** (vedi `.gitignore`):

- `gadgetBridgeSync/Gadgetbridge.db` — dati grezzi di battito cardiaco, sonno e attività
- `XiaomiTokenExtractor/` — può contenere token o credenziali dell'account Xiaomi
- `dashboardData.db` — copia derivata dei dati personali, rigenerabile in qualsiasi momento tramite la sync
- `venv/`, `__pycache__/` — ambiente Python locale

Anche trattandosi di una repository privata, nessuno di questi file dovrebbe mai entrare nella storia di Git.

## Requisiti e installazione

Sezione da completare quando le dipendenze definitive saranno fissate. Indicativamente:

```bash
python -m venv venv
source venv/bin/activate        # su Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Stato del progetto

- [x] Tool CLI di tracciamento (misure, dieta, allenamento, profilo)
- [x] Lettura dati smartwatch da Gadgetbridge per famiglia Xiaomi/Redmi/Poco
- [x] Estrazione dati e fasi del sonno (`parseXiaomiSleep`)
- [x] Consolidamento modulo smartwatch in file singolo flat (`smartwatch.py`)
- [ ] Collegamento opzione "Sincronizza Smartwatch" nel menu CLI
- [ ] Definizione schema tabelle e aggregati per `dashboardData.db`
- [ ] Motore di sincronizzazione (`dashboardSync.py`)
- [ ] Applicazione web Flask (routes, template, grafici Plotly)
