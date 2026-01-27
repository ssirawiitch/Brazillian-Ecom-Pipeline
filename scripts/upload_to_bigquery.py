import os
import json
from pathlib import Path
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import kagglehub

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
DATASET_ID = "olist"
TABLE_ID = "orders"

def main():
    # Load service account from GitHub secret
    sa_info = json.loads(os.environ["GCP_SA_KEY"])
    credentials = service_account.Credentials.from_service_account_info(sa_info)

    client = bigquery.Client(
        credentials=credentials,
        project=PROJECT_ID,
    )

    # Download dataset via kagglehub
    dataset_path = Path(kagglehub.dataset_download("olistbr/brazilian-ecommerce"))
    orders_csv = dataset_path / "olist_orders_dataset.csv"

    print("Reading:", orders_csv)
    df = pd.read_csv(orders_csv)

    # Create dataset if not exists
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset_ref.location = "US"
    client.create_dataset(dataset_ref, exists_ok=True)

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # overwrite daily
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
    )

    job = client.load_table_from_dataframe(
        df,
        table_ref,
        job_config=job_config,
    )

    job.result()  # wait

    print(f"✅ Loaded {len(df)} rows into {table_ref}")

if __name__ == "__main__":
    main()