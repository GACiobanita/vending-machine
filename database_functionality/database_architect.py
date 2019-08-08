import sqlite3
import os
import pandas as pd
from inspect import getsourcefile


class DatabaseArchitect(object):

    def __init__(self):
        self.db_connection = None
        self.db_cursor = None
        self.current_table = None
        self.current_database = None

    def create_db_connection(self, db_file):
        # create a database_functionality connection to a SQLite database_functionality
        try:
            self.db_connection = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Exception as e:
            print(e)

    def create_db_cursor(self):
        self.db_cursor = self.db_connection.cursor()

    def create_table(self, table_name):
        execution_string = '''CREATE TABLE {} (Item_ID text NOT NULL)'''.format(table_name)
        self.db_cursor.execute(execution_string)

    def drop_table(self, table_name):
        execution_string = '''DROP TABLE {}'''.format(table_name)
        self.db_cursor.execute(execution_string)

    def add_table_column_with_basic_type(self, table_name, column_name, column_type):
        self.db_cursor.execute('''ALTER TABLE {} ADD COLUMN {} {}'''.format(table_name, column_name, column_type))

    def add_data_to_table(self, table_name):
        table_columns = self.get_table_columns(table_name)
        input_values = []
        for column in table_columns:
            input_value = input('Enter value for column ' + str(column[1]) + ' of type ' + str(column[2]) + ': ')
            input_values.append(input_value)
        column_count = '?,' * len(table_columns)
        execution_string = 'INSERT INTO {} VALUES ('.format(table_name) + column_count[:-1] + ')'
        self.db_cursor.executemany(execution_string, (input_values,))

    def get_table_from_db(self):
        result = self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table_name in result:
            print(table_name[0])

    def get_table_columns(self, table_name):
        execution_string = '''PRAGMA table_info({})'''.format(table_name)
        self.db_cursor.execute(execution_string)
        rows = self.db_cursor.fetchall()
        return rows

    def commit_changes_to_db(self):
        self.db_connection.commit()

    def commit_and_close_db(self):
        self.db_connection.commit()
        self.db_connection.close()

    def close_db(self):
        self.db_connection.close()

    def csv_to_db(self, data_base_name, csv_table_name, item_list='item_list.csv'):
        module_file_path = os.path.abspath(getsourcefile(lambda: 0))
        csv_file_path = os.path.join(os.path.dirname(module_file_path), item_list)
        db_file_path = os.path.dirname(os.path.dirname(module_file_path)) + "\\database\\" + data_base_name
        print(db_file_path)
        self.create_db_connection()

        df = pd.read_csv(csv_file_path)
        df.to_sql("test_csv_table", self.db_connection, if_exists='append', index=False)
