import csv

input_file = "as_link_emissions_may_2025.csv"
output_file = "as_links_sorted.csv"

with open(input_file, newline='') as infile:
    reader = csv.DictReader(infile)
    
    # Estrai solo le colonne che ci servono
    data = []
    for row in reader:
        try:
            as1 = row["AS1"]
            as2 = row["AS2"]
            total = float(row["Total_CO2"])
            data.append((as1, as2, total))
        except (KeyError, ValueError):
            continue  # salta righe con dati mancanti o errati

# Ordina dal più green (CO2 minore) al meno green
data.sort(key=lambda x: x[2])

# Scrivi il file pronto per il sito
with open(output_file, "w", newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["AS1", "AS2", "Total_CO2"])
    for row in data:
        writer.writerow(row)

print(f"File generato: {output_file}")

