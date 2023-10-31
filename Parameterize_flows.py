import os
import argparse
import requests
import gzip
import shutil
from time import time
from datetime import timedelta
import pandas_gbq
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector
from pathlib import Path
from prefect_gcp import GcpCredentials
from prefect_gcp.bigquery import BigQueryWarehouse



@task()
def download_file(url,destination):
    with requests.get(url, stream=True) as response:
            with open(destination, 'wb') as file:
                 shutil.copyfileobj(response.raw, file)

@task()
def compressing_file(destination):
    with gzip.open(destination, 'rt') as f_in, open(destination[:-3], 'w') as f_out:
         shutil.copyfileobj(f_in, f_out)

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def transform_file_datetime(csv_path):
     df = pd.read_csv(csv_path)
     df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
     df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
     return df


@task()
def transform_passenger(df):
    print(f"Pre:Missing passenger count: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0,inplace=True)
    print(f"Post:Missing passenger count: {df['passenger_count'].isna().sum()}")
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task(log_prints=True, retries=3)
def ingest_data(table_name, data_clean):
    connection_block= SqlAlchemyConnector.load("posgres")

    with connection_block.get_connection(begin=False) as engine:
        
        data_clean.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
        
        data_clean.to_sql(name=table_name, con=engine, if_exists='append')
        return data_clean


@task()
def extract_from_postgres():
    connection_block = SqlAlchemyConnector.load("posgres")
    with connection_block.get_connection() as engine:
        query = "SELECT * FROM yellow_taxi_trips"
        df = pd.read_sql_query(query, engine)
        return df

@task()
def write_bq(df: pd.DataFrame):
    try:
        
        gcp_credentials_block = GcpCredentials.load("cred0111")
        df.to_gbq(
            destination_table="subtle-seer-403504.nytaxi.yellow_taxi_trips",
            project_id="subtle-seer-403504",
            credentials=gcp_credentials_block.get_credentials_from_service_account(),
            chunksize=500_000,
            if_exists="append"
        )
        print("Data successfull load to BigQuery.")
    except Exception as e:
        print(f"Data Failed writing load to BigQuery: {e}")
        raise

    
    
@flow()
def main_flow(table_name: str, year: int, month: int, color: str) -> None:
     dataset = f"{color}_tripdata_{year}-{month:02}"
     url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset}.csv.gz"
     destination = f"data/yellow/{dataset}.csv.gz"
     csv_path = f"data/yellow/{dataset}.csv"
     download_file(url, destination)
     compressing_file(destination)
     df = transform_file_datetime(csv_path)
     data_clean = transform_passenger(df)
     ingest_data(table_name, data_clean)
     datapg= extract_from_postgres()
     write_bq(datapg)

@flow()
def parent_flows(months: list[int] = [1,2], year: int = 2021, color: str = "yellow") -> None:
     
     for month in months:
         main_flow(f"{color}_taxi_trips", year, month, color)
     

if __name__=="__main__":
    color = "yellow"
    months= [1,2,3]
    year = 2021
    parent_flows(months, year, color)



