import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "./data/PhysicalFlows_12.1.G/"

exports = {}
imports = {}

# Process data year by year
for year in range(2019, 2024):
    year_data = []
    # Read and concatenate monthly data for current year
    for month in range(1, 13):
        df = pd.read_csv(f"{DATA_PATH}{year}_{month:02d}_PhysicalFlows_12.1.G.csv", sep='\t', parse_dates=['DateTime'])
        mask = ((df['InMapCode'].isin(['NO2', 'DE_LU'])) & 
                (df['OutMapCode'].isin(['NO2', 'DE_LU'])))
        year_data.append(df[mask])
    
    # Process current year's data
    df_year = pd.concat(year_data)
    exports[year] = df_year[df_year['OutMapCode'] == 'NO2']['FlowValue'].sum()
    imports[year] = df_year[df_year['InMapCode'] == 'NO2']['FlowValue'].sum()


# Convert dictionaries to Series for plotting
exports = pd.Series(exports)
imports = pd.Series(imports)


# Create the bar plot
plt.figure(figsize=(10, 6))
x = exports.index
bar_width = 0.35


plt.bar(x - bar_width/2, imports, bar_width, label='Imports to NO2', color='skyblue')
plt.bar(x + bar_width/2, exports, bar_width, label='Exports from NO2', color='lightgreen')

plt.xlabel('Year')
plt.ylabel('Electricity Flow (MWh) in millions')
plt.title('Annual Electricity Imports and Exports - NO2 and Germany')
plt.legend()
plt.grid(True, alpha=0.3)

# Display years on x axis
plt.xticks(x, [int(year) for year in x])

plt.margins(y=0.2)

plt.show()


# Saving plot as png file
plt.savefig('figure_task3.png')



# Conclusion
# NO2 exports more electricity than it imports from Germany. The annual sums of exports have grown rapidly over the years, while the annual sums of imports have been relatively stable. As you can observe from the graph, Nordlink was not operational before 2020.