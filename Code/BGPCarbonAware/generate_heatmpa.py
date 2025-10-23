import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the CSV file
df = pd.read_csv("as_link_emissions_may_2025.csv")

# 2. Ensure numeric types
df["AS1"] = pd.to_numeric(df["AS1"], errors="coerce")
df["AS2"] = pd.to_numeric(df["AS2"], errors="coerce")
df["Total_CO2"] = pd.to_numeric(df["Total_CO2"], errors="coerce")
df = df.dropna(subset=["AS1", "AS2", "Total_CO2"])

# 3. Identify top 50 AS by frequency of appearance
as_counts = pd.concat([df["AS1"], df["AS2"]]).value_counts()
top_50_as = as_counts.head(50).index

# 4. Filter dataset to only include rows where both AS1 and AS2 are in top 
50
filtered_df = df[df["AS1"].isin(top_50_as) & df["AS2"].isin(top_50_as)]

# 5. Create a pivot table for the heatmap
pivot_table = filtered_df.pivot_table(
    index="AS1", columns="AS2", values="Total_CO2", fill_value=0
)

# 6. Plot the heatmap
plt.figure(figsize=(16, 14))
sns.heatmap(pivot_table, cmap="Reds", linewidths=0.3, linecolor='gray', 
cbar=True)

plt.title("Top 50 AS Link Emissions (CO₂) Heatmap")
plt.xlabel("AS2")
plt.ylabel("AS1")

# ✅ Define step size for x and y axis ticks to avoid overlap
xtick_step = max(1, len(pivot_table.columns) // 25)
ytick_step = max(1, len(pivot_table.index) // 25)

# ✅ Apply reduced number of labels
plt.xticks(
    ticks=range(0, len(pivot_table.columns), xtick_step),
    labels=pivot_table.columns[::xtick_step],
    rotation=90
)
plt.yticks(
    ticks=range(0, len(pivot_table.index), ytick_step),
    labels=pivot_table.index[::ytick_step],
    rotation=0
)

plt.tight_layout()

# 7. Save the figure
plt.savefig("as_link_emissions_heatmap_top50.png", dpi=300)
print("✅ Saved as 'as_link_emissions_heatmap_top50.png'")

