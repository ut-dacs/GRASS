import json
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

MIN_COUNT = 25  # Only include business types with 25+ ASNs

# Load the JSON data
with open('../asdb/2024-01_categorized_ases.json') as f:
    asn_to_types = json.load(f)

with open('../as2co2_mapping/output/as2co2_intensity_may_2025.json') as f:
    asn_to_co2 = json.load(f)

# Aggregate CO2 emissions by business type
business_type_co2 = defaultdict(float)
business_type_counts = defaultdict(int)

for asn_str, co2 in asn_to_co2.items():
    types = asn_to_types.get(asn_str, [])
    unique_types = set(types)
    for t in unique_types:
        business_type_co2[t] += co2
        business_type_counts[t] += 1

print("Business type counts:")
for btype, count in sorted(business_type_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{btype}: {count}")

# Prepare a DataFrame for plotting
data = {
    "Business Type": [],
    "Total CO2 Emissions": [],
    "Average CO2 Emissions": []
}

for btype, total_co2 in business_type_co2.items():
    count = business_type_counts[btype]
    if count >= MIN_COUNT:
        data["Business Type"].append(btype)
        data["Total CO2 Emissions"].append(total_co2)
        data["Average CO2 Emissions"].append(total_co2 / count if count else 0)

df = pd.DataFrame(data)
df = df.sort_values(by="Average CO2 Emissions", ascending=False)

# Truncate long business type names
def truncate_label(label, max_len=25):
    return (label[:max_len] + '...') if len(label) > max_len else label

df["Business Type Short"] = df["Business Type"].apply(truncate_label)

# Plotting
plt.figure(figsize=(14, 10))
bars = plt.barh(df["Business Type Short"], df["Average CO2 Emissions"], color='skyblue', edgecolor='black')

# Grid and style improvements
plt.xlabel("Average CO2 Emissions", fontsize=12)
plt.title("Average CO2 Emissions per Business Type", fontsize=14)
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=8)

# Adjust layout and save
plt.tight_layout()
plt.savefig("output/co2_per_astype.png", dpi=300)

from adjustText import adjust_text

# Add ASN count column
df["ASN Count"] = df["Business Type"].apply(lambda b: business_type_counts[b])

# Start figure
# Keep only top N for plotting
TOP_N = 20
df_scatter = pd.concat([
    df.nlargest(TOP_N, "Total CO2 Emissions"),
    df.nlargest(TOP_N, "Average CO2 Emissions")
]).drop_duplicates()

# Plot only top ones
plt.figure(figsize=(12, 8))
plt.scatter(df_scatter["Average CO2 Emissions"], df_scatter["Total CO2 Emissions"],
            s=df_scatter["ASN Count"], alpha=0.7, edgecolors='black', color='orange')

# # Fix for pandas 2.x
# top_labels = pd.concat([
#     df.nlargest(10, "Total CO2 Emissions"),
#     df.nlargest(10, "Average CO2 Emissions")
# ]).drop_duplicates()

# Annotate only top ones
texts = []
for _, row in df_scatter.iterrows():
    texts.append(
        plt.text(row["Average CO2 Emissions"], row["Total CO2 Emissions"],
                 row["Business Type Short"], fontsize=9)
    )

adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

# Labels and grid
plt.xlabel("Average CO2 Emissions per ASN")
plt.ylabel("Total CO2 Emissions")
plt.title("Business Type CO2 Profile: Average vs Total (Top Highlighted)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("output/co2_scatter_avg_vs_total_readable.png", dpi=300)

import numpy as np

# Sort top emitters
top_total = df.nlargest(10, "Total CO2 Emissions").copy()
top_total["Business Type Short"] = top_total["Business Type"].apply(lambda x: truncate_label(x, 20))

# Setup
labels = top_total["Business Type Short"]
values = top_total["Total CO2 Emissions"]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

# Plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
bars = ax.bar(angles, values, width=0.4, color='orange', alpha=0.8, edgecolor='black')

# Label each bar
ax.set_xticks(angles)
ax.set_xticklabels(labels, fontsize=8)
ax.set_yticklabels([])
ax.set_title("Top 10 Business Types by Total CO2 Emissions (Polar)", y=1.08)
plt.tight_layout()
plt.savefig("output/co2_polar_top10_total.png", dpi=300)

import matplotlib.pyplot as plt
import pandas as pd

# Sort and select top N
TOP_N = 15
df_sorted = df.sort_values(by="Total CO2 Emissions", ascending=False).copy()
top_pie = df_sorted.head(TOP_N).copy()
others_total = df_sorted["Total CO2 Emissions"].iloc[TOP_N:].sum()

# Add 'Other' slice using pd.concat (Pandas 2.x compatible)
top_pie = pd.concat([top_pie, pd.DataFrame([{
    "Business Type": "Other",
    "Total CO2 Emissions": others_total,
    "Average CO2 Emissions": None,
    "Business Type Short": "Other"
}])], ignore_index=True)

# Pie chart
fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    top_pie["Total CO2 Emissions"],
    labels=top_pie["Business Type Short"],
    autopct='%1.1f%%',
    startangle=140,
    pctdistance=0.7,
    textprops=dict(color="black", fontsize=11),
    wedgeprops=dict(width=0.4, edgecolor='white')
)

# Center circle for donut
centre_circle = plt.Circle((0, 0), 0.55, fc='white')
ax.add_artist(centre_circle)

# Title with less padding
# ax.set_title(f"CO₂ Emissions Share by Business Type\n(Top {TOP_N} + Other)", fontsize=14, pad=10)

# Clean margins and save tightly
plt.subplots_adjust(left=0.05, right=0.95, top=0.88, bottom=0.05)
plt.savefig("output/co2_pie_topN_total_readable.png", dpi=300, bbox_inches='tight', pad_inches=0.1)

# Sort and compute cumulative % as before
df_cdf = df.sort_values(by="Total CO2 Emissions", ascending=False).copy()
df_cdf["Cumulative Emissions"] = df_cdf["Total CO2 Emissions"].cumsum()
df_cdf["Cumulative %"] = 100 * df_cdf["Cumulative Emissions"] / df_cdf["Total CO2 Emissions"].sum()
df_cdf["Business Type Short"] = df_cdf["Business Type"].apply(lambda x: (x[:25] + "...") if len(x) > 25 else x)

# Correct x and y for aligned CDF
x = list(range(len(df_cdf)))
y = df_cdf["Cumulative %"].tolist()

# Pad for proper CDF starting at 0%
x_step = [x[0] - 1] + x
y_step = [0] + y

# Plot
plt.figure(figsize=(14, 6))
plt.step(x_step, y_step, where='post', color='black', linewidth=1.5)

# X-axis labels aligned with steps
plt.xticks(ticks=x, labels=df_cdf["Business Type Short"], rotation=90, fontsize=8)
plt.yticks(ticks=range(0, 110, 10))  # Labels from 0% to 100% in 10% steps

# Axis and layout
plt.xlabel("Business Type (sorted by total CO₂)", fontsize=14)
plt.ylabel("Cumulative % of Total CO₂ Intensity", fontsize=14)
plt.ylim(0, 105)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("output/co2_intensity_cdf_black_steps_aligned.png", dpi=300, bbox_inches='tight', pad_inches=0.1)
