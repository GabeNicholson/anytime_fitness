import os 

def get_backup_file_suffix():
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
    return max_backup_file_suffix

