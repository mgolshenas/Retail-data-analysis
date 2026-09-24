import pandas as pd
from sqlalchemy import create_engine
import os

# 1. Database Configuration Parameters
db_user = 'postgres'
db_password = 'password'  
db_host = 'localhost'
db_port = '5432'
db_name = 'Retail_analytics'

# 2. Locate the Raw Data File
# Put your downloaded dataset in the same folder as this script
raw_file = r"C:\...\Ecommerce_Data.csv"

if not os.path.exists(raw_file):
    print(f"Error: Could not find '{raw_file}' in this directory.")
    print("Please make sure your downloaded Kaggle file is placed in this folder "
          "and matches the name.")
else:
    print("Pipeline started. Loading raw dataset...")

    # 3. Read Data
    if raw_file.endswith('.csv'):
        df = pd.read_csv(raw_file, encoding='ISO-8859-1')
    else:
        df = pd.read_excel(raw_file)

    print(f"Raw Data Loaded: Found {len(df):,} records.")

    # 4. Data Cleansing
    print("Commencing data sanitation...")

    # Remove duplicate transactions
    df = df.drop_duplicates()

    # Drop records where CustomerID is completely missing
    df = df.dropna(subset=['CustomerID'])

    # Standardise column names to lowercase
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Convert dates to datetime
    df['invoicedate'] = pd.to_datetime(df['invoicedate'])

    # Remove negative quantities/prices and cancellation transactions
    df = df[(df['quantity'] > 0) & (df['unitprice'] > 0)]

    # Convert CustomerID to integer
    df['customerid'] = df['customerid'].astype(int)

    print(
        f"Data Sanitized: {len(df):,} valid rows remaining "
        "after filtering operational anomalies."
    )

    # 5. Connect and Transfer Data to PostgreSQL
    print("Establishing connection to PostgreSQL...")

    engine = create_engine(
        f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )

    print("Loading data into the 'raw_transactions' database table...")

    df.to_sql(
        'raw_transactions',
        engine,
        if_exists='replace',
        index=False
    )

    print(
        "Pipeline executed successfully! "
        "Your clean database table is ready inside pgAdmin."
    )






