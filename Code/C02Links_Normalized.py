import pandas as pd

# Load the CSV correctly (no index=False here)
df = pd.read_csv('../docs/enriched_as_links_june.csv')

# Compute total CO₂
total_co2 = df['Total_CO2'].sum()

# Calculate normalized values
df['CO2_Normalized'] = df['Total_CO2'] / total_co2

# Format to scientific notation as string
df['CO2_Normalized'] = df['CO2_Normalized'].apply(lambda x: f'{x:.2e}')

# Save the updated file
df.to_csv('../docs/enriched_as_links_june.csv', index=False)

# Preview
print(df.head(10))

