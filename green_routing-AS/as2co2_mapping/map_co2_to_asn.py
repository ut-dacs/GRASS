# This dataset is updated yearly: https://github.com/thegreenwebfoundation/co2.js/blob/main/data/output/average-intensities.json
# This dataset hasn't been updated since 2021: https://github.com/thegreenwebfoundation/co2.js/blob/main/data/output/marginal-intensities-2021.json

import pycountry
import json
from pprint import pprint as pprint
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Reads content of JSON file and returns
def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)

# writes content to json file
def write_json(jsonfilename, content):
    with open(jsonfilename, 'w+') as fp:
        json.dump(content, fp, indent=4)

# Converts ISO3 to ISO2
def iso3_to_iso2(iso3):
    try:
        return pycountry.countries.get(alpha_3=iso3).alpha_2
    except AttributeError:
        return None

# Normalize percentages so the total adds up to 100.
def normalize_percentages(country_data):
    total_presence = sum(country_data.values())
    if total_presence > 0:
        return {country: (value / total_presence) * 100 for country, value in country_data.items()}
    return country_data

# Merge MaxMind and PeeringDB datasets, then normalize 
def merge_datasets(maxmind_data, peeringdb_data):
    combined_data = defaultdict(lambda: defaultdict(float))
    
    # Add MaxMind data
    for asn, data in maxmind_data.items():
        for ip_type in ['ipv4', 'ipv6']:
            for country, presence in data.get(ip_type, {}).items():
                combined_data[asn][country] += presence

    # Add PeeringDB data
    for asn, data in peeringdb_data.items():
        for country, presence in data.items():
            combined_data[asn][country] += presence

    # Normalize percentages for each AS
    for asn in combined_data:
        combined_data[asn] = normalize_percentages(combined_data[asn])
    
    return combined_data

# Add CO2 emissions intensity to the combined dataset
def add_co2_intensity(combined_data, co2_data):
    co2_map = {iso3_to_iso2(k): v['emissions_intensity_gco2_per_kwh'] for k, v in co2_data.items()}
    
    enriched_data = {}

    for asn, country_data in combined_data.items():
        enriched_data[asn] = {}
        for country, presence in country_data.items():
            enriched_data[asn][country] = {
                'presence': presence,
                'co2_intensity': co2_map.get(country, None)  # Add CO2 intensity if available
            }

    return enriched_data

# Calculate the CO2 intensity for each AS based on its geographic footprint
def calculate_co2_intensity_per_as(enriched_data):
    as_co2_intensity = {}

    for asn, country_data in enriched_data.items():
        total_presence = 0
        weighted_co2_sum = 0

        for country, data in country_data.items():
            presence = data['presence']
            co2_intensity = data['co2_intensity']

            if co2_intensity is not None:
                weighted_co2_sum += presence * co2_intensity
                total_presence += presence

        # Avoid division by zero and calculate average CO2 intensity
        if total_presence > 0:
            as_co2_intensity[asn] = weighted_co2_sum / total_presence
        else:
            as_co2_intensity[asn] = None  # No valid CO2 intensity available

    return as_co2_intensity

# Plot a CDF showing the greenness of ASes and determine the best threshold for green ASes
def plot_threshold(output_url, as_co2_intensity):
    scores = [v for v in as_co2_intensity.values() if v is not None]
    thresholds = np.linspace(min(scores), max(scores), 50)
    green_fraction = [(np.array(scores) <= t).sum() / len(scores) for t in thresholds]

    plt.figure(figsize=(8, 6))
    plt.plot(thresholds, green_fraction, marker='o', linestyle='-', label="Fraction of Green ASes")
    plt.axvline(x=np.mean(scores), color='red', linestyle='--', label='Mean Threshold')
    plt.title("Greeness Threshold", fontsize=16)
    plt.xlabel("Carbon Emissions Intensity in gco2 per kwh", fontsize=16)
    plt.ylabel("CDF of ASes", fontsize=16)
    plt.xticks(np.arange(0, max(thresholds) + 1, 100), fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_url)
    plt.close()

if __name__ == '__main__':
    # Load datasets
    peeringdb_data = read_json('../geolocate/output/presence_per_AS_peeringdb_may_2025.json')
    maxmind_data = read_json('../geolocate/output/presence_per_AS_maxmind_may_2025.json')
    co2_per_iso3 = read_json("../green_web_foundation/gwf_average-intensities_last_updated_may_2025.json")

    # Merge the datasets
    normalized_data = merge_datasets(maxmind_data, peeringdb_data)

    # Generate a new dataset enriched with CO2 intensity
    augmented_data = add_co2_intensity(normalized_data, co2_per_iso3)

    # Calculate CO2 intensity per AS
    as_co2_intensity = calculate_co2_intensity_per_as(augmented_data)

    # Exclude None values
    filtered_dict = {k: v for k, v in as_co2_intensity.items() if v is not None}

    # Sort the filtered dictionary
    sorted_dict = dict(sorted(filtered_dict.items(), key=lambda item: item[1]))

    write_json("output/as2co2_intensity_may_2025.json", sorted_dict)
    
    # Plot the requested figures
    plot_threshold("output/threshold_green_ases_may_2025.png", sorted_dict)