import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from os import environ

USERNAME = environ["POSTGRES_USER"]
PASSWORD = environ["POSTGRES_PASSWORD"]
HOST = environ["POSTGRES_HOST"]
PORT = environ["POSTGRES_PORT"]
DATABASE = environ["POSTGRES_DB"]

files = [
    "1_market_access.parquet",
    "2_bdmo_population.parquet",
    "3_bdmo_migration.parquet",
    "4_bdmo_salary.parquet",
    "5_connection.parquet",
]
tables = [
    "market_access",
    "bdmo_population",
    "bdmo_migration",
    "bdmo_salary",
    "connection",
]

url = URL.create(
    drivername="postgresql",
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DATABASE
)

engine = create_engine(url)

for file, table in zip(files, tables):
    df = pd.read_parquet(file, engine="fastparquet")
    df.to_sql(table, engine, if_exists="replace", index=False)

excel_file = "t_dict_dict_municipal_districts.xlsx"
table = "municipal_districts"
df = pd.read_excel(excel_file, sheet_name="Sheet1")
df.to_sql(table, engine, if_exists="replace", index=False)
