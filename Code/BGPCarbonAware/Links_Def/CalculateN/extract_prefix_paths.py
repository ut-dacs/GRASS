import csv

input_file = '2025-05-01_ribs.csv'
output_file = '2025-05-01_prefixes_aspaths.csv'

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile, delimiter='|')
    writer = csv.writer(outfile, delimiter='|')
    
    for row in reader:
        if len(row) < 12:
            continue  # salta righe malformate
        prefix = row[9]
        as_path = row[11]
        writer.writerow([prefix, as_path])
