import pandas as pd
import plotly.graph_objects as go

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

# Create interactive CDF plot (no modification to x values)
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_sorted["CO2_Normalized"],
    y=df_sorted["Cumulative_Fraction"],
    mode="markers+lines",
    marker=dict(size=4),
    line=dict(width=2),
    name="CDF"
))

# Update layout with log x-axis and original x-values preserved
fig.update_layout(
    title="CDF of CO₂ Intensity Across AS-to-AS Links",
    xaxis=dict(
        title="CO₂ Intensity per Link (normalized)",
        type="log",
        tickformat=".1e"
    ),
    yaxis=dict(
        title="Cumulative Fraction of Total CO₂"
    ),
    width=800,
    height=500,
    template="simple_white"
)

# Save as HTML
fig.write_html("interactive_cdf_co2_intensity.html")
print("Saved: interactive_cdf_co2_intensity.html")

