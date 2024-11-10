import sqlite3
from datetime import datetime

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect('ChatHistory.db')
        self.cursor = self.db.cursor()
        self.BackupDB = sqlite3.connect('Backup.db')
        self.BkDB = self.BackupDB.cursor()
    
    def CreateTable(self, tablename: str, columns: dict) -> None:
        if not tablename.isidentifier():
            print(f"Invalid table name: {tablename}")
            return
        
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tablename,))
        table_exists = self.cursor.fetchone() is not None
        self.BkDB.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tablename,))
        backup_exists = self.BkDB.fetchone() is not None

        if not table_exists and not backup_exists:
            columns_with_types = ', '.join([f"{col} {typ}" for col, typ in columns.items()])
            create_table_query = f"CREATE TABLE {tablename} ({columns_with_types});"

            try:
                self.cursor.execute(create_table_query)
                self.BkDB.execute(create_table_query)
                self.db.commit()
                self.BackupDB.commit()
                print(f"Table '{tablename}' created successfully.")
            except Exception as e:
                print(f"An error occurred while creating the table: {e}")
                self.db.rollback()
                self.BackupDB.rollback()
        else:
            print(f"Table '{tablename}' already exists.")

    def Insert(self, tablename: str, values: list[str]) -> bool:
        try:
            placeholders = ', '.join(['?'] * len(values))
            query = f"INSERT INTO {tablename} VALUES ({placeholders});"

            self.cursor.execute(query, values)
            self.BkDB.execute(query, values)
            self.db.commit()
            self.BackupDB.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def ClearHistory(self, tablename: str) -> None:        
        self.cursor.execute(f"DELETE FROM {tablename}")
        self.db.commit()
        print("History Deleted successfully")

    def DeleteHistory(self, tablename):
        print("Warning: This function will delete all data from the database.\n"
              "Are you sure you want to delete? (y/n): ", end='')

        choice = input().lower()
        while choice not in ['y', 'n']:
            choice = input("Invalid choice. Please enter 'y' for yes or 'n' for no: ").lower()

        if choice == 'y':
            try:
                columns = self.get_table_info(tablename)
                self.cursor.execute(f"DROP TABLE IF EXISTS {tablename};")
                self.BkDB.execute(f"DROP TABLE IF EXISTS {tablename};")
                print("All specified data has been deleted from the database.")
                self.db.commit()
                self.BackupDB.commit()

                # Get column info after deletion and recreate table
                if columns:
                    self.CreateTable(tablename, columns)

            except Exception as e:
                print(f"An error occurred while trying to delete the tables: {e}")
                self.db.rollback()
                self.BackupDB.rollback()
        elif choice == 'n':
            print("Deletion canceled by the user.")
    
    def get_table_info(self, tablename):
        if not tablename.isidentifier():
            print(f"Invalid table name: {tablename}")
            return
        
        try:
            self.cursor.execute(f"PRAGMA table_info({tablename})")
            cols = self.cursor.fetchall()  # Fetch all column info

            # Create a dictionary of columns
            columns = {col[1]: col[2] for col in cols}  # col[1] is the column name, col[2] is the type
            return columns
        except sqlite3.OperationalError as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.cursor.close()
        self.db.close()
        self.BkDB.close()
        self.BackupDB.close()

# for application purpose
def main():
    db = DataBase()

    table_name = 'ChatHistory'
    columns = {
        "command": "TEXT",
        "time": "DATETIME",
        "response": "TEXT",
        "errors": "TEXT",
        "status": "TEXT"
    }
    db.CreateTable(table_name, columns)


# for testing
if __name__ == '__main__':
    # db = DataBase()

    # table_name = 'ChatHistory'
    # columns = {
    #     "command": "TEXT",
    #     "time": "DATETIME",
    #     "response": "TEXT",
    #     "errors": "TEXT",
    #     "status": "TEXT"
    # }

    # # Uncomment to create the table if it doesn't exist
    # # db.CreateTable(table_name, columns)

    # test_data_1 = ['Increase brightness 10%', str(datetime.now()), 'Brightness increased', 'None', 'Offline']
    # test_data_2 = ['Increase volume 50%', str(datetime.now()), 'Volume increased', 'None', 'Offline']

    # # Uncomment to insert test data
    # # db.Insert(table_name, test_data_1)
    # # db.Insert(table_name, test_data_2)

    # # db.CreateTable(table_name, columns)
    # # db.DeleteHistory(table_name)

    # db.close()
    pass