import pandas as pd

df = pd.read_csv("enriched_as_links.csv")
df["CO2_Normalized"] = pd.to_numeric(df["CO2_Normalized"], errors="coerce")
df = df[df["CO2_Normalized"] > 0].sort_values("CO2_Normalized").reset_index(drop=True)

# Compute cumulative distribution
df["cumsum"] = df["CO2_Normalized"].cumsum()
df["cum_frac"] = df["cumsum"] / df["CO2_Normalized"].sum()

# Number of links
n = len(df)

# Example: find % emissions from top 10%
top_10_cutoff = int(0.9 * n)
top_10_emissions = 1 - df.loc[top_10_cutoff, "cum_frac"]
print(f"Top 10% of links contribute about {top_10_emissions:.2%} of total emissions")

