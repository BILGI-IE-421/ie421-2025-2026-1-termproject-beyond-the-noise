# Motor Vehicle Collisions Analysis

## Beyond the Noise

### Team Members
* **Belinay Keleş** - 122203088
* **Ahmet Kağan Çelenk** - 121203114
* **İrem Ural** - 121203037
* **Sude Şintürk** - 121203034

## Data

* **Dataset Name:** Motor Vehicle Collisions - Crashes
* **Source:** NYC Open Data
* **Link:** [Motor Vehicle Collisions - Crashes](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data)

## Research Questions
Q1: How does the frequency of accidents vary by time of day and by different boroughs of New York; can "danger hours" and "danger zones" be identified?

Q2: Is there a clear relationship between different crash causes and the types of vehicles involved that increase injury or death rates?

Q3: Can the number of injuries in an accident be predicted using variables such as accident time, location, vehicle type, and cause of accident?

## Data Preprocessing

Extensive data preprocessing was conducted to ensure data quality, reduce noise, and focus the analysis on relevant crash scenarios. The following steps outlined the cleaning pipeline:

* **Initial Missing Value Handling:** Rows containing null values in critical identifying columns, specifically CRASH TIME and BOROUGH, were removed.

* **Focusing on 1-2 Vehicle Crashes:** The scope was narrowed to incidents involving only one or two vehicles. Rows where vehicle/factor information existed for a 3rd, 4th, or 5th vehicle were dropped. Subsequently, columns related to vehicles 3, 4, and 5 were removed entirely from the dataset.

* **Dimensionality Reduction (Feature Dropping):** High-cardinality location features considered unnecessary for this specific analysis were dropped to reduce noise. These included ZIP CODE, LATITUDE, LONGITUDE, LOCATION, and all street name columns (ON STREET NAME, CROSS STREET NAME, OFF STREET NAME).

* **Preserving Single-Vehicle Incidents:** A targeted null handling strategy was applied. While most remaining system nulls were cleared, missing values in VEHICLE TYPE CODE 2 and CONTRIBUTING FACTOR VEHICLE 2 were explicitly filled with "Not Applicable". This ensured that single-vehicle crashes were not lost during data cleaning.

* **Feature Engineering - Vehicle Type Standardization:**
The raw vehicle type data contained high noise (typos, redundant categories). Analysis showed the top 20 vehicle types covered 97% of the data.

These top types were consolidated into broader categories (e.g., grouping "bike", "motorcycle", "bicycle" into "two wheeled"). Rare or irrelevant types outside this consolidated list were removed.

* **Feature Engineering - Contributing Factor Standardization:**
Similar to vehicle types, over 80 diverse contributing factors were analyzed. Nonsensical values were removed.

Remaining factors were grouped into actionable categories such as "distraction", "unsafe driving", "impairment", and "vehicle defect".

* **Categorical Encoding:** The newly standardized vehicle type and contributing factor columns underwent categorical encoding to prepare them for analysis.

* **Temporal Filtering:** The dataset, originally dating back to 2012, was filtered to focus on the most recent trends between 2021 and 2025.

## Model

## Visuals 
Below are selected insights derived from the cleaned and processed NYC collision data.

* **Vehicle Type vs. Crash Cause Interaction**
This heatmap visualizes the relationship between the types of vehicles involved and the primary contributing factors, color-coded by the average number of casualties per collision.

![Urban System Risk Analysis](Visuals/comprehensive_risk_matrix_v2.jpg)

**Insight:** This heatmap reveals that **two-wheeled vehicles** face the highest risk, with average casualties per collision reaching near-maximum levels (0.86 - 0.99) across all contributing factors, especially during **impairment-related** incidents.

* **Vulnerability by Borough and User Type**
This chart highlights the distribution of total casualties (injured + killed) across NYC boroughs, segmented by the type of road user (pedestrians, cyclists, or motorists).

![Urban Vulnerability Analysis](Visuals/urban_vulnerability_distribution.png)

**Insight:** **Brooklyn** and **Queens** exhibit the highest volume of total casualties; notably, Brooklyn leads in motorist injuries, while Manhattan shows a high concentration of pedestrian and cyclist casualties relative to its size.

* **High-Risk Hours Across Boroughs**
A temporal heatmap identifying the "danger hours" within each borough, showing peak times for collision risks throughout the day (00:00 - 23:00).

![Urban Risk Analysis: Danger Hours](Visuals/crash_density_heatmap_optimized.png)

**Insight:** The relative risk peak is synchronized across all boroughs, identifying the window between **14:00 and 19:00 (Rush Hour)** as the most dangerous period for commuters in New York City.

