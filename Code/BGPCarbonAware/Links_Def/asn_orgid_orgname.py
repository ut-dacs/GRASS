import pandas as pd
import re

# Step 1: Parse 'asn_orgid.txt' safely
asn_list = []
with open('asn_orgid.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or ',' not in line:
            continue
        match = re.match(r'^(\d+)\s+(.*?),\s*[A-Z]{2}$', line)
        if match:
            asn = int(match.group(1))
            org_id = match.group(2).strip()
            asn_list.append((asn, org_id))

asn_orgid_df = pd.DataFrame(asn_list, columns=['ASN', 'OrgID'])

# Step 2: Parse '20250501.as-org2info.txt' manually (skip # lines)
org_rows = []
with open('20250501.as-org2info.txt', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split('|')
        if len(parts) >= 5:
            org_rows.append({
                'OrgID': parts[0],
                'OrgName': parts[2]
            })

orginfo_df = pd.DataFrame(org_rows)

# Step 3: Merge
merged = pd.merge(asn_orgid_df, orginfo_df, on='OrgID', how='left')

# Step 4: Save or print
merged.to_csv('asn_orgid_orgname_output.csv', index=False)
print(merged.head(10))

