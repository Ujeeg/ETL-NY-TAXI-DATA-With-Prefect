# ETL-NY-TAXI-DATA-With-Prefect

![](https://github.com/Ujeeg/ETL-NY-TAXI-DATA-With-Prefect/blob/4d007f876becd48befa652d14a190e0f49dd17c3/Picture/RoadMap.png)


# Overview:

The aim of this data engineering project is to create a robust ETL (Extract, Transform, Load) pipeline to process data from a GitHub data source (NY-Taxi-data), store it in a local PostgreSQL database, and subsequently load it into Google BigQuery for further analysis. This project involves collecting data from GitHub, transforming it into a suitable format, and efficiently storing it in both a local PostgreSQL database and Google BigQuery.



# Steps:

## Create local storeage (PgAdmin) using Docker:
1. Create PgAdmin Connection
2. Create local DataBase
 ![Connection Setup with docker](https://github.com/Ujeeg/ETL-NY-TAXI-DATA-With-Prefect/blob/4d007f876becd48befa652d14a190e0f49dd17c3/local%20Storage/Setting%20Network%20Manually.yml)

## Create python scripts file Data Flow and Task with Prefect :
## 1. File 1 to ETL to local postgre
![Source Code](https://github.com/Ujeeg/ETL-NY-TAXI-DATA-With-Prefect/blob/8304d5483a3366f67cbdb33376de48a4c6b53b4f/ingest_data.py)

### Data Extraction :
1. downdload file data from url
2. compressing file from csv.gzip to csv

### Data Transform   
1. transform data to datetime
2. clean and preprocessing the extracted tade to handle missing value

### Load to local storage (PostgreSQL)
1. Create Postgre Block in prefect
2. Load data to local storage with connection block prefect_SqlAlchemy

## 2. File 2 to Load data from local postgre to BigQuery
![Source Code](https://github.com/Ujeeg/ETL-NY-TAXI-DATA-With-Prefect/blob/8304d5483a3366f67cbdb33376de48a4c6b53b4f/load_to_Bq.py)
### Data Loading to BigQuery
1. Set up a Google Cloud Platform (GCP) project and enable BigQuery.
2. Create database in BigQuery that mirror the structure of the local PostgreSQL database.
3. Create Block Google Credentian and setting IAM admin
4. Load Data from PostgreSql to BigQuery

### Create Deployment
1. Create deployment ingst data in Prefect
2. Setup deployment in prefert UI
3. Test deployment
- lngest_data.py Flow
![](https://github.com/Ujeeg/ETL-NY-TAXI-DATA-With-Prefect/blob/0471692e463e6d1585492497764b696c6fb79401/Picture/ingest%20data%20flow.jpg)

- local_to_Bq.py Flow
![](https://github.com/Ujeeg/ETL-NY-TAXI-DATA-With-Prefect/blob/main/Picture/Load_to_bq%20flow.jpg)



### Scheduling and Automation
1. Lmplement scheduling mechanisms  Prefect flows to run the ETL pipeline at predefined intervals
2. Automate the entire ETL process to ensure regular updates.

# Technology and Tools:
1. Docker
2. VS code
3. Python (pandas, prefect, sqlalchemy)
4. Github API
5. Prefect
6. Google Cloud Platform (BigQuery)

# Deliverables:
1. Python scripts for ETL pipeline.
2. SQL scripts for PostgreSQL database schema creation.
3. Documentation detailing the ETL process, schema design, and any relevant information.
4. Scheduled and automated ETL pipeline.

# Conclusion:
This project aims to create a scalable and efficient ETL pipeline that extracts valuable insights from GitHub data, stores it locally for quick analysis, and further loads it into BigQuery for more extensive and complex analytics. The combination of local storage and cloud-based data warehousing allows for flexibility and optimization in handling different aspects of data engineering. 

# Notes :
Typically, in ETL processes using GCP, data is extracted, transformed, and loaded into a bucket, then transformed again before being loaded into the BigQuery data warehouse. However, in this case, I don't have a premium GCP account, so I am seeking an alternative bucket, namely local PostgreSQL


   
