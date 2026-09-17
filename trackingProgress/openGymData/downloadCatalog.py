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