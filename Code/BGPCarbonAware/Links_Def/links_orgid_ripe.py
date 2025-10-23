import pandas as pd
import re

# Step 1: Load ASN-to-Org mapping from asn_orgid.txt
asn_org_map = {}

with open('asn_orgid.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or ',' not in line:
            continue
        match = re.match(r'^(\d+)\s+(.*?),\s*[A-Z]{2}$', line)
        if match:
            asn = int(match.group(1))
            org = match.group(2).strip()
            asn_org_map[asn] = org

# Step 2: Load AS links with CO2 data
links_df = pd.read_csv('as_links_sorted.csv')

# Step 3: Map OrgID for AS1 and AS2
links_df['Org1_ID'] = links_df['AS1'].map(asn_org_map).fillna('UNKNOWN')
links_df['Org2_ID'] = links_df['AS2'].map(asn_org_map).fillna('UNKNOWN')

# Step 4: Reorder columns
result_df = links_df[['AS1', 'Org1_ID', 'AS2', 'Org2_ID', 'Total_CO2']]

# Step 5: Output to CSV
result_df.to_csv('as_links_with_orgs.csv', index=False)
print(result_df.head(10))

