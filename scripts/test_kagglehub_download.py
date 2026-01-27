import os
from pathlib import Path
import pandas as pd
import kagglehub

DATASET = "olistbr/brazilian-ecommerce"

EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]

def main():
    # Quick sanity: secrets should exist (provided by GitHub Actions env)
    ku = os.getenv("KAGGLE_USERNAME")
    kk = os.getenv("KAGGLE_KEY")
    if not ku or not kk:
        raise RuntimeError("Missing KAGGLE_USERNAME or KAGGLE_KEY environment variables.")

    # Download via kagglehub
    dataset_path = Path(kagglehub.dataset_download(DATASET))
    print("✅ Downloaded dataset to:", dataset_path)

    # Check required files exist
    missing = [f for f in EXPECTED_FILES if not (dataset_path / f).exists()]
    if missing:
        raise FileNotFoundError(f"Missing expected files: {missing}")

    print("✅ All expected CSV files exist.")

    # Load one file + basic checks
    orders_path = dataset_path / "olist_orders_dataset.csv"
    df = pd.read_csv(orders_path)

    print("orders rows:", len(df))
    print("orders cols:", list(df.columns))

    if len(df) < 1000:
        raise AssertionError("Orders dataset looks too small — download may be wrong.")
    if "order_id" not in df.columns:
        raise AssertionError("order_id column missing — dataset schema unexpected.")

    # Optional: verify order_id uniqueness (not strictly required, but good sanity)
    uniq = df["order_id"].nunique()
    print("unique order_id:", uniq)

    print("🎉 SMOKE TEST PASSED")

if __name__ == "__main__":
    main()