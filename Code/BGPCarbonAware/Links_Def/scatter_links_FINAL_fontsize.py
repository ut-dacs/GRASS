import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

# Imposta font grandi globalmente
plt.rcParams.update({
    'font.size': 30,                  # Font base
    'axes.titlesize': 40,             # Titolo del grafico
    'axes.labelsize': 34,             # Etichette degli assi
    'xtick.labelsize': 38,            # Etichette tick asse X
    'ytick.labelsize': 38,            # Etichette tick asse Y
})

# Carica i dati
df = pd.read_csv("enriched_as_links.csv")

# Filtra emissioni non nulle
df = df[df["Total_CO2"] > 0].copy()

# Funzione per ripulire i nomi
def clean_org_name(name):
    if pd.isna(name):
        return name
    name = re.sub(r'\s*,?\s*\b(inc|llc)\b\.?', '', name, 
flags=re.IGNORECASE)
    return name.strip()

# Pulisci nomi delle organizzazioni
df["AS1_org_name"] = df["AS1_org_name"].apply(clean_org_name)
df["AS2_org_name"] = df["AS2_org_name"].apply(clean_org_name)

# Calcola emissioni totali per organizzazione
org1_totals = df.groupby("AS1_org_name")["Total_CO2"].sum()
org2_totals = df.groupby("AS2_org_name")["Total_CO2"].sum()
org_totals = (org1_totals.add(org2_totals, 
fill_value=0)).sort_values(ascending=False)

# Seleziona le 20 organizzazioni principali
top_orgs = org_totals.head(10).index

# Filtra dati per le top 20
df_top = df[df["AS1_org_name"].isin(top_orgs) & 
df["AS2_org_name"].isin(top_orgs)]

# Matrice pivot
pivot = df_top.pivot_table(
    index="AS1_org_name",
    columns="AS2_org_name",
    values="Total_CO2",
    aggfunc="sum"
)
pivot = pivot.reindex(index=top_orgs, columns=top_orgs)

# Crea la figura
plt.figure(figsize=(24, 22))

# Heatmap
ax = sns.heatmap(
    pivot,
    cmap="Reds",
    linewidths=0.5,
    linecolor="gray",
    square=True,
    cbar_kws={'label': 'CO₂ Intensity (gCO₂)', 'format': '%.1e'},
    mask=pivot.isnull(),
    annot=False
)

# Imposta fontsize per colorbar
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=24)
cbar.ax.yaxis.label.set_size(30)

# Marca le celle vuote con '×'
for y in range(pivot.shape[0]):
    for x in range(pivot.shape[1]):
        if pd.isna(pivot.iloc[y, x]):
            ax.text(
                x + 0.5, y + 0.5, '×',
                ha='center', va='center',
                color='black', fontsize=30, fontweight='bold'
            )

# Titolo e etichette assi
plt.title("CO₂ Intensity Between Top 10 Organizations", pad=60, 
fontsize=38)
plt.xlabel("Destination Organization", labelpad=30, fontsize=32)
plt.ylabel("Source Organization", labelpad=30, fontsize=32)

# Rotazione etichette
ax.set_xticklabels(ax.get_xticklabels(), fontsize=28, rotation=90)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=28, rotation=0)

# Ottimizza layout per evitare tagli
plt.tight_layout(rect=[0, 0.05, 1, 0.95])

# Salva in formato vettoriale EPS
plt.savefig("plot5_heatmap_top20_orgs_large_fonts.png", format='png')
plt.close()

print("Saved: plot5_heatmap_top20_orgs_large_fonts.eps")

