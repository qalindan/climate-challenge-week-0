"""
COMPLETE EDA REPORT - African Climate Trend Analysis
10 Academy Week 0 Challenge
Task 2: Data Profiling, Cleaning & Exploratory Data Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for professional reports
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

print("="*80)
print("AFRICAN CLIMATE TREND ANALYSIS - COMPLETE EDA REPORT")
print("="*80)
print("Prepared for: 10 Academy Week 0 Challenge")
print("Date: April 2026")
print("="*80)

# ============================================================================
# SECTION 1: DATA LOADING AND INITIAL PROFILING
# ============================================================================
print("\n" + "="*80)
print("SECTION 1: DATA PROFILING")
print("="*80)

# Load the dataset
df = pd.read_csv('data/africa_climate_data.csv')
print(f"\n✓ Dataset loaded successfully")
print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")

print("\n📊 FIRST 5 ROWS:")
print(df.head())

print("\n📊 DATA TYPES:")
print(df.dtypes)

print("\n📊 BASIC STATISTICS:")
print(df.describe())

print("\n📊 MISSING VALUES:")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "No missing values found!")

print("\n📊 DUPLICATE ROWS:")
print(f"Number of duplicates: {df.duplicated().sum()}")

# ============================================================================
# SECTION 2: DATA CLEANING
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: DATA CLEANING")
print("="*80)

df_clean = df.copy()
print("\n✓ Creating clean dataset copy")

# 2.1 Check and handle missing values
if df_clean.isnull().sum().sum() > 0:
    print("\n🔧 Handling Missing Values:")
    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:
            if df_clean[col].dtype in ['float64', 'int64']:
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                print(f"  - {col}: Filled {df[col].isnull().sum()} missing with median ({median_val:.2f})")
            else:
                mode_val = df_clean[col].mode()[0]
                df_clean[col].fillna(mode_val, inplace=True)
                print(f"  - {col}: Filled with mode ({mode_val})")
else:
    print("\n✓ No missing values to handle")

# 2.2 Handle outliers using IQR method
print("\n🔧 Handling Outliers:")
outliers_handled = {}
for col in df_clean.select_dtypes(include=[np.number]).columns:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers_before = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
    if outliers_before > 0:
        df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
        outliers_handled[col] = outliers_before
        print(f"  - {col}: Capped {outliers_before} outliers")

print(f"\n✓ Data cleaning complete. New shape: {df_clean.shape}")

# ============================================================================
# SECTION 3: DESCRIPTIVE STATISTICS & DISTRIBUTIONS
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: DESCRIPTIVE STATISTICS & DISTRIBUTIONS")
print("="*80)

print("\n📊 CLEANED DATA STATISTICS:")
print(df_clean.describe())

# Create distribution plots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
for idx, col in enumerate(numeric_cols[:6]):
    axes[idx].hist(df_clean[col], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    axes[idx].axvline(df_clean[col].mean(), color='red', linestyle='--', 
                     label=f'Mean: {df_clean[col].mean():.2f}')
    axes[idx].axvline(df_clean[col].median(), color='green', linestyle='--', 
                     label=f'Median: {df_clean[col].median():.2f}')
    axes[idx].set_title(f'Distribution of {col}')
    axes[idx].set_xlabel(col)
    axes[idx].set_ylabel('Frequency')
    axes[idx].legend()

plt.suptitle('Figure 1: Distribution of Key Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('data/distribution_plots.png', dpi=150, bbox_inches='tight')
print("\n✓ Figure 1 saved: 'data/distribution_plots.png'")
plt.show()

# ============================================================================
# SECTION 4: CORRELATION ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("SECTION 4: CORRELATION ANALYSIS")
print("="*80)

# Calculate correlation matrix
corr_matrix = df_clean[numeric_cols].corr()

print("\n📊 CORRELATION MATRIX:")
print(corr_matrix.round(3))

# Create heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            fmt='.3f', square=True, linewidths=1)
plt.title('Figure 2: Correlation Matrix of Climate Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('data/correlation_heatmap.png', dpi=150, bbox_inches='tight')
print("\n✓ Figure 2 saved: 'data/correlation_heatmap.png'")
plt.show()

# Find strongest correlations
print("\n📈 STRONGEST CORRELATIONS:")
corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
corr_pairs = corr_pairs[corr_pairs < 1]  # Remove self-correlations

print("\nTop 5 Positive Correlations:")
for i, (pair, corr) in enumerate(corr_pairs.head(5).items(), 1):
    if corr > 0:
        print(f"  {i}. {pair[0]} ↔ {pair[1]}: {corr:.3f}")

print("\nTop 5 Negative Correlations:")
for i, (pair, corr) in enumerate(corr_pairs.tail(5).items(), 1):
    if corr < 0:
        print(f"  {i}. {pair[0]} ↔ {pair[1]}: {corr:.3f}")

# ============================================================================
# SECTION 5: TIME SERIES ANALYSIS (By Country)
# ============================================================================
print("\n" + "="*80)
print("SECTION 5: TIME SERIES ANALYSIS BY COUNTRY")
print("="*80)

if 'country' in df_clean.columns and 'year' in df_clean.columns:
    countries = df_clean['country'].unique()
    
    # Figure 3: Temperature trends over time
    fig, ax = plt.subplots(figsize=(12, 6))
    for country in countries:
        country_data = df_clean[df_clean['country'] == country]
        ax.plot(country_data['year'], country_data['temperature_change_celsius'], 
                marker='o', linewidth=2, markersize=4, label=country)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Temperature Change (°C)', fontsize=12)
    ax.set_title('Figure 3: Temperature Change Trends by Country (1980-2023)', 
                 fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/temperature_trends.png', dpi=150, bbox_inches='tight')
    print("\n✓ Figure 3 saved: 'data/temperature_trends.png'")
    plt.show()
    
    # Figure 4: CO2 emissions over time
    fig, ax = plt.subplots(figsize=(12, 6))
    for country in countries:
        country_data = df_clean[df_clean['country'] == country]
        ax.plot(country_data['year'], country_data['co2_emissions_kt'], 
                marker='s', linewidth=2, markersize=4, label=country)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('CO2 Emissions (kilotons)', fontsize=12)
    ax.set_title('Figure 4: CO2 Emissions Trends by Country (1980-2023)', 
                 fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/co2_trends.png', dpi=150, bbox_inches='tight')
    print("✓ Figure 4 saved: 'data/co2_trends.png'")
    plt.show()

# ============================================================================
# SECTION 6: COUNTRY COMPARISON
# ============================================================================
print("\n" + "="*80)
print("SECTION 6: COUNTRY COMPARISON ANALYSIS")
print("="*80)

country_stats = df_clean.groupby('country').agg({
    'temperature_change_celsius': ['mean', 'max', 'std'],
    'co2_emissions_kt': ['mean', 'sum'],
    'precipitation_mm': 'mean'
}).round(2)

print("\n📊 COUNTRY-WISE STATISTICS:")
print(country_stats)

# Figure 5: Bar chart comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Temperature change by country
temp_means = df_clean.groupby('country')['temperature_change_celsius'].mean().sort_values()
axes[0].barh(temp_means.index, temp_means.values, color='coral')
axes[0].set_xlabel('Average Temperature Change (°C)')
axes[0].set_title('Average Temperature Change by Country')

# CO2 emissions by country
co2_means = df_clean.groupby('country')['co2_emissions_kt'].mean().sort_values()
axes[1].barh(co2_means.index, co2_means.values, color='forestgreen')
axes[1].set_xlabel('Average CO2 Emissions (kt)')
axes[1].set_title('Average CO2 Emissions by Country')

plt.suptitle('Figure 5: Country Comparison - Climate Indicators', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('data/country_comparison.png', dpi=150, bbox_inches='tight')
print("\n✓ Figure 5 saved: 'data/country_comparison.png'")
plt.show()

# ============================================================================
# SECTION 7: KEY FINDINGS & INSIGHTS
# ============================================================================
print("\n" + "="*80)
print("SECTION 7: KEY FINDINGS & INSIGHTS")
print("="*80)

insights = []

# Calculate key metrics
overall_temp_increase = df_clean['temperature_change_celsius'].max() - df_clean['temperature_change_celsius'].min()
fastest_warming = df_clean.groupby('country')['temperature_change_celsius'].mean().idxmax()
highest_emitter = df_clean.groupby('country')['co2_emissions_kt'].mean().idxmax()

insights.append(f"📈 Temperature Increase: {overall_temp_increase:.2f}°C overall increase from 1980-2023")
insights.append(f"🌍 Fastest Warming Country: {fastest_warming}")
insights.append(f"🏭 Highest CO2 Emitter: {highest_emitter}")

# Correlation insights
temp_co2_corr = df_clean['temperature_change_celsius'].corr(df_clean['co2_emissions_kt'])
insights.append(f"🔗 Correlation between CO2 and Temperature: {temp_co2_corr:.3f}")

if temp_co2_corr > 0.7:
    insights.append("   → Strong positive correlation suggests CO2 emissions drive temperature increase")
elif temp_co2_corr > 0.4:
    insights.append("   → Moderate positive correlation between emissions and warming")
else:
    insights.append("   → Weak correlation indicates other factors affect temperature")

# Precipitation trends
precip_trend = df_clean.groupby('year')['precipitation_mm'].mean()
precip_change = (precip_trend.iloc[-1] - precip_trend.iloc[0]) / precip_trend.iloc[0] * 100
insights.append(f"💧 Precipitation Change: {precip_change:.1f}% change over 43 years")

if precip_change < 0:
    insights.append("   → Decreasing precipitation trend - potential desertification risk")

print("\n🎯 TOP 6 INSIGHTS FROM ANALYSIS:")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

# ============================================================================
# SECTION 8: RECOMMENDATIONS
# ============================================================================
print("\n" + "="*80)
print("SECTION 8: RECOMMENDATIONS FOR POLICY MAKERS")
print("="*80)

recommendations = [
    "1. Prioritize emissions reduction in countries with highest CO2 output",
    "2. Invest in climate adaptation infrastructure for fast-warming regions",
    "3. Monitor desertification in areas with declining precipitation trends",
    "4. Strengthen regional cooperation on climate data collection and sharing",
    "5. Develop early warning systems for extreme weather events",
    "6. Promote renewable energy adoption to decouple growth from emissions"
]

for rec in recommendations:
    print(f"  {rec}")

# ============================================================================
# SECTION 9: SAVE CLEANED DATA & EXPORT REPORT
# ============================================================================
print("\n" + "="*80)
print("SECTION 9: EXPORTING RESULTS")
print("="*80)

# Save cleaned dataset
df_clean.to_csv('data/cleaned_climate_data.csv', index=False)
print("✓ Cleaned dataset saved: 'data/cleaned_climate_data.csv'")

# Save summary statistics
summary_stats = df_clean.describe()
summary_stats.to_csv('data/summary_statistics.csv')
print("✓ Summary statistics saved: 'data/summary_statistics.csv'")

# Save country statistics
country_stats.to_csv('data/country_statistics.csv')
print("✓ Country statistics saved: 'data/country_statistics.csv'")

# Create a text report
with open('data/EDA_REPORT.txt', 'w') as f:
    f.write("AFRICAN CLIMATE TREND ANALYSIS - EDA REPORT\n")
    f.write("="*50 + "\n\n")
    f.write(f"Dataset Shape: {df_clean.shape}\n")
    f.write(f"Time Period: {df_clean['year'].min()} - {df_clean['year'].max()}\n")
    f.write(f"Countries Analyzed: {', '.join(df_clean['country'].unique())}\n\n")
    f.write("KEY FINDINGS:\n")
    for insight in insights:
        f.write(f"• {insight}\n")

print("✓ Text report saved: 'data/EDA_REPORT.txt'")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("✅ EDA COMPLETED SUCCESSFULLY")
print("="*80)
print("\n📁 OUTPUT FILES CREATED:")
print("  • data/cleaned_climate_data.csv")
print("  • data/summary_statistics.csv")
print("  • data/country_statistics.csv")
print("  • data/EDA_REPORT.txt")
print("  • data/distribution_plots.png")
print("  • data/correlation_heatmap.png")
print("  • data/temperature_trends.png")
print("  • data/co2_trends.png")
print("  • data/country_comparison.png")

print("\n" + "="*80)
print("END OF REPORT")
print("="*80)