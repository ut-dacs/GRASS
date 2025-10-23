#This script calculates estimated CO₂ emissions associated with inter-AS (Autonomous System) 
#links on the Internet. It combines several datasets:

#- Geolocation data (MaxMind and PeeringDB) describing the presence of ASes in different countries.
#- Country-level emissions intensity data from the Green Web Foundation.
#- AS relationship data from CAIDA.
#- Link count data describing how many connections exist between AS pairs.

#Steps performed:
#1. Load and normalize AS geolocation presence data.
#2. Map ISO3 country codes to ISO2 for consistency with emissions data.
#3. Merge datasets (MaxMind + PeeringDB).
#4. Load country-level emissions intensity factors.
#5. Load AS relationships and link counts.
#6. For each AS-AS pair, estimate CO₂ emissions per link and total emissions 
#   based on link counts and geographical overlap.
#7. Save results as a CSV file.


import json
import pandas as pd
import pycountry
from collections import defaultdict
import os

def read_json(jsonfilename):
    with open(jsonfilename, 'r') as f:
        return json.load(f)

def iso3_to_iso2(iso3):
    try:
        return pycountry.countries.get(alpha_3=iso3).alpha_2
    except AttributeError:
        return None

def normalize_percentages(country_data):
    total_presence = sum(country_data.values())
    if total_presence > 0:
        return {country: (value / total_presence) * 100 for country, value in country_data.items()}
    return country_data

def merge_datasets(maxmind_data, peeringdb_data):
    combined_data = defaultdict(lambda: defaultdict(float))

    for asn, data in maxmind_data.items():
        for ip_type in ['ipv4', 'ipv6']:
            for country, presence in data.get(ip_type, {}).items():
                combined_data[asn][country] += presence

    for asn, data in peeringdb_data.items():
        for country, presence in data.items():
            combined_data[asn][country] += presence

    for asn in combined_data:
        combined_data[asn] = normalize_percentages(combined_data[asn])

    return combined_data

def load_emissions(filepath):
    raw = read_json(filepath)
    iso2_emissions = {}
    for iso3, entry in raw.items():
        iso2 = iso3_to_iso2(iso3)
        if iso2 and 'emissions_intensity_gco2_per_kwh' in entry:
            iso2_emissions[iso2] = entry['emissions_intensity_gco2_per_kwh']
    return iso2_emissions

def load_as_relationships(filepath):
    relationships = []
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split("|")
            if len(parts) >= 4:
                as1, as2, rel, source = parts
                relationships.append((as1, as2, int(rel), source))
    return relationships

def load_link_counts(filepath):
    df = pd.read_csv(filepath)
    count_data = {}
    skipped = 0

    for _, row in df.iterrows():
        as1_str = str(row['as1'])
        as2_str = str(row['as2'])
        count_str = str(row['count'])

        if "{" in as1_str or "{" in as2_str or "{" in count_str:
            skipped += 1
            continue

        try:
            as1 = int(as1_str)
            as2 = int(as2_str)
            count = int(count_str)
            key = (str(min(as1, as2)), str(max(as1, as2)))
            count_data[key] = count
        except ValueError:
            skipped += 1

    print(f"Skipped {skipped} invalid rows in count file.")
    return count_data

def compute_link_emission(as1, as2, presence_data, emissions_data, count_data):
    if as1 not in presence_data or as2 not in presence_data:
        return None

    pops1 = presence_data[as1]
    pops2 = presence_data[as2]
    shared_countries = set(pops1.keys()) & set(pops2.keys())

    total_weight = 0
    weighted_sum = 0

    if shared_countries:
        for country in shared_countries:
            if country not in emissions_data:
                continue
            w1 = pops1[country] / 100
            w2 = pops2[country] / 100
            weight = w1 + w2
            emission = emissions_data[country]
            weighted_sum += emission * weight
            total_weight += weight

        if total_weight > 0:
            co2_per_link = round(weighted_sum / total_weight, 2)
        else:
            return None
    elif len(pops1) == 1 and len(pops2) == 1:
        country1 = next(iter(pops1))
        country2 = next(iter(pops2))
        if country1 in emissions_data and country2 in emissions_data:
            co2_per_link = round((emissions_data[country1] + emissions_data[country2]) / 2, 2)
        else:
            return None
    else:
        return None

    key = tuple(sorted((as1, as2)))
    count = count_data.get(key)
    if count is None:
        return None

    total_co2 = round(co2_per_link * count, 2)

    return {
        "AS1": as1,
        "AS2": as2,
        "CO2_per_link": co2_per_link,
        "Count": count,
        "Total_CO2": total_co2
    }

def main():
    peeringdb_file = "geolocate/output/presence_per_AS_peeringdb_may_2025.json"
    maxmind_file = "geolocate/output/presence_per_AS_maxmind_may_2025_2.json"
    emissions_file = "green_web_foundation/gwf_average-intensities_last_updated_may_2025.json"
    caida_file = "caida/20250501.as-rel2.txt"
    counts_file = "Calculate_N/2025-05-01_as_links_count.csv"

    peeringdb_data = read_json(peeringdb_file)
    maxmind_data = read_json(maxmind_file)
    presence_data = merge_datasets(maxmind_data, peeringdb_data)
    emissions_data = load_emissions(emissions_file)
    relationships = load_as_relationships(caida_file)
    count_data = load_link_counts(counts_file)

    results = []
    for as1, as2, rel, source in relationships:
        result = compute_link_emission(as1, as2, presence_data, emissions_data, count_data)
        if result:
            result.update({"Relation": rel, "Source": source})
            results.append(result)

    os.makedirs("output", exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv("as_link_emissions_may_2025.csv", index=False)
    print("Saved to 'as_link_emissions_may_2025.csv'")

if __name__ == "__main__":
    main()
