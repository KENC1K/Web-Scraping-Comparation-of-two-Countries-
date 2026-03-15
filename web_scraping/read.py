import pandas as pd

df = pd.read_hdf("dataset.h5", key="data")
print(df)
"""
Loads the HDF5 dataset into a pandas DataFrame for analysis and preview.
"""

print(df.head())