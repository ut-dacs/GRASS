import json
import csv

# Load the organization info
with open("20250501.as-org2info.json", "r") as f:
    as_org_info = json.load(f)

# Map AS number to AS_ID and organization name
as_number_to_info = {}
for as_id, (unique_id, org_name) in as_org_info.items():
    as_number = int(as_id.split("_")[0])
    as_number_to_info[as_number] = {
        "AS_ID": as_id,
        "AS_Organization": org_name
    }

# Load CO₂ intensity values
with open("as2co2_intensity_may_2025.json", "r") as f:
    as2co2 = json.load(f)

# Build and filter the final data
final_data = []
for asn_str, co2 in as2co2.items():
    asn = int(asn_str)
    if co2 and co2 > 0.0:  # exclude zero or missing values
        info = as_number_to_info.get(asn, {"AS_ID": None, "AS_Organization": None})
        final_data.append({
            "ASnumber": asn,
            "AS_ID": info["AS_ID"],
            "AS_Organization": info["AS_Organization"],
            "CO2_Intensity": co2
        })

# Sort by CO₂ intensity (ascending)
final_data.sort(key=lambda x: x["CO2_Intensity"])

# Write to CSV
with open("as_co2_final_filtered_sorted.csv", "w", newline="") as csvfile:
    fieldnames = ["ASnumber", "AS_ID", "AS_Organization", "CO2_Intensity"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(final_data)

print("Saved: as_co2_final_filtered_sorted.csv")

