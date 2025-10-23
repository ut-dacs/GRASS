import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carica il CSV
df = pd.read_csv("enriched_as_links.csv")

# Assicura che la colonna CO2_Normalized sia numerica
df["CO2_Normalized"] = pd.to_numeric(df["CO2_Normalized"], errors="coerce")

# Rimuovi valori nulli o negativi
df = df[df["CO2_Normalized"] > 0].copy()

# Ordina i link per CO₂ crescente (dal meno impattante al più impattante)
df_sorted = df.sort_values("CO2_Normalized").reset_index(drop=True)

# Calcola la somma cumulativa della CO₂ (già normalizzata)
df_sorted["CDF"] = df_sorted["CO2_Normalized"].cumsum()

# Calcola la frazione dei link (asse X)
df_sorted["Fraction_of_Links"] = np.linspace(0, 1, len(df_sorted))

# Crea il grafico
plt.figure(figsize=(8, 5))
plt.plot(df_sorted["Fraction_of_Links"], df_sorted["CDF"], marker='.', linestyle='-')

# Label e stile
plt.xlabel("Fraction of AS-to-AS Links", fontsize=12)
plt.ylabel("Cumulative Fraction of Total CO₂", fontsize=12)
plt.title("CDF of Normalized CO₂ Intensity Across AS-to-AS Links", fontsize=14)
plt.grid(True, linestyle="--", linewidth=0.5)

# Salva il grafico
plt.tight_layout()
plt.savefig("cdf_normalized_co2.png")
plt.close()

print("✅ CDF plot saved as: cdf_normalized_co2.png")

