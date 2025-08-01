import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("https://raw.githubusercontent.com/TianchengLi42/StatsCan_LandValue/refs/heads/main/3210004701_databaseLoadingData.csv")

# First, cleaning up the data, "STATUS	SYMBOL	TERMINATED" columns only contain nan values, they will be dropped

nan_columns = ["STATUS", "SYMBOL", "TERMINATED"]
df = df.drop(columns = nan_columns)

# Dropping more columns that contains values, but do not contain any useable information
# The following columns are dropped : DGUID	Farm land and buildings	UOM	UOM_ID	SCALAR_FACTOR	SCALAR_ID	VECTOR	COORDINATE

drop_columns = ["DGUID", "Farm land and buildings", "UOM", "UOM_ID", "SCALAR_FACTOR", "SCALAR_ID", "VECTOR", "COORDINATE", "DECIMALS" ]
df = df.drop(columns = drop_columns)
df.index = df["GEO"]
df = df.drop(columns = ["GEO"])

#print(df)

# Adding a GEO index column to make data searching easier (using ISO 3166), eg: CA for canada, ON for ontario, etc

index = pd.read_csv("https://raw.githubusercontent.com/ravinsharma12345/ISO-3166/refs/heads/master/ISO-3166-2.csv", sep = ';', index_col=0)

# Cleaning the Index file to drop all unnecessary columns, we only need the "Country Short Code" and "Region Name" to make our index

drop_columns = [" REGION TYPE", " REGIONAL NUMBER CODE"]
index = index.drop(columns = drop_columns, axis=0)

# Finding Canada (and Provinces) in the index list

canada_rows = index.loc["CA"]
canada_rows = canada_rows.reset_index()
canada_rows = canada_rows.drop(columns="COUNTRY SHORT CODE")

# Canada isn't present in the index list, adding Canada related info directly to the dataframe
canada_rows.loc[-1] = ["Canada", "CA"]
canada_rows = canada_rows.reset_index()
canada_rows = canada_rows.drop(columns="index")
canada_rows.index = canada_rows[" REGIONAL CODE"]
canada_rows = canada_rows.drop(columns=" REGIONAL CODE")
print(canada_rows)

# asking the user which province they would like to analyse
print("Hello, please input a province to analyse its historical land value changes. Input 'index' if you're not sure about the list of provinces and their abbreviations. ")
user_input = input()
if user_input == "index":
    print("Here are the provinces and their abbreviations.")
    print(canada_rows)
    print("Please select a province in the above list.")
    user_input = input()
else:
    pass
print("Thank you for choosing a province! Here's the past land value trend.")

# using the user provided input to select the corresponding data from df
user_input = canada_rows.loc[user_input]
selected_province = df.loc[user_input]

# making a basic graph showing the land value trend based on the selected province
date_value = selected_province.loc[:, "REF_DATE"]
monetary_value = selected_province.loc[:, "VALUE"]
plt.plot(date_value, monetary_value)
plt.title('Historical Land Value Trend')
plt.xticks(ticks=range(2020, 2025, 1))
plt.xlabel('Year')
plt.ylabel('Land Value (CAD)')
for x,y in zip(date_value, monetary_value):
    plt.plot(x, y, 'bo-')
plt.grid(True)
plt.show()











