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

complete_df = pd.read_sql("SELECT * FROM Users ORDER BY id", con=connection)

db_backup_directory_path = "../user_db_backup/"
if not os.path.exists(db_backup_directory_path):
    print("---MAKING NEW BACKUP DIRECTORY---")
    os.makedirs(db_backup_directory_path)
backup_parquets: list[str] = os.listdir(db_backup_directory_path)
backup_suffix_nums: list[int] = [int(pq_file.split("backup_")[1][0]) for pq_file in backup_parquets]
if backup_suffix_nums:
    max_backup_file_suffix = max(backup_suffix_nums) + 1
else:
    max_backup_file_suffix = 1
complete_df.to_parquet(f"../user_db_backup/database_backup_{max_backup_file_suffix}.parquet")

total_signups = len(complete_df)
df_previous = pd.read_csv("~/Desktop/dims_leads_previous.csv")

print(f"Previous csv save max id: {df_previous['id'].max()}")
print(f"total signups: {total_signups}")

new_df = complete_df.loc[complete_df['id'] > df_previous['id'].max()]
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