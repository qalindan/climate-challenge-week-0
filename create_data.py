import pandas as pd
import numpy as np

# Create sample climate data for African countries
countries = ['Ethiopia', 'Kenya', 'Sudan', 'Tanzania', 'Nigeria']
years = range(1980, 2024)
data = []

for country in countries:
    for year in years:
        temp_change = np.random.normal(0.8, 0.3, 1)[0] + (year-1980)*0.02
        precipitation = np.random.normal(1000, 200, 1)[0] - (year-1980)*2
        co2_emissions = np.random.normal(500, 100, 1)[0] + (year-1980)*10
        
        data.append({
            'country': country,
            'year': year,
            'temp_change': temp_change,
            'precipitation': precipitation,
            'co2_emissions': co2_emissions,
            'population': np.random.normal(100e6, 50e6, 1)[0],
            'gdp': np.random.normal(500e9, 300e9, 1)[0]
        })

df = pd.DataFrame(data)
df.to_csv('data/africa_climate_data.csv', index=False)
print('Sample dataset created at data/africa_climate_data.csv')
print(f'Dataset shape: {df.shape}')
print(f'Columns: {list(df.columns)}')