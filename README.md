# IE 421 - Data Science for Engineers Term Project

### Motor Vehicle Collisions Analysis - Beyond the Noise
&emsp;This study aims to analyze motor vehicle collisions in New York City between 2021 and 2025 using data science methodologies. Utilizing the NYC Open Data API, more than 1.3 million accident records were processed through an extensive data cleaning pipeline. In this phase, 2,300 unique vehicle descriptions and 60 distinct contributing factors were consolidated into primary categories to reduce data complexity and improve analytical accuracy. Methodologically, descriptive logistic regression was chosen over predictive modeling to better analyze the impact of individual variables within the high-variance dataset. By interpreting results through Odds Ratios, the research scientifically evaluates how the time of day, weekend status, vehicle categories, and contributing factors influence the likelihood of injuries or fatalities. These statistical insights are complemented by an interactive Leaflet map that visualizes the spatial distribution of accidents across the city. Representing a complete end-to-end data science workflow—from data ingestion and preprocessing to modeling and visualization—this project provides a data-driven foundation for urban safety strategies. Overall, the work demonstrates the capacity to extract meaningful and actionable insights from large-scale, complex urban systems.

### Team Members
* **Belinay Keleş** - 122203088
* **Ahmet Kağan Çelenk** - 121203114
* **İrem Ural** - 121203037
* **Sude Şintürk** - 121203034

### Files
* Dataset: Contains preprocessed NYC Motor Vehicle Collisions datasets used throughout the analysis.
* Images: Includes generated figures such as the descriptive logistic regression charts and the interactive Leaflet collision map.<br>
  &emsp;***Interaction of Vehicle Types and Crash Causes:*** This graph illustrates the average risk of casualties per collision resulting from the interaction between different vehicle types and contributing factors such as distraction, environmental conditions, and impairment.<br>
  &emsp;***Urban Vulnerability Analysis:*** This graph illustrates the distribution of road user casualties (injured and killed) by road user type across the five boroughs of New York.<br>
  &emsp;***Factors Associated with Casualty Occurence:*** This graph analyzes the factors influencing the probability of a traffic accident resulting in a casualty based on Odds Ratios.<br>
  &emsp;***NYU Collision Interactive Map:*** This interactive map geographically visualizes traffic collision data across the five main boroughs of New York City from 2021 to 2025, providing detailed data for each borough such as the total number of collisions, injury statistics, and highest-risk hours.<br>
* Scripts: Holds the source code for data preprocessing and descriptive model.
* index.html: Serves as the main webpage for GitHub Pages to host the project's interactive findings and summary.
* requirements.txt: Lists the necessary Python libraries and dependencies required to execute the data preprocessing and analysis scripts successfully. Open a terminal or command prompt in the project folder, install the required libraries by running: pip install --no-cache-dir -r requirements.txt


### Hosting


Website GitHub Repository -> https://github.com/iremmural/beyond-the-noise_Website.git <br>
Website link ->  https://bilgi-ie-421.github.io/ie421-2025-2026-1-termproject-beyond-the-noise/




