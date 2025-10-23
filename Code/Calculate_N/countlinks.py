#This script computes undirected AS-to-AS link counts from filtered BGP data.

#Input:
#    - A CSV file (`Data/2025-05-01_filtered_prefixes_aspaths.csv`)
#      containing rows in the format:
#        prefix | as_path
#      where as_path is a space-separated list of ASNs.

#Process:
#    1. Parse each AS path from the input file.
#    2. For each consecutive pair of ASes in the path, record a link.
#    3. Treat links as undirected (AS1-AS2 is the same as AS2-AS1).
#    4. Count how many times each link appears across all paths.

#Output:
#    - A CSV file (`2025-05-01_as_links_count.csv`) with columns:
#        as1, as2, count
#      where count = number of occurrences of the undirected link.

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
