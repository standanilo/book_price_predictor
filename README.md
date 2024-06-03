# Book Price Predictor
This project aims to implement various tasks related to data collection, processing, analysis, and modeling based on book data obtained from web page www.knjizare-vulkan.rs.

Implemented Tasks

1. Web Indexer and Parser
Implemented a web indexer, also known as a web crawler or spider, along with a web parser (scraper) to collect data about books from online sources.

2. Data Filtering
Filtered the collected data from web crawler, rejecting records with insufficient field values. The filtered data is stored in a new file with a minimum of 15,000 records.

3. Data Analysis & Visualization
Performed data analysis on the records from filtered data, visualizing relevant data points to derive insights.

4. Model Building / Linear & Logistic Regression
Created a small application to build predictive models based on records from the filtered database. Implemented linear regression, logistic regression (both multinomial and binary - one-vs-one approach), predicting the book value based on carefully chosen features.

5. K-Means Clustering
Applied the K-Means clustering method to multiple input attributes observed from the filtered books in multiple iterations to analyze data patterns and clusters.
