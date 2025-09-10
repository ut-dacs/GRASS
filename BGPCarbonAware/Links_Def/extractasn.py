import json

# Load emissions JSON
with open("as2co2_intensity_may_2025.json") as f:
    data = json.load(f)

# Extract and sort ASNs
asn_list = sorted([int(asn) for asn in data.keys()])

# Write to file
with open("asn_list.txt", "w") as f:
    for asn in asn_list:
        f.write(f"{asn}\n")

print("✅ Saved ASN list to asn_list.txt")

