import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

# Load data
df = pd.read_csv("enriched_as_links.csv")
df = df[df["Total_CO2"] > 0].copy()

# Clean organization names
def clean_org_name(name):
    if pd.isna(name):
        return name
    name = re.sub(r'\s*,?\s*\b(inc|llc)\b\.?', '', name, flags=re.IGNORECASE)
    return name.strip()

df["AS1_org_name"] = df["AS1_org_name"].apply(clean_org_name)
df["AS2_org_name"] = df["AS2_org_name"].apply(clean_org_name)

# Compute total emissions per organization
org1_totals = df.groupby("AS1_org_name")["Total_CO2"].sum()
org2_totals = df.groupby("AS2_org_name")["Total_CO2"].sum()
org_totals = (org1_totals.add(org2_totals, fill_value=0)).sort_values(ascending=False)

# Select top 10 organizations
top_orgs = org_totals.head(10).index
df_top = df[df["AS1_org_name"].isin(top_orgs) & df["AS2_org_name"].isin(top_orgs)]

# Create pivot table
pivot = df_top.pivot_table(
    index="AS1_org_name",
    columns="AS2_org_name",
    values="Total_CO2",
    aggfunc="sum"
).reindex(index=top_orgs, columns=top_orgs)

# Create base heatmap (without text annotations)
fig = go.Figure(data=go.Heatmap(
    z=pivot.values,
    x=pivot.columns,
    y=pivot.index,
    colorscale='Reds',
    colorbar=dict(title='CO₂ Intensity (gCO₂)'),
    zmin=0,
    zmax=np.nanmax(pivot.values),
    hovertemplate='Source: %{y}<br>Destination: %{x}<br>CO₂: %{z:.2e}<extra></extra>',
    showscale=True
))

# Add '×' where values are missing
for i, row in enumerate(pivot.index):
    for j, col in enumerate(pivot.columns):
        if pd.isna(pivot.loc[row, col]):
            fig.add_annotation(
                text='×',
                x=col,
                y=row,
                showarrow=False,
                font=dict(color='black', size=20, family='Arial'),
                xanchor='center',
                yanchor='middle'
            )

# Update layout
fig.update_layout(
    title='CO₂ Intensity Between Top 10 Organizations',
    xaxis_title='Destination Organization',
    yaxis_title='Source Organization',
    xaxis_tickangle=45,
    width=1000,
    height=900,
    font=dict(size=16),
)

# Save as HTML
fig.write_html("interactive_heatmap_top10_orgs_with_x.html")
print("Saved: interactive_heatmap_top10_orgs_with_x.html")

