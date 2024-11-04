# Your boss believes that NO2 tends to export more electricity to Germany whenever the
# electricity price in Germany is higher relative to the price in NO2. She has asked you to
# investigate this claim by creating a scatter plot between the weekly sum of net exports in NO2
# and the weekly average price difference between Germany and NO2. Note that to find the
# weekly average price difference, you should first find the hourly price difference, and then take
# the weekly average.
# The graph should:
# - contain a single scatter plot that shows the weekly sum of net exports in NO2 on the y-
# axis and the weekly average price difference between Germany and NO2 on the x-axis.
# - contain the correlation coefficient between the weekly sum of net exports and the
# weekly average price difference in the figure title.
# - be stored as a png file called “figure_task5.png”.
# What is your conclusion? Does there seem to be a relationship between the weekly sum of net
# exports and the weekly average price difference? If so, is the relationship positive or negative?


# finding weekly average price difference
# sample of data:
# DateTime	ResolutionCode	AreaCode	AreaTypeCode	AreaName	MapCode	Price	Currency	UpdateTime
# 2019-01-01 00:00:00.000	PT60M	10Y1001A1001A45N	BZN	SE2 BZN	SE2	10.07	EUR	2018-12-31 13:16:07
# 2019-01-01 01:00:00.000	PT60M	10Y1001A1001A45N	BZN	SE2 BZN	SE2	10.03	EUR	2018-12-31 13:16:07
# 2019-01-01 02:00:00.000	PT60M	10Y1001A1001A45N	BZN	SE2 BZN	SE2	4.56	EUR	2018-12-31 13:16:07
# 2019-01-01 03:00:00.000	PT60M	10Y1001A1001A45N	BZN	SE2 BZN	SE2	4.83	EUR	2018-12-31 13:16:07
# 2019-01-01 04:00:00.000	PT60M	10Y1001A1001A45N	BZN	SE2 BZN	SE2	8.09	EUR	2018-12-31 13:16:07
# 2019-01-01 05:00:00.000	PT60M	10Y1001A1001A45N	BZN	SE2 BZN	SE2	25.54	EUR	2018-12-31 13:16:07

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Paths
price_data_path = './data/DayAheadPrices_12.1.D/'
flow_data_path = './data/PhysicalFlows_12.1.G/'

# Function to read and process price data for a specific area
def read_price_data(year_range, area_code):
    dfs = []
    for year in year_range:
        for month in range(1, 13):
            file_path = f"{price_data_path}{year}_{month:02d}_DayAheadPrices_12.1.D.csv"
            df = pd.read_csv(file_path, sep='\t', parse_dates=['DateTime'])
            df = df[df['MapCode'] == area_code][['DateTime', 'Price']]
            dfs.append(df)
    return pd.concat(dfs).sort_values('DateTime')

#REPLACE WHEN TASK 4 IS DONE
# Function to read and process flow data 
def read_flow_data(year_range):
    dfs = []
    for year in year_range:
        for month in range(1, 13):
            file_path = f"{flow_data_path}{year}_{month:02d}_PhysicalFlows_12.1.G.csv"
            df = pd.read_csv(file_path, sep='\t', parse_dates=['DateTime'])
            mask = ((df['InMapCode'].isin(['NO2', 'DE_LU'])) & 
                    (df['OutMapCode'].isin(['NO2', 'DE_LU'])))
            dfs.append(df[mask])
    return pd.concat(dfs)

# Read data
years = range(2019, 2024)
no2_prices = read_price_data(years, 'NO2')
de_prices = read_price_data(years, 'DE_LU')
flow_data = read_flow_data(years)

# Calculate hourly price differences (DE - NO2)
price_diff = pd.merge(de_prices, no2_prices, on='DateTime', suffixes=('_DE', '_NO2'))
price_diff['price_difference'] = price_diff['Price_DE'] - price_diff['Price_NO2']

# Calculate weekly average price differences
weekly_price_diff = price_diff.set_index('DateTime')['price_difference'].resample('W').mean()

# Calculate net exports (exports - imports)
flow_data['net_flow'] = np.where(flow_data['OutMapCode'] == 'NO2', 
                                flow_data['FlowValue'], 
                                -flow_data['FlowValue'])
weekly_net_exports = flow_data.set_index('DateTime')['net_flow'].resample('W').sum()

# Merge weekly data
weekly_data = pd.DataFrame({
    'price_diff': weekly_price_diff,
    'net_exports': weekly_net_exports
}).dropna()

# Calculate correlation coefficient
correlation = weekly_data['price_diff'].corr(weekly_data['net_exports'])

# Create scatter plot
plt.figure(figsize=(10, 6))

# Add scatter plot with label
plt.scatter(weekly_data['price_diff'], weekly_data['net_exports'], 
           alpha=0.5, label='Weekly Data Points')

# Add zero lines with labels
plt.axhline(y=0, color='red', linestyle='--', alpha=0.3, label='Net Zero')  
plt.axvline(x=0, color='red', linestyle='--', alpha=0.3)  

plt.xlabel('Weekly Average Price Difference (EUR/MWh)\nGermany - NO2')
plt.ylabel('Weekly Sum of Net Exports from NO2 (MWh)')
plt.title(f'Net Exports vs Price Difference\nCorrelation: {correlation:.2f}')
plt.grid(True, alpha=0.3)

# Add legend
plt.legend()

# Save plot before showing it
# plt.savefig('figure_task5.png')
plt.show()


# Conclusion: The correlation coefficient of 0.57 suggests a moderate positive relationship 
# between the weekly average price difference and net exports. This indicates that NO2 tends 
# to export more electricity to Germany when the price in Germany is higher relative to NO2.