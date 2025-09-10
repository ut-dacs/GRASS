import csv
import ipaddress

# Function to load valid prefixes from .pfx2as files
def load_pfx2as_prefixes(filenames):
    ipv4_set = set()
    ipv6_set = set()
    
    for filename in filenames:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                ip, length = parts[0], parts[1]
                try:
                    net = ipaddress.ip_network(f"{ip}/{length}", strict=False)
                    if net.version == 4:
                        ipv4_set.add(str(net))
                    elif net.version == 6:
                        ipv6_set.add(str(net))
                except ValueError:
                    continue  # skip malformed lines
    return ipv4_set, ipv6_set

# Function to filter rows from the main CSV file
def filter_csv(input_csv, ipv4_set, ipv6_set, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='|')
        writer = csv.writer(outfile, delimiter='|')
        
        for row in reader:
            if not row:
                continue
            prefix = row[0]
            try:
                net = ipaddress.ip_network(prefix, strict=False)
                if net.version == 4 and str(net) in ipv4_set:
                    writer.writerow(row)
                elif net.version == 6 and str(net) in ipv6_set:
                    writer.writerow(row)
            except ValueError:
                continue  # skip invalid prefixes

# Input files
pfx2as_files = [
    'routeviews-rv2-20250501-1200.pfx2as',  # IPv4
    'routeviews-rv6-20250501-1200.pfx2as'   # IPv6
]
input_csv = '2025-05-01_prefixes_aspaths.csv'
output_csv = '2025-05-01_filtered_prefixes_aspaths.csv'

# Execution

ipv4_prefixes, ipv6_prefixes = load_pfx2as_prefixes(pfx2as_files)
filter_csv(input_csv, ipv4_prefixes, ipv6_prefixes, output_csv)
