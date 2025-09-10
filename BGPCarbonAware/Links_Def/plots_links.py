import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dataset with Org names
df = pd.read_csv("as_links_with_orgs.csv")

# Filter out zero-emission links
df = df[df["Total_CO2"] > 0].copy()

# --- Plot 1: Cumulative Contribution (Pareto) ---
df_sorted = df.sort_values(by="Total_CO2")
df_sorted["Cumulative_CO2"] = df_sorted["Total_CO2"].cumsum()
df_sorted["Cumulative_Share"] = df_sorted["Cumulative_CO2"] / df_sorted["Total_CO2"].sum()
df_sorted["Link_Rank"] = np.arange(1, len(df_sorted) + 1) / len(df_sorted)

plt.figure(figsize=(8, 5))
plt.plot(df_sorted["Link_Rank"], df_sorted["Cumulative_Share"], linewidth=2)
plt.title("Cumulative Contribution of Links to Total CO₂ Emissions")
plt.xlabel("Fraction of Links (Sorted)")
plt.ylabel("Cumulative Share of CO₂ Emissions")
plt.grid(True)
plt.tight_layout()
plt.savefig("plot1_cumulative_contribution.png")
plt.close()

# --- Plot 2: Histogram of Total CO₂ (log scale) ---
plt.figure(figsize=(8, 5))
plt.hist(df["Total_CO2"], bins=100, log=True, edgecolor='black')
plt.title("Distribution of Total CO₂ Emissions per Link")
plt.xlabel("Total CO₂ (gCO₂)")
plt.ylabel("Number of Links (log scale)")
plt.tight_layout()
plt.savefig("plot2_histogram_total_co2.png")
plt.close()

# --- Plot 3: Top 20 Most Polluting Links (by Org Name) ---
df_top = df.sort_values(by="Total_CO2", ascending=False).head(20)
link_labels = df_top["Org1_ID"].astype(str) + " → " + df_top["Org2_ID"].astype(str)

plt.figure(figsize=(10, 8))
plt.barh(link_labels, df_top["Total_CO2"], color="darkred")
plt.title("Top 20 Most Polluting Links by Organization")
plt.xlabel("Total CO₂ Emissions (gCO₂)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("plot3_top20_orgs.png")
plt.close()

# --- Plot 4: Empirical CDF of Link CO₂ Emissions ---
co2_values = df_sorted["Total_CO2"].values
cdf = np.arange(1, len(co2_values) + 1) / len(co2_values)

plt.figure(figsize=(8, 5))
plt.plot(co2_values, cdf, linewidth=2)
plt.title("Empirical CDF of Link CO₂ Emissions")
plt.xlabel("Total CO₂ per Link (gCO₂)")
plt.ylabel("Cumulative Fraction of Links")
plt.grid(True)
plt.tight_layout()
plt.savefig("plot4_cdf_links.png")
plt.close()

print("✅ Plots saved as:")
print(" - plot1_cumulative_contribution.png")
print(" - plot2_histogram_total_co2.png")
print(" - plot3_top20_orgs.png")
print(" - plot4_cdf_links.png")

