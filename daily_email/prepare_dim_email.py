from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
hostname = os.getenv("hostname")
database_name = os.getenv("database_name")
engine_uri = f"postgresql://{username}:{password}@{hostname}/{database_name}"
sql_engine = create_engine(engine_uri)
connection = sql_engine.raw_connection()

df = pd.read_sql("SELECT * FROM Users ORDER BY id", con=connection)
total_signups = len(df)
df_previous = pd.read_csv("~/Desktop/dims_leads_previous.csv")
print(df_previous['id'].max())
print(f"total signups: {total_signups}")

df = df.loc[df['id'] > df_previous['id'].max()]
print(df)

df['created_at_v2'] += pd.Timedelta(hours=3)
df['date'] = df['created_at_v2'].dt.date

print(df_previous)
assert len(df) + len(df_previous) <= total_signups
assert len(df) > 0
df.to_csv("~/Desktop/dims_leads_previous.csv", index=False)

df_email = df[['name', 'email', 'phone', "id"]]
df_email.to_csv("~/Desktop/dims_leads.csv", index=False)