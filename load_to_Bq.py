import os
import argparse
import requests
import gzip
import shutil
from time import time
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
def extract_from_postgres(color):
    connection_block = SqlAlchemyConnector.load("posgres")
    with connection_block.get_connection() as engine:
        query = f"SELECT * FROM {color}_taxi_trips"
        df = pd.read_sql_query(query, engine)
        return df

@task()
def write_bq(color, df: pd.DataFrame):
    try:
        
        gcp_credentials_block = GcpCredentials.load("cred0111")
        df.to_gbq(
            destination_table= f"subtle-seer-403504.nytaxi.{color}_taxi_trips",
            project_id= "subtle-seer-403504",
            credentials= gcp_credentials_block.get_credentials_from_service_account(),
            chunksize= 500_000,
            if_exists= "replace"
        )
        print("Data successfull load to BigQuery.")
    except Exception as e:
        print(f"Data Failed writing load to BigQuery: {e}")
        raise

@flow()
def load_postgre_to_bq (color):
    df = extract_from_postgres(color)
    write_bq(color, df)


if __name__ == "__main__":
    color = 'yellow'
    load_postgre_to_bq(color)
    




