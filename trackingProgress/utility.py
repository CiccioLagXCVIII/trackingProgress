
# AA Codici Di Formattazione ANSI Per Il Terminale
# BB Colori Associati Ai Vari Moduli Del Sistema
CLR_MISURE = "\033[92m"         # Verde Chiaro Per Il Modulo Misure
CLR_ERRORE = "\033[91m"         # Rosso Chiaro Per Errori E Blocchi
CLR_RESET = "\033[0m"           # Ripristina Il Colore Di Default Del Terminale
CLR_BOLD = "\033[1m"            # Applica Il Grassetto Al Testo
CLR_PROFILO = "\033[96m"        # Azzurro/Ciano Chiaro Per Il Modulo Profilo
CLR_ALLENAMENTO = "\033[95m"    # Magenta Chiaro Per Il Modulo Allenamento
CLR_PALESTRA = "\033[35m"       # Viola Per Il Modulo Della Bacheca Record Palestra
CLR_DIETA = "\033[93m"          # Giallo Chiaro Per Il Modulo Dieta
CLR_SMARTWATCH = "\033[94m"     # Blu Chiaro Per Il Modulo Smartwatch

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