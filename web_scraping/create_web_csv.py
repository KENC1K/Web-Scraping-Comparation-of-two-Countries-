import csv

data = [
["country","category","website","url"],
["Germany","cost_of_living","livingcost","https://livingcost.org/cost/germany"],
["Germany","employment","destatis","https://www.destatis.de/EN/Themes/Labour/Labour-Market/Employment/_node.html"],
["Moldova","cost_of_living","livingcost","https://livingcost.org/cost/moldova"],
["Moldova","employment","statistics_md","https://statistica.gov.md/en/statistic_indicator_details/1"]
]
"""
List of selected web sources used for scraping.
Each row stores the country, data category, website name, and URL.
"""


with open("websites.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(data)
print("websites.csv successfully created")
"""
Creates the websites.csv file and writes all source links into it.
The file allows the scraping script to easily read and iterate through the websites.
"""