import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carica il file
df = pd.read_csv("enriched_as_links.csv")

# Converti in numerico
df["CO2_Normalized"] = pd.to_numeric(df["CO2_Normalized"], errors="coerce")
df = df[df["CO2_Normalized"] > 0].copy()

# Ordina i link dal meno impattante al più impattante
df_sorted = df.sort_values("CO2_Normalized").reset_index(drop=True)

# Calcola la cumulata
df_sorted["Cumulative_CO2"] = df_sorted["CO2_Normalized"].cumsum()

# Calcola la differenza (salto) tra un punto e il precedente
df_sorted["Jump"] = df_sorted["Cumulative_CO2"].diff().fillna(df_sorted["Cumulative_CO2"])

# Trova i punti dove c'è un salto grande (es. > 1% = 0.01)
jump_threshold = 0.01
df_jumps = df_sorted[df_sorted["Jump"] >= jump_threshold]

# Mostra i punti con salti maggiori
print("🔍 Link che causano salti nella CDF > 1%:")
print(df_jumps[["CO2_Normalized", "Cumulative_CO2", "Jump"]])

# (Facoltativo) salva in un file CSV
df_jumps.to_csv("cdf_jump_links.csv", index=False)

# Grafico con annotazioni
plt.figure(figsize=(8, 5))
plt.plot(df_sorted["CO2_Normalized"], df_sorted["Cumulative_CO2"], marker='.', linestyle='-')
plt.xscale("log")
plt.xlabel("CO₂ Intensity per Link – normalized (log scale)", fontsize=12)
plt.ylabel("Cumulative Fraction of Total CO₂", fontsize=12)
plt.title("CDF of CO₂ Intensity with Jump Points Highlighted", fontsize=14)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Evidenzia i punti con salti
for _, row in df_jumps.iterrows():
    plt.plot(row["CO2_Normalized"], row["Cumulative_CO2"], 'ro')  # punto rosso

plt.tight_layout()
plt.savefig("cdf_with_jumps.png")
plt.close()

print("✅ Grafico salvato come: cdf_with_jumps.png")

