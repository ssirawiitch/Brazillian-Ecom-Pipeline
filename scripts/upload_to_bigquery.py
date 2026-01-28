import os
import json
from pathlib import Path
import pandas as pd
import kagglehub
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = os.environ["PROJECT_ID"]
DATASET_ID = "olist"

CSV_TABLE_MAP = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_name",
}

def main():
    sa_info = json.loads(os.environ["BIGQUERY_TOKEN"])
    credentials = service_account.Credentials.from_service_account_info(sa_info)
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset_ref.location = "US"
    client.create_dataset(dataset_ref, exists_ok=True)

    dataset_path = Path(kagglehub.dataset_download("olistbr/brazilian-ecommerce"))
    print("Dataset cache path:", dataset_path)

    for csv_name, table_name in CSV_TABLE_MAP.items():
        csv_path = dataset_path / csv_name
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing file: {csv_path}")

        print(f"Reading: {csv_path}")
        df = pd.read_csv(csv_path)

        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            autodetect=True,
        )

        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()

        print(f"✅ Loaded {len(df)} rows into {table_ref}")

    print("🎉 All tables uploaded")

if __name__ == "__main__":
    main()