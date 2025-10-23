import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv("enriched_as_links.csv")

# Ensure CO2_Normalized is numeric
df["CO2_Normalized"] = pd.to_numeric(df["CO2_Normalized"], errors="coerce")

# Keep only positive values
df = df[df["CO2_Normalized"] > 0].copy()

# Sort by CO₂ intensity
df_sorted = df.sort_values("CO2_Normalized").reset_index(drop=True)

# Compute cumulative sum and normalize to get the CDF
df_sorted["Cumulative_CO2"] = df_sorted["CO2_Normalized"].cumsum()
df_sorted["Cumulative_Fraction"] = df_sorted["Cumulative_CO2"] / df_sorted["CO2_Normalized"].sum()

# Plot the CDF
plt.figure(figsize=(8, 5))
plt.plot(df_sorted["CO2_Normalized"], df_sorted["Cumulative_Fraction"], marker='.', linestyle='-')

# Use log scale for better visibility
plt.xscale('log')

# Labels and formatting
plt.xlabel("CO₂ Intensity per Link - normalized (log))", fontsize=12)
plt.ylabel("Cumulative Fraction of Total CO₂", fontsize=12)
plt.title("CDF of CO₂ Intensity Across AS-to-AS Links", fontsize=14)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Save the figure
plt.tight_layout()
plt.savefig("cdf_co2_intensity.png")
plt.close()

print("Saved: cdf_co2_intensity.png")

