from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
import prepare_email_helpers
pd.options.mode.chained_assignment = None  # default='warn'


load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
hostname = os.getenv("hostname")
database_name = os.getenv("database_name")
engine_uri = f"postgresql://{username}:{password}@{hostname}/{database_name}"
sql_engine = create_engine(engine_uri)
connection = sql_engine.raw_connection()

complete_df = pd.read_sql("SELECT * FROM Users ORDER BY id", con=connection)
complete_df = complete_df.groupby(["name", "session_id"], as_index=False).first()
max_backup_file_suffix: int = prepare_email_helpers.get_backup_file_suffix()
complete_df.to_parquet(f"../user_db_backup/database_backup_{max_backup_file_suffix}.parquet")

total_signups = len(complete_df)
df_previous = pd.read_csv("~/Desktop/dims_leads_previous.csv")

print(f"Previous csv save max id: {df_previous['id'].max()}")
print(f"total signups: {total_signups}")

new_df = complete_df.loc[complete_df['id'] > df_previous['id'].max()]
new_df = new_df[new_df['email'] != "test@test.com"]

print("New signup dataframe after filtering by old max id:")
print(new_df)
print()
new_df['created_at_v2'] += pd.Timedelta(hours=3) # adjust date to be EST
new_df['date'] = new_df['created_at_v2'].dt.date # Get the date format without hour or timezone.
print("Previous signup dataframe from csv:")
print(df_previous)

assert len(new_df) + len(df_previous) <= total_signups
assert len(new_df) > 0

new_df.to_csv("~/Desktop/dims_leads_previous.csv", index=False)

df_email = new_df[['name', 'email', 'phone', "id"]]
df_email.to_csv("~/Desktop/dims_leads.csv", index=False)
print("Writing csv success!")