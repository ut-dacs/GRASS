import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load data
with open('../as2co2_mapping/output/as2co2_intensity_may_2025.json') as f:
    asn_to_co2 = json.load(f)

df_pop = pd.read_csv('../popular_ases/as_top_list_ranked.csv')
df_pop['asn'] = df_pop['asn'].astype(str)
df_pop['CO2 Intensity'] = df_pop['asn'].map(asn_to_co2)
df_pop = df_pop.dropna(subset=['CO2 Intensity'])
df_pop = df_pop.sort_values(by='weight', ascending=False)

# Prepare group labels
df_pop['Group'] = 'All'
df_pop.loc[df_pop.index < 10000, 'Group'] = 'Top 10k'
df_pop.loc[df_pop.index < 1000, 'Group'] = 'Top 1k'
df_pop.loc[df_pop.index < 100, 'Group'] = 'Top 100'

# Ensure correct order
df_pop['Group'] = pd.Categorical(df_pop['Group'], categories=['Top 100', 'Top 1k', 'Top 10k', 'All'], ordered=True)

# Plot
plt.figure(figsize=(10, 6))
sns.violinplot(x='Group', y='CO2 Intensity', data=df_pop,
               inner='box', scale='width', cut=0, linewidth=1.1)

plt.xlabel("AS Popularity Group", fontsize=14)
plt.ylabel("CO₂ Intensity", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("output/co2_violin_popularity_groups.png", dpi=300)
plt.show()
