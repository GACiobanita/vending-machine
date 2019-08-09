import sqlite3
import os
import pandas as pd
from inspect import getsourcefile


class DatabaseArchitect(object):

    def __init__(self):
        self.db_connection = None
        self.db_cursor = None
        self.db_tables = []
        self.csv_files = []

        module_file_path = os.path.abspath(getsourcefile(lambda: 0))

        project_file_path = os.path.dirname(os.path.dirname(module_file_path))

        self.data_base_file_path = project_file_path + "\\database\\vendor_database.db"
        self.csv_file_path = project_file_path + "\\csv_files"

        self.connect_to_database()

    def create_db_connection(self):
        # create a database_functionality connection to a SQLite database_functionality
        try:
            self.db_connection = sqlite3.connect(self.data_base_file_path)
            print(sqlite3.version)
        except Exception as e:
            print(e)

    def create_db_cursor(self):
        self.db_cursor = self.db_connection.cursor()

    def add_data_to_table(self, table_name):
        table_columns = self.get_table_columns(table_name)
        input_values = []
        for column in table_columns:
            input_value = input('Enter value for column ' + str(column[1]) + ' of type ' + str(column[2]) + ': ')
            input_values.append(input_value)
        column_count = '?,' * len(table_columns)
        execution_string = 'INSERT INTO {} VALUES ('.format(table_name) + column_count[:-1] + ')'
        self.db_cursor.executemany(execution_string, (input_values,))

    def distribute_data_to_table(self, new_table_values, table_name):
        table_columns = self.get_table_columns(table_name)
        input_values = new_table_values
        column_count = '?,' * len(table_columns)
        execution_string = 'INSERT INTO {} VALUES ('.format(table_name) + column_count[:-1] + ')'
        self.db_cursor.executemany(execution_string, (input_values,))

    def update_table_data(self, table_name, column_name, id_column_name, id_column, new_value):
        table_string_first_half = 'UPDATE {} SET {}=?'.format(table_name, column_name)
        table_string_second_half = ' WHERE {}=?'.format(id_column_name)
        execution_string = table_string_first_half+table_string_second_half
        self.db_cursor.execute(execution_string, (new_value, id_column,))
        self.commit_changes_to_database()

    def get_tables_from_database(self):
        result = self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table_name in result:
            self.db_tables.append(table_name[0])

    def get_table_columns(self, table_name):
        execution_string = '''PRAGMA table_info({})'''.format(table_name)
        self.db_cursor.execute(execution_string)
        rows = self.db_cursor.fetchall()
        return rows

    def commit_changes_to_database(self):
        self.db_connection.commit()

    def commit_and_close_db(self):
        self.db_connection.commit()
        self.db_connection.close()

    def close_db(self):
        self.db_connection.close()

    def create_new_database(self):
        self.create_db_connection()

    def get_csv_files_from_path(self):
        file_names = os.listdir(self.csv_file_path)
        for file_name in file_names:
            if file_name.endswith(".csv"):
                self.csv_files.append(file_name)

    def csv_to_database_table(self):
        # in order to avoid rogue creation of databases
        # we want to control how databases are created through our code
        for csv_file_name in self.csv_files:
            df = pd.read_csv(self.csv_file_path + "\\" + csv_file_name)
            df.to_sql(csv_file_name[:-4], self.db_connection, if_exists='append', index=False)

    def get_data_base_data(self):
        df_list = {}
        for table in self.db_tables:
            df = pd.read_sql(sql='SELECT * FROM {}'.format(table), con=self.db_connection, index_col=None)
            df_list[table] = df
        return df_list

    def data_base_to_csv(self):
        for table in self.db_tables:
            df = pd.read_sql(sql='SELECT * FROM {}'.format(table), con=self.db_connection)
            df.to_csv(self.csv_file_path+'\\' + str(table) + ".csv", index=False)

    def connect_to_database(self):
        if os.path.isfile(self.data_base_file_path) is True:
            self.create_db_connection()
            self.create_db_cursor()
            self.get_tables_from_database()
            print("Successfully connect to existent data base.")
        else:
            print("Data base does not exist, creating new data base.\n")
            self.create_new_database()
            print("Data base created, uploading data from csv file.\n")
            self.get_csv_files_from_path()
            self.csv_to_database_table()
            print("New database created.\n")
            self.create_db_cursor()
            self.get_tables_from_database()
