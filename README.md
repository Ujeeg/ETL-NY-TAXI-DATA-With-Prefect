# ETL-NY-TAXI-DATA-With-Prefect


# Overview:

The aim of this data engineering project is to create a robust ETL (Extract, Transform, Load) pipeline to process data from a GitHub data source (NY-Taxi-data), store it in a local PostgreSQL database, and subsequently load it into Google BigQuery for further analysis. This project involves collecting data from GitHub, transforming it into a suitable format, and efficiently storing it in both a local PostgreSQL database and Google BigQuery.



# Steps:

## Create local storeage (PgAdmin) using Docker:
1. Create PgAdmin Connection
2. Create local DataBase
   
## Data Extraction :
1. downdload file data from url
2. compressing file from csv.gzip to csv

## Data Transform
1. transform data to datetime
2. clean and preprocessing the extracted tade to handle missing value

## Load to local storage (PostgreSQL)
1. Create Postgre Block in prefect
2. Use Python and relevant libraries (e.g., pandas, SQLAlchemy) for ETL scripting.
3. Load data to local storage with connection block prefect_SqlAlchemy

## Data Loading to BigQuery
1. Set up a Google Cloud Platform (GCP) project and enable BigQuery.
2. Create database in BigQuery that mirror the structure of the local PostgreSQL database.
3. Create Block Google Credentian and setting IAM admin
4. Load Data from PostgreSql to BigQuery

## Create Deplooyment
1. Create deployment ingst data in Prefect
2. Setup deployment in prefert UI
3. Test deployment

## Scheduling and Automation
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

   
