import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.lines import Line2D


os.makedirs("visualisations", exist_ok=True)

df = pd.read_hdf("dataset.h5", key="data")

df["value"] = pd.to_numeric(df["value"], errors="coerce")

df = df.groupby(["country","indicator","date"], as_index=False)["value"].mean()

df = df.sort_values("date")

money_indicators = [
    "salary_after_tax",
    "rent_utilities",
    "food_cost",
    "transport_cost"
]



"""
COST OF LIVING LINE CHART
 Generates a line chart showing cost of living components over time for Germany and Moldova.
Lines and colors distinguish indicators and countries to visualize trends in rent, food, and transport costs.
"""
plt.figure(figsize=(10,6))
cost_indicators = ["rent_utilities","food_cost","transport_cost"]
colors = {
    "rent_utilities": "blue",
    "food_cost": "green",
    "transport_cost": "red"
}
for ind in cost_indicators:

    g = df[(df.country=="Germany") & (df.indicator==ind)]
    m = df[(df.country=="Moldova") & (df.indicator==ind)]

    plt.plot(
        g.date,
        g.value,
        color=colors[ind],
        linestyle="-",
        marker="o"
    )

    plt.plot(
        m.date,
        m.value,
        color=colors[ind],
        linestyle="--",
        marker="o",
        markerfacecolor="none"
    )

plt.title("Cost of Living Components")
plt.ylabel("USD")
plt.xticks(rotation=45)

indicator_legend = [
    Line2D([0], [0], color="blue", lw=2, label="Rent & Utilities"),
    Line2D([0], [0], color="green", lw=2, label="Food Cost"),
    Line2D([0], [0], color="red", lw=2, label="Transport Cost")
]

country_legend = [
    Line2D([0], [0], color="black", lw=2, linestyle="-", label="Germany"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="Moldova")
]

plt.legend(handles=indicator_legend + country_legend)
plt.tight_layout()
plt.savefig("visualisations/cost_of_living_lines.png")
plt.close()



"""
SALARY COMPARISON BAR
Creates a bar chart comparing average salaries after tax for the two countries.
Highlights differences in income levels at the latest available date.
"""
last_date = df.date.max()
salary = df[
    (df.indicator=="salary_after_tax") &
    (df.date==last_date)
]
plt.figure(figsize=(6,5))
sns.barplot(data=salary, x="country", y="value")
plt.title("Salary After Tax Comparison")
plt.ylabel("USD")
plt.tight_layout()
plt.savefig("visualisations/salary_bar.png")
plt.close()



"""
EMPLOYMENT RATE TREND
Plots employment rate trends over time for Germany and Moldova.
Shows the evolution of labor market participation in both countries.
"""
plt.figure(figsize=(8,5))
g = df[(df.country=="Germany") & (df.indicator=="employment_rate")]
m = df[(df.country=="Moldova") & (df.indicator=="employment_rate")]
plt.plot(g.date, g.value, marker="o", linestyle="-", label="Germany")
plt.plot(m.date, m.value, marker="o", linestyle="--", markerfacecolor="none", label="Moldova")
plt.title("Employment Rate Over Time")
plt.ylabel("%")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("visualisations/employment_rate_trend.png")
plt.close()



"""
EMPLOYMENT TOTAL COMPARISON
Generates a bar chart comparing total number of employed people in Germany and Moldova.
Summarizes workforce size at the most recent date.
"""
emp = df[
    (df.indicator=="employment_total") &
    (df.date==last_date)
]

plt.figure(figsize=(6,5))
sns.barplot(data=emp, x="country", y="value")
plt.title("Total Employment Comparison")
plt.ylabel("Number of Employed People")
plt.tight_layout()
plt.savefig("visualisations/employment_total_comparison.png")
plt.close()



"""
HEATMAP GERMANY
Creates a heatmap of Germany's monetary indicators across multiple days.
Quickly visualizes variations in rent, food, transport, and salary values.
"""
pivot_g = df[
    (df.country=="Germany") &
    (df.indicator.isin(money_indicators))
].pivot(
    index="indicator",
    columns="date",
    values="value"
)

plt.figure(figsize=(10,5))
sns.heatmap(pivot_g, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Germany Cost Indicators ($)")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("visualisations/heatmap_germany.png")
plt.close()



"""
HEATMAP MOLDOVA
Creates a heatmap of Moldova's monetary indicators across multiple days.
Allows fast visual comparison of cost trends with Germany.
"""
pivot_m = df[
    (df.country=="Moldova") &
    (df.indicator.isin(money_indicators))
].pivot(
    index="indicator",
    columns="date",
    values="value"
)

plt.figure(figsize=(10,5))
sns.heatmap(pivot_m, annot=True, fmt=".0f", cmap="YlOrRd")
plt.title("Moldova Cost Indicators ($)")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("visualisations/heatmap_moldova.png")
plt.close()


print("All graphs saved in 'visualisations' folder.")