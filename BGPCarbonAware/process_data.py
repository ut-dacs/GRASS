import json
import pandas as pd

# === Load CO2 emissions ===
with open("as2co2_intensity_may_2025.json") as f:
    co2_data_raw = json.load(f)

# Keep only ASNs with emission > 0
co2_data = {
    int(asn): float(emission)
    for asn, emission in co2_data_raw.items()
    if float(emission) > 0
}

# === Load ASN → Organization name from asn.txt ===
asn_to_org = {}
with open("asn.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("0 -Reserved") or line.startswith("#"):
            continue
        try:
            # Handles lines like: 37057 VODACOM-LESOTHO, LS
            asn_str, rest = line.split(" ", 1)
            asn = int(asn_str)
            org_name = rest.split(",")[0].strip()
            asn_to_org[asn] = org_name
        except Exception:
            continue

# === Create list: ASN, Organization, CO2 Emissions ===
rows = []
for asn, co2 in co2_data.items():
    org = asn_to_org.get(asn, "Unknown Org")
    rows.append({
        "ASN": asn,
        "Organization": org,
        "CO2 Emissions": co2
    })

# === Save to CSV ===
df = pd.DataFrame(rows)
df = df.sort_values(by="CO2 Emissions")
df.to_csv("asn_emissions_with_org.csv", index=False)

print("✅ File saved: asn_emissions_with_org.csv")

