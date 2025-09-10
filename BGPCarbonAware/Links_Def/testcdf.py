import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Carica il file
df = pd.read_csv("enriched_as_links.csv")
df["CO2_Normalized"] = pd.to_numeric(df["CO2_Normalized"], errors="coerce")
df = df[df["CO2_Normalized"] > 0].copy()

# 2. Ordina i link dal più impattante al meno
df_sorted = df.sort_values("CO2_Normalized", ascending=False).reset_index(drop=True)

# 3. CDF CO2 (frazione cumulativa delle emissioni)
df_sorted["CDF_CO2"] = df_sorted["CO2_Normalized"].cumsum()

# 4. Frazione cumulativa dei link
df_sorted["CDF_Links"] = np.linspace(0, 1, len(df_sorted))

# 5. Calcola il punto in cui hai coperto il top 10% dei link
top_10_index = int(len(df_sorted) * 0.10)
co2_top_10 = df_sorted.iloc[:top_10_index]["CO2_Normalized"].sum()

# 6. Plot
plt.figure(figsize=(8, 5))
plt.plot(df_sorted["CDF_Links"], df_sorted["CDF_CO2"], marker='.', linestyle='-')
plt.xlabel("Fraction of AS-to-AS Links (most to least impactful)", fontsize=14)
plt.ylabel("Cumulative Fraction of Total CO₂", fontsize=14)
plt.title("Top 10% Most Impactful Links vs. CO₂", fontsize=16)
plt.grid(True, linestyle='--', linewidth=0.5)

# 7. Linee e annotazioni
x_10 = df_sorted.loc[top_10_index, "CDF_Links"]
y_10 = df_sorted.loc[top_10_index, "CDF_CO2"]

plt.axvline(x_10, color='red', linestyle='--')
plt.axhline(y_10, color='red', linestyle='--')

plt.text(x_10 + 0.01, 0.02, "Top 10%", rotation=90, color='red', fontsize=14)
plt.text(
    0.12, y_10 - 0.05, f"{y_10*100:.2f}% CO₂",
    color='red', fontsize=14
)

plt.tight_layout()
plt.savefig("cdf_top10_impactful.png")
plt.close()

# 8. Stampa valore esatto
print(f"✅ Il top 10% dei link più impattanti ({top_10_index} link) causa il {co2_top_10*100:.2f}% delle emissioni.")
print("Grafico salvato come: cdf_top10_impactful.png")

