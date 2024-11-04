"""
Your boss has heard that electricity prices have become more volatile with extreme prices in 
recent years. Therefore, she has asked you to create a table with some descriptive statistics for 
the hourly electricity price in NO2 and Germany. The table should: - - - 
contain the mean, median, standard deviation, min and max of the hourly electricity 
price in NO2 and Germany separately for each year in the sample (2019, 2020, 2021, 
2022, 2023). 
round all descriptive statistics to two decimals. 
be stored as an excel file called “table_task2.xlsx”. 
What is your conclusion? Have electricity prices in NO2 and Germany become more extreme in 
recent years? Have the prices evolved differently in NO2 than in Germany?  

"""


import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "../data/DayAheadPrices_12.1.D"

df = pd.read_csv(f"{DATA_PATH}/2019_02_DayAheadPrices_12.1.D.csv")


print(df)




"""
for year in range(2019, 2024):
    df
    

"""