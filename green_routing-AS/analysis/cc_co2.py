import bz2
import csv
import sys
import io
import json
from pprint import pprint as pprint
import matplotlib.pyplot as plt
import numpy as np

def plot_total_cone_co2_vs_size(as2cone, as2co2, include_self=False, log_scale=False):
    """
    Plots total customer cone CO₂ vs. cone size for each AS.

    Parameters:
    - as2cone: dict of {ASN: list of customer ASNs}
    - as2co2: dict of {ASN: CO₂ intensity}
    - include_self: whether to include the root AS in the cone CO₂ total
    - log_scale: whether to use log-log plot
    """
    x_sizes = []
    y_total_co2 = []

    for asn, customers in as2cone.items():
        cone_size = len(customers)
        total_co2 = sum(as2co2.get(cust, 0.0) for cust in customers)
        if include_self:
            total_co2 += as2co2.get(asn, 0.0)

        x_sizes.append(cone_size)
        y_total_co2.append(total_co2)

    plt.figure(figsize=(10, 6))
    plt.scatter(x_sizes, y_total_co2, alpha=0.3, s=10, color='black')
    x = np.array(x_sizes)
    y = np.array(y_total_co2)

    # Filter out zero or negative values
    mask = (x > 0) & (y > 0)
    x = x[mask]
    y = y[mask]

    log_x = np.log10(x)
    log_y = np.log10(y)
    
    # Fit linear regression in log-log space
    m, b = np.polyfit(log_x, log_y, 1)
    plt.plot(x, 10**(m * log_x + b), color='red', linewidth=2, label=f"Trend: y ∝ x^{m:.2f}")
    plt.xlabel("Customer Cone Size", fontsize=14)
    plt.ylabel("Total CO₂ Intensity in Cone (kg CO₂)", fontsize=14)

    if log_scale:
        plt.xscale('log')
        plt.yscale('log')

    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/co2_vs_cc.png")

def read_topology(as2rel_mapping):
    as2cone = {}

    with bz2.BZ2File(as2rel_mapping, 'rb') as compressed_file:
        decompressed_text = compressed_file.read().decode('utf-8')
        file_like = io.StringIO(decompressed_text)
        csvreader = csv.reader(file_like, delimiter=' ')

        for row in csvreader:
            if not row or row[0].startswith('#'):
                continue  # Skip comments and empty lines

            root_as = row[0]
            customer_ases = set(row[1:])  # remove duplicates per line

            if root_as not in as2cone:
                as2cone[root_as] = set()

            as2cone[root_as].update(customer_ases)  # add new customers uniquely

    # Convert all sets to lists if needed
    as2cone = {k: list(v) for k, v in as2cone.items()}

    return as2cone

csv.field_size_limit(sys.maxsize)
cc = read_topology('../caida/20250501.ppdc-ases.txt.bz2')
# Load data
with open('../as2co2_mapping/output/as2co2_intensity_may_2025.json') as f:
    asn_to_co2 = json.load(f)
plot_total_cone_co2_vs_size(cc, asn_to_co2, True, True)