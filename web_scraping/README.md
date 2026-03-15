# Web Scraping and Data Analysis Project

This project demonstrates automated web scraping, data processing, and visualization for comparing cost of living, salaries, and employment indicators between Germany and Moldova.

## 📁 Project Structure
```text
project-folder/
│
├── websites.csv              # List of websites to scrape
├── dataset.h5                # HDF5 dataset storing scraped and simulated data
├── create_web_csv.py         # Script to create the websites CSV
├── read.py                   # Script to read or preview the dataset
├── scraping.py               # Script for web scraping and data extraction
├── simulated_data.py         # Script for generating simulated daily variations
├── visualization.py          # Script for plotting line charts, bar charts, and heatmaps
├── visualisations/           # Folder where generated graphs are saved
├── requirements.txt          # Project dependencies
└── README.md                 # This file
````

## ⚙️ Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
````

Dependencies:

* `pandas` – data manipulation and HDF5 storage
* `requests` – HTTP requests for scraping
* `beautifulsoup4` – HTML parsing
* `matplotlib` – plotting line and bar charts
* `seaborn` – advanced visualization
* `lxml` / `html5lib` – alternative HTML parsers for BeautifulSoup


## 📝 Scripts

### 1. `scrape_websites.py`

* Reads the `websites.csv` file.
* Scrapes numeric data from selected websites.
* Cleans, structures, and saves the data into `dataset.h5`.
* Handles different HTML structures for each source.

### 2. `simulate_data.py`

* Generates simulated data for the past 5 days.
* Applies ±5% random variation to each indicator.
* Appends simulated data to `dataset.h5`.

### 3. `visualize_data.py`

* Loads the dataset from `dataset.h5`.
* Creates multiple visualizations:

  * Line chart of cost of living components
  * Salary comparison bar chart
  * Employment rate trend line chart
  * Total employment bar chart
  * Heatmaps of cost indicators for Germany and Moldova
* Saves all graphs to the `visualisations/` folder.


## 🧩 How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
````

2. Create the CSV with websites:

```bash
python create_web_csv.py
```

3. Read or preview the dataset:

```bash
python read.py
```

4. Run the scraping script to collect data:

```bash
python scraping.py
```

5. Optional: generate simulated data for testing:

```bash
python simulated_data.py
```

6. Generate all visualizations:

```bash
python visualization.py
```

All generated graphs will be saved in the `visualisations/` folder.




## ⚠️ Notes

* Make sure scraping complies with each website’s terms of use.
* The HDF5 dataset allows appending new data without overwriting existing observations.
* Simulated data is for testing purposes and represents ±5% daily variations.


