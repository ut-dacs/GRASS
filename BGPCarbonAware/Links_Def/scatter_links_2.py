import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the enriched data with org names
df = pd.read_csv("enriched_as_links.csv")

# Keep only non-zero CO₂ emissions
df = df[df["Total_CO2"] > 0].copy()

# Compute total emissions per organization
org1_totals = df.groupby("AS1_org_name")["Total_CO2"].sum()
org2_totals = df.groupby("AS2_org_name")["Total_CO2"].sum()
org_totals = (org1_totals.add(org2_totals, fill_value=0)).sort_values(ascending=False)

# Top 20 organizations by total emissions
top_orgs = org_totals.head(20).index

# Filter data to include only top orgs as both source and destination
df_top = df[df["AS1_org_name"].isin(top_orgs) & df["AS2_org_name"].isin(top_orgs)]

# Pivot table
pivot = df_top.pivot_table(
    index="AS1_org_name",
    columns="AS2_org_name",
    values="Total_CO2",
    aggfunc="sum"
)
pivot = pivot.reindex(index=top_orgs, columns=top_orgs)

# Plot heatmap with larger fonts and NO annotations
plt.figure(figsize=(14, 12))
ax = sns.heatmap(
    pivot,
    cmap="Reds",
    linewidths=0.5,
    linecolor="gray",
    square=True,
    cbar_kws={'label': 'CO₂ Intensity (gCO₂)', 'format': '%.1e'},
    mask=pivot.isnull(),
    annot=False  # ← DISABLE annotations
)

# Mark missing cells with × using larger font
for y in range(pivot.shape[0]):
    for x in range(pivot.shape[1]):
        if pd.isna(pivot.iloc[y, x]):
            ax.text(
                x + 0.5, y + 0.5, '×',
                ha='center', va='center',
                color='black', fontsize=14, fontweight='bold'
            )

# Axis and title fonts
plt.title("CO₂ Intensity Between Top 20 Organizations", fontsize=22, pad=30)
plt.xlabel("Destination Organization", fontsize=16, labelpad=15)
plt.ylabel("Source Organization", fontsize=16, labelpad=15)

# Tick labels
plt.xticks(rotation=90, fontsize=12)
plt.yticks(rotation=0, fontsize=12)

# Colorbar font
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12)
cbar.set_label('CO₂ Intensity (gCO₂)', fontsize=14)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("plot5_heatmap_top20_orgs_large_fonts.png")
plt.close()

print("Saved: plot5_heatmap_top20_orgs_large_fonts.png")

