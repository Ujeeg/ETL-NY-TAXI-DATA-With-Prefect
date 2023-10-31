import os
import argparse
import requests
import gzip
import shutil
from time import time
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector

@task()
def download_file(url,destination):
    with requests.get(url, stream=True) as response:
            with open(destination, 'wb') as file:
                 shutil.copyfileobj(response.raw, file)

@task()
def compressing_file(destination):
    with gzip.open(destination, 'rt') as f_in, open(destination[:-3], 'w') as f_out:
         shutil.copyfileobj(f_in, f_out)


@task()
def transform_file(csv_path):
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
def ingest_data(table_name, data):
    connection_block= SqlAlchemyConnector.load("posgres")

    with connection_block.get_connection(begin=False) as engine:
        
        data.head(n=0).to_sql(name=table_name, con=engine, if_exists='append')
        
        data.to_sql(name=table_name, con=engine, if_exists='append')
        return data

@flow()
def main_flow(table_name: str, year: int, month: int, color: str):
     dataset = f"{color}_tripdata_{year}-{month:02}"
     url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset}.csv.gz"
     destination = f"data/yellow/{dataset}.csv.gz"
     csv_path = f"data/yellow/{dataset}.csv"
     download_file(url, destination)
     compressing_file(destination)
     df = transform_file(csv_path)
     data = transform_passenger(df)
     ingest_data(table_name, data)

@flow()
def parent_flows(months: list[int] = [1,2], year: int = 2021, color: str = "yellow") -> None:
     
     for month in months:
         main_flow( f"{color}_taxi_trips", year, month, color)

    


if __name__=="__main__":
    color = "yellow"
    months= [1,2]
    year = 2021
    parent_flows(months, year, color)
