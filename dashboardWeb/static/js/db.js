// AA Indirizzo Del CDN Ufficiale Di sql.js, Da Cui Vengono Caricati Sia Il Motore Che Il File .wasm
const SQL_JS_CDN = "https://sql.js.org/dist/";

// AA Cache Del Database Caricato E Della Promise Di Caricamento, Condivise Da Tutte Le Pagine
// BB Evita Di Riscaricare/Reinizializzare Il Database Se Più Grafici Nella Stessa Pagina Chiamano queryDB()
let dbInstance = null;
let dbLoadingPromise = null;


// AA Caricamento Di sql.js E Di dashboardData.db, Eseguito Una Sola Volta
async function loadDatabase() {
    if (dbInstance) {
        return dbInstance;
    }
    if (dbLoadingPromise) {
        return dbLoadingPromise;
    }

    dbLoadingPromise = (async () => {
        // BB initSqlJs Viene Esposta Globalmente Dallo Script sql-wasm.js Incluso Nella Pagina HTML
        const initSqlJs = window.initSqlJs;
        const SQL = await initSqlJs({
            locateFile: (file) => `${SQL_JS_CDN}${file}`,
        });

        // BB Il Server Statico Viene Lanciato Dalla Radice Del Progetto, Quindi Il Percorso Assoluto
        // CC Funziona Indipendentemente Da Quale Pagina Dentro dashboardWeb/ Sta Chiamando Questa Funzione
        const response = await fetch("/dashboardData.db");
        if (!response.ok) {
            throw new Error(
                `Impossibile Caricare dashboardData.db (Status ${response.status}). ` +
                `Hai Lanciato "python -m http.server" Dalla Radice Del Progetto?`
            );
        }
        const buffer = await response.arrayBuffer();

        dbInstance = new SQL.Database(new Uint8Array(buffer));
        console.log("[DB] Database Caricato Con Successo.");
        return dbInstance;
    })();

    return dbLoadingPromise;
}


// AA Esegue Una Query SQL E Restituisce Un Array Di Oggetti (Una Riga = Un Oggetto Colonna: Valore)
// BB Piu' Comodo Da Usare Nei Grafici Rispetto Al Formato Grezzo Di sql.js (Colonne E Valori Separati)
async function queryDB(sql, params = []) {
    const db = await loadDatabase();
    const stmt = db.prepare(sql);
    if (params.length > 0) {
        stmt.bind(params);
    }

    const risultati = [];
    while (stmt.step()) {
        risultati.push(stmt.getAsObject());
    }
    stmt.free();

    return risultati;
}