import csv
from collections import Counter

# Counter to track undirected AS links
link_counter = Counter()

# Input file: filtered prefixes and AS paths
input_file = '2025-05-01_filtered_prefixes_aspaths.csv'
output_file = '2025-05-01_as_links_count.csv'

# Read and process AS paths
with open(input_file, 'r') as f:
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        if len(row) < 2:
            continue
        as_path = row[1].strip().split()
        for i in range(len(as_path) - 1):
            a, b = as_path[i], as_path[i + 1]
            link = tuple(sorted((a, b)))  # Undirected: (a, b) == (b, a)
            link_counter[link] += 1

# Write results to output CSV: as1, as2, count
with open(output_file, 'w', newline='') as f_out:
    writer = csv.writer(f_out)
    writer.writerow(['as1', 'as2', 'count'])  # header
    for (as1, as2), count in link_counter.items():
        writer.writerow([as1, as2, count])
