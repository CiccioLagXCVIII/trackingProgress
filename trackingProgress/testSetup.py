import logging
import os
import sqlite3

import pandas as pd
import utility

# AA Percorsi Assoluti, Identici A Quelli Di updateTracking.py
EXCEL_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/trackingProgressi.xlsx"
SMARTWATCH_DB = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/gadgetBridgeSync/Gadgetbridge.db"
DASHBOARD_DB_PATH = "/home/lag/privateDashboard/dashboardData.db"

SOGLIA_AFFIDABILITA_MISURE = "2026-06-01"

# AA Elenco Globale Dei Risultati Dei Controlli, Popolato Man Mano Dallo Script
risultati = []


# AA Funzione Di Appoggio Per Registrare E Stampare Un Singolo Esito Di Controllo
def segnaRisultato(nome, esito, dettaglio=""):
    risultati.append((nome, esito, dettaglio))
    tag = f"{utility.CLR_MISURE}[OK]{utility.CLR_RESET}" if esito else f"{utility.CLR_ERRORE}[FALLITO]{utility.CLR_RESET}"
    print(f"{tag} {nome}" + (f" — {dettaglio}" if dettaglio else ""))


# AA Verifica Che I Tre File/Database Principali Esistano Fisicamente Sul Disco
def verificaPercorsi():
    print(f"\n{utility.CLR_TEST}=== Verifica Percorsi ==={utility.CLR_RESET}")
    for nome, percorso in [
        ("File Excel", EXCEL_PATH),
        ("Database Gadgetbridge", SMARTWATCH_DB),
        ("Database Dashboard", DASHBOARD_DB_PATH),
    ]:
        esiste = os.path.exists(percorso)
        dettaglio = f"{os.path.getsize(percorso) / 1024 / 1024:.2f} MB" if esiste else percorso
        segnaRisultato(f"Percorso Trovato: {nome}", esiste, dettaglio)


# AA Verifica Che Il File Excel Sia Leggibile E Che Tutti I Fogli Attesi Siano Presenti
def verificaExcel():
    print(f"\n{utility.CLR_TEST}=== Verifica File Excel ==={utility.CLR_RESET}")
    if not os.path.exists(EXCEL_PATH):
        segnaRisultato("Lettura Fogli Excel", False, "File Non Trovato, Salto Il Controllo")
        return {}

    fogliAttesi = ['Dati Personali', 'Dati Misure', 'Dati Dieta', 'Dati Allenamento', 'Dati Palestra']
    excelData = {}
    try:
        for foglio in fogliAttesi:
            excelData[foglio] = pd.read_excel(EXCEL_PATH, sheet_name=foglio)
        segnaRisultato("Lettura Fogli Excel", True, f"{len(fogliAttesi)} Fogli Letti Correttamente")
        for foglio, df in excelData.items():
            print(f"    {foglio}: {len(df)} Righe")
    except Exception as e:
        segnaRisultato("Lettura Fogli Excel", False, str(e))

    return excelData

# AA Verifica Completa Del Database Dashboard: Tabelle, Coerenza Specchio, Regressioni Note
def verificaDashboardDB(excelData):
    print(f"\n{utility.CLR_TEST}=== Verifica Database Dashboard ==={utility.CLR_RESET}")
    if not os.path.exists(DASHBOARD_DB_PATH):
        segnaRisultato("Connessione Database Dashboard", False, "File Non Trovato, Salto Il Controllo")
        return

    conn = sqlite3.connect(DASHBOARD_DB_PATH)

    tabelleAttese = [
        "smartwatch_activity_raw", "smartwatch_daily_summary",
        "smartwatch_sleep_sessions", "smartwatch_sleep_stages",
        "misure", "dieta", "personale", "allenamento", "palestra", "profilo_storico"
    ]

    # BB Presenza Tabelle E Conteggio Righe
    conteggi = {}
    for tabella in tabelleAttese:
        try:
            conteggio = pd.read_sql_query(f"SELECT COUNT(*) as n FROM {tabella};", conn).iloc[0]['n']
            conteggi[tabella] = conteggio
            segnaRisultato(f"Tabella Presente: {tabella}", True, f"{conteggio} Righe")
        except Exception:
            segnaRisultato(f"Tabella Presente: {tabella}", False, "Tabella Non Trovata")

    # BB Regressione: Nessuna Stringa "NaT" Residua (Il Bug Che Abbiamo Gia' Corretto Una Volta)
    print(f"\n{utility.CLR_TEST}--- Controllo Valori 'NaT' Residui ---{utility.CLR_RESET}")
    natTrovati = []
    for tabella in tabelleAttese:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {tabella};", conn)
        except (sqlite3.Error, pd.errors.DatabaseError):
            logging.getLogger(__name__).exception(
                "Errore nel controllo della tabella dashboard %s", tabella
            )
            continue
        for colonna in df.select_dtypes(include=['object', 'str']).columns:
            match = df[df[colonna].astype(str) == "NaT"]
            if not match.empty:
                natTrovati.append(f"{tabella}.{colonna} ({len(match)} Righe)")
    segnaRisultato("Nessuna Stringa 'NaT' Residua", len(natTrovati) == 0, "; ".join(natTrovati))

    # BB Coerenza Specchio: Conteggio Righe Dashboard Deve Combaciare Con L'Excel Di Origine
    if excelData:
        print(f"\n{utility.CLR_TEST}--- Controllo Coerenza Specchio Excel <-> Dashboard ---{utility.CLR_RESET}")
        mappaSpecchio = {
            "Dati Misure": "misure",
            "Dati Dieta": "dieta",
            "Dati Allenamento": "allenamento",
            "Dati Palestra": "palestra",
        }
        for foglioExcel, tabellaDashboard in mappaSpecchio.items():
            righeExcel = len(excelData.get(foglioExcel, []))
            righeDashboard = conteggi.get(tabellaDashboard)
            segnaRisultato(
                f"Coerenza Righe: {foglioExcel} <-> {tabellaDashboard}",
                righeDashboard == righeExcel,
                f"Excel: {righeExcel}, Dashboard: {righeDashboard}"
            )

    # BB La Tabella Personale Deve Contenere Sempre Esattamente Una Riga (Vincolo id = 1)
    segnaRisultato("Tabella 'personale' Ha Esattamente 1 Riga", conteggi.get("personale") == 1, f"Trovate: {conteggi.get('personale')}")

    # BB Coerenza Del Flag Affidabile Rispetto Alla Soglia Dell'1 Giugno 2026
    print(f"\n{utility.CLR_TEST}--- Controllo Flag Affidabilita Misure ---{utility.CLR_RESET}")
    try:
        misureDf = pd.read_sql_query("SELECT data_misurazione, affidabile FROM misure;", conn)
        errori = misureDf[
            ((misureDf["data_misurazione"] < SOGLIA_AFFIDABILITA_MISURE) & (misureDf["affidabile"] != 0)) |
            ((misureDf["data_misurazione"] >= SOGLIA_AFFIDABILITA_MISURE) & (misureDf["affidabile"] != 1))
        ]
        segnaRisultato("Flag Affidabile Coerente Con La Soglia", errori.empty, f"{len(errori)} Righe Incoerenti")
    except Exception as e:
        segnaRisultato("Flag Affidabile Coerente Con La Soglia", False, str(e))

    # BB Tutti I Codici Fase Sonno Devono Essere Tra Quelli Verificati E Mappati
    print(f"\n{utility.CLR_TEST}--- Controllo Codici Fase Sonno ---{utility.CLR_RESET}")
    try:
        fasiDf = pd.read_sql_query("SELECT DISTINCT fase FROM smartwatch_sleep_stages;", conn)
        fasiConosciute = {"Sonno Profondo", "Sonno Leggero", "Sonno REM", "Sveglio"}
        fasiSconosciute = set(fasiDf["fase"]) - fasiConosciute
        segnaRisultato("Tutte Le Fasi Sonno Sono Codici Riconosciuti", len(fasiSconosciute) == 0, f"Sconosciute: {fasiSconosciute}" if fasiSconosciute else "")
    except Exception as e:
        segnaRisultato("Tutte Le Fasi Sonno Sono Codici Riconosciuti", False, str(e))

    # BB La Durata Totale Della Sessione Deve Coincidere Con Profondo + Leggero + REM (Verificato Manualmente In Precedenza)
    print(f"\n{utility.CLR_TEST}--- Controllo Coerenza Durata Sonno ---{utility.CLR_RESET}")
    try:
        sessioni = pd.read_sql_query("SELECT * FROM smartwatch_sleep_sessions;", conn)
        incoerenti = []
        for _, sessione in sessioni.iterrows():
            sommaFasi = sessione["sonno_profondo_min"] + sessione["sonno_leggero_min"] + sessione["sonno_rem_min"]
            if sommaFasi != sessione["durata_totale_min"]:
                incoerenti.append(sessione["data"])
        segnaRisultato(
            "Durata Totale Sonno = Profondo + Leggero + REM",
            len(incoerenti) == 0,
            f"Notti Incoerenti: {incoerenti}" if incoerenti else ""
        )
    except Exception as e:
        segnaRisultato("Durata Totale Sonno = Profondo + Leggero + REM", False, str(e))

    # BB Controllo Incrociato: Somma Della Timeline Fasi Deve Combaciare Con I Totali Ufficiali Della Sessione
    print(f"\n{utility.CLR_TEST}--- Controllo Incrociato Timeline Fasi Vs Sessioni Sonno ---{utility.CLR_RESET}")
    try:
        sessioni = pd.read_sql_query("SELECT * FROM smartwatch_sleep_sessions;", conn)
        fasiTimeline = pd.read_sql_query("SELECT * FROM smartwatch_sleep_stages;", conn)

        mappaFaseColonna = {
            "Sonno Profondo": "sonno_profondo_min",
            "Sonno Leggero": "sonno_leggero_min",
            "Sonno REM": "sonno_rem_min",
        }
        TOLLERANZA_MINUTI = 2
        discrepanze = []

        for _, sessione in sessioni.iterrows():
            fasiNotte = fasiTimeline[fasiTimeline["data"] == sessione["data"]]
            for fase, colonna in mappaFaseColonna.items():
                sommaTimeline = fasiNotte.loc[fasiNotte["fase"] == fase, "durata_min"].sum()
                valoreUfficiale = sessione[colonna]
                if abs(sommaTimeline - valoreUfficiale) > TOLLERANZA_MINUTI:
                    discrepanze.append(f"{sessione['data']}/{fase}: Timeline={sommaTimeline}, Ufficiale={valoreUfficiale}")

        segnaRisultato(
            "Timeline Fasi Coerente Con I Totali Ufficiali Della Sessione",
            len(discrepanze) == 0,
            "; ".join(discrepanze) if discrepanze else ""
        )
    except Exception as e:
        segnaRisultato("Timeline Fasi Coerente Con I Totali Ufficiali Della Sessione", False, str(e))

    conn.close()


# AA Stampa Il Riepilogo Finale Di Tutti I Controlli Eseguiti
def stampaRiepilogoFinale():
    print(f"\n{utility.CLR_TEST}{utility.CLR_BOLD}=========================================================={utility.CLR_RESET}")
    print(f"{utility.CLR_TEST}{utility.CLR_BOLD} RIEPILOGO VERIFICA SISTEMA{utility.CLR_RESET}")
    print(f"{utility.CLR_TEST}{utility.CLR_BOLD}=========================================================={utility.CLR_RESET}")

    totali = len(risultati)
    falliti = [r for r in risultati if not r[1]]

    print(f"Controlli Eseguiti: {utility.CLR_BOLD}{totali}{utility.CLR_RESET}")
    print(f"Superati: {utility.CLR_MISURE}{totali - len(falliti)}{utility.CLR_RESET}")
    print(f"Falliti: {utility.CLR_ERRORE}{len(falliti)}{utility.CLR_RESET}")

    if falliti:
        print(f"\n{utility.CLR_ERRORE}Controlli Falliti:{utility.CLR_RESET}")
        for nome, _, dettaglio in falliti:
            print(f"  - {nome}" + (f" ({dettaglio})" if dettaglio else ""))
    else:
        print(f"\n{utility.CLR_MISURE}{utility.CLR_BOLD}Tutti I Controlli Sono Passati! Sistema Pronto Per La Dashboard.{utility.CLR_RESET}")

    print(f"{utility.CLR_TEST}{utility.CLR_BOLD}=========================================================={utility.CLR_RESET}\n")


# AA Blocco Di Esecuzione Diretta Dello Script
if __name__ == "__main__":
    os.system('clear')
    print(f"{utility.CLR_TEST}{utility.CLR_BOLD}Avvio Verifica Completa Del Sistema...{utility.CLR_RESET}")

    verificaPercorsi()
    excelData = verificaExcel()
    verificaDashboardDB(excelData)

    stampaRiepilogoFinale()