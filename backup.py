import shutil

def backup_db():
    shutil.copy("finance.db", "finance_backup.db")
    print("✅ Backup created")

def restore_db():
    shutil.copy("finance_backup.db", "finance.db")
    print("✅ Database restored")
