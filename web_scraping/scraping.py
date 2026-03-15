import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import date

sites = pd.read_csv("websites.csv")
dataset = []


for _, row in sites.iterrows():
    """
    Iterates over each website in the CSV file.
    For each site, the script retrieves its HTML content and extracts relevant numeric data based on the source type.
    """

    country = row["country"]
    source = row["website"]
    url = row["url"]
    print(f"Procesare site: {country} - {source}")
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        text = soup.get_text()
    except:
        print("Nu s-a putut accesa site-ul:", url)
        continue


    if source == "livingcost":
        """
        Processes tables from livingcost.org.
        Extracts numeric values for rent, food, transport, and salary after tax, then appends them to the dataset with corresponding indicators.
        """

        rows = soup.find_all("tr")
        for r in rows:
            row_text = r.get_text()
            numbers_raw = re.findall(r'\d[\d,\.]*', row_text)
            numbers = []
            for n in numbers_raw:
                if n.count('.') > 1: 
                    continue
                try:
                    numbers.append(float(n.replace(",", ".")))
                except:
                    continue
            if not numbers:
                continue
            value = numbers[0]

            if "Rent & Utilities" in row_text:
                dataset.append([date.today(), country, source,
                                "rent_utilities", value])
            elif "Food" in row_text:
                dataset.append([date.today(), country, source,
                                "food_cost", value])
            elif "Transport" in row_text:
                dataset.append([date.today(), country, source,
                                "transport_cost", value])
            elif "Monthly salary after tax" in row_text:
                dataset.append([date.today(), country, source,
                                "salary_after_tax", value])

   
    elif source == "statistics_md":
        """
        Extracts employment total and employment rate from Moldova’s statistics site using regex.
        Adds the values to the dataset for later analysis.
        """

        match_total = re.search(r"Employment, thou\.\s*([\d,\.]+)", text)
        match_rate = re.search(r"Employment rate, %\s*([\d,\.]+)", text)
        if match_total:
            try:
                val_total = float(match_total.group(1).replace(",", "."))
                dataset.append([date.today(), country, source,
                                "employment_total", val_total])
            except:
                pass
        if match_rate:
            try:
                val_rate = float(match_rate.group(1).replace(",", "."))
                dataset.append([date.today(), country, source,
                                "employment_rate", val_rate])
            except:
                pass

   
    elif source == "destatis":
        """
        Extracts employment total and employment rate from Germany’s Destatis site using regex.
        Converts units if needed and appends data to the dataset.
        """

        match_total = re.search(r"([\d,\.]+)\s*(mn|million|mio|Mio).*persons in employment", text, re.IGNORECASE)
        match_rate = re.search(r"(\d{1,3}\.\d)%\s*employment rate", text, re.IGNORECASE)

        if match_total:
            try:
                val = float(match_total.group(1).replace(",", "."))
                
                if match_total.group(2).lower() in ["mn", "million", "mio"]:
                    val *= 1000 
                dataset.append([date.today(), country, source,
                                "employment_total", val])
            except:
                pass

        if match_rate:
            try:
                val = float(match_rate.group(1))
                dataset.append([date.today(), country, source,
                                "employment_rate", val])
            except:
                pass

df = pd.DataFrame(dataset, columns=["date", "country", "source", "indicator", "value"])
"""
Converts the collected list of records into a pandas DataFrame.
This structured format is used for cleaning, unit assignment, and storage.
"""
df.loc[df['indicator'] == 'employment_total', 'value'] /= 1000
pd.options.display.float_format = '{:g}'.format


def get_unit(ind):
    """
    Defines the measurement unit for each indicator.
    Returns 'M' for employment total, '%' for employment rate, and '$' for cost-related indicators.
    """

    if ind == 'employment_total':
        return 'M'       
    elif ind == 'employment_rate':
        return '%'      
    else:
        return '$'       

df['unit'] = df['indicator'].apply(get_unit)
df['date'] = df['date'].astype(str)


df.to_hdf("dataset.h5", key="data", mode="a", format="table", append=True)
"""
Stores the cleaned and processed DataFrame into an HDF5 file.
Allows appending new daily observations without overwriting existing data.
"""

print(df)