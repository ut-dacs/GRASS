import csv
import json

# Load AS → Organization mapping
with open("ORG/20250501.as-org2info.json", "r") as f:
    as_org_map = json.load(f)

# Helper function to look up org info for an AS
def find_org(asn):
    for key in as_org_map:
        if key.startswith(str(asn) + "_"):
            return as_org_map[key]  # [org_id, org_name]
    return [None, None]

# Open the original CSV and the output CSV
with open("as_links_sorted.csv", newline='') as infile, \
     open("enriched_as_links.csv", "w", newline='') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = [
        "AS1", "AS1_org_id", "AS1_org_name",
        "AS2", "AS2_org_id", "AS2_org_name",
        "Total_CO2"
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        as1 = int(row["AS1"])
        as2 = int(row["AS2"])
        co2 = float(row["Total_CO2"])

        as1_org_id, as1_org_name = find_org(as1)
        as2_org_id, as2_org_name = find_org(as2)

        writer.writerow({
            "AS1": as1,
            "AS1_org_id": as1_org_id,
            "AS1_org_name": as1_org_name,
            "AS2": as2,
            "AS2_org_id": as2_org_id,
            "AS2_org_name": as2_org_name,
            "Total_CO2": co2
        })

