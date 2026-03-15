import pandas as pd
from datetime import date, timedelta
import random

base_data = [
    {"country":"Germany","source":"livingcost","indicator":"rent_utilities","value":924,"unit":"$"},
    {"country":"Germany","source":"livingcost","indicator":"food_cost","value":552,"unit":"$"},
    {"country":"Germany","source":"livingcost","indicator":"transport_cost","value":129,"unit":"$"},
    {"country":"Germany","source":"livingcost","indicator":"salary_after_tax","value":3290,"unit":"$"},
    {"country":"Germany","source":"destatis","indicator":"employment_total","value":45.5,"unit":"M"},
    {"country":"Germany","source":"destatis","indicator":"employment_rate","value":77.3,"unit":"%"},
    {"country":"Moldova","source":"livingcost","indicator":"rent_utilities","value":467,"unit":"$"},
    {"country":"Moldova","source":"livingcost","indicator":"food_cost","value":284,"unit":"$"},
    {"country":"Moldova","source":"livingcost","indicator":"transport_cost","value":30.5,"unit":"$"},
    {"country":"Moldova","source":"livingcost","indicator":"salary_after_tax","value":351,"unit":"$"},
    {"country":"Moldova","source":"statistics_md","indicator":"employment_total","value":0.8064,"unit":"M"},
    {"country":"Moldova","source":"statistics_md","indicator":"employment_rate","value":40.8,"unit":"%"},
]


end_date = date(2026, 3, 9)

dates = [end_date - timedelta(days=i) for i in reversed(range(5))]  

simulated_dataset = []

for d in dates:
    for entry in base_data:
        """
        Simulates daily variations for the past 5 days.
        Applies a ±5% random change to each indicator value and appends the results to the simulated dataset.
        """
        variation = entry["value"] * random.uniform(-0.05, 0.05)
        new_value = round(entry["value"] + variation, 2)
        simulated_dataset.append([
            d.strftime("%Y-%m-%d"),
            entry["country"],
            entry["source"],
            entry["indicator"],
            new_value,
            entry["unit"]
        ])


df = pd.DataFrame(simulated_dataset, columns=["date","country","source","indicator","value","unit"])
"""
Converts the simulated dataset into a pandas DataFrame.
Prepares the data for storage and further analysis like the real collected data.
"""

df.to_hdf("dataset.h5", key="data", mode="a", format="table", append=True)
"""
Appends the simulated daily data into the existing HDF5 dataset.
This allows continuous testing of analysis and visualization without accessing live websites.
"""

print("Simulated data with small variations for 5 past days added to dataset.h5")
print(df)