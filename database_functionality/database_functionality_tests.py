from .database_architect import DatabaseArchitect
import unittest


class TestDatabaseFunctionality(unittest.TestCase):

    def setUp(self):
        self.database_architect = DatabaseArchitect()

    def test_create_db_connection_valid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        self.assertNotEqual(None, self.database_architect.db_connection)
        self.database_architect.close_db()

    # missing db from file path
    def test_create_db_connection_invalid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\"
        self.database_architect.create_db_connection()
        self.assertNotEqual(None, self.database_architect.db_connection)
        self.database_architect.commit_and_close_db()

    def test_create_db_cursor_valid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        self.database_architect.create_db_cursor()
        self.assertNotEqual(None, self.database_architect.db_cursor)
        self.database_architect.close_db()

    # can't create a cursor without a connection to a db
    def test_create_db_cursor_invalid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\"
        self.database_architect.create_db_connection()
        self.database_architect.create_db_cursor()
        self.assertNotEqual(None, self.database_architect.db_cursor)
        self.database_architect.close_db()

    def test_get_csv_files_from_path(self):
        self.database_architect.get_csv_files_from_path(self.database_architect.csv_file_path)
        self.assertNotEqual(0, len(self.database_architect.csv_files))

    # no csv files in path
    def test_get_csv_files_from_path(self):
        self.database_architect.csv_file_path = "D:\\"
        self.database_architect.get_csv_files_from_path(self.database_architect.csv_file_path)
        self.assertNotEqual(0, len(self.database_architect.csv_files))

    def test_csv_to_database_table_valid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        self.database_architect.csv_to_database_table()
        self.database_architect.create_db_cursor()
        self.database_architect.get_tables_from_database()
        self.assertNotEqual(0, len(self.database_architect.db_tables))

    # no csv files in path
    def test_csv_to_database_table_invalid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.data_base_file_path = "D:\\"
        self.database_architect.create_db_connection()
        self.database_architect.csv_to_database_table()
        self.database_architect.create_db_cursor()
        self.database_architect.get_tables_from_database()
        self.assertNotEqual(0, len(self.database_architect.db_tables))

    def test_get_tables_from_database_valid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        self.database_architect.create_db_cursor()
        self.database_architect.get_tables_from_database()
        self.assertNotEqual(0, len(self.database_architect.db_tables))
        self.database_architect.close_db()

    # database has no tables
    def test_get_tables_from_database_invalid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        self.database_architect.create_db_cursor()
        self.database_architect.get_tables_from_database()
        self.assertNotEqual(0, len(self.database_architect.db_tables))
        self.database_architect.close_db()

    def test_get_table_columns_valid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        self.database_architect.create_db_cursor()
        result = self.database_architect.get_table_columns()
        self.assertNotEqual(0, len(result))
        self.database_architect.close_db()

    # database has no tables
    # delete database before test
    def test_get_table_columns_invalid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        self.database_architect.create_db_cursor()
        result = self.database_architect.get_table_columns()
        self.assertNotEqual(0, len(result))
        self.database_architect.close_db()

    def test_add_data_to_table_valid(self):
        self.database_architect.connect_to_database('test_db.db')
        self.database_architect.add_data_to_table('item_list')
        self.database_architect.data_base_to_csv()
        self.database_architect.commit_and_close_db()

    # non existent table name
    # delete database before test
    def test_add_data_to_table_invalid(self):
        self.database_architect.connect_to_database('test_db.db')
        self.database_architect.add_data_to_table('non_existent')
        self.database_architect.data_base_to_csv()
        self.database_architect.commit_and_close_db()

    def test_update_table_data_valid(self):
        self.database_architect.connect_to_database('test_db.db')
        self.database_architect.update_table_data('machine_funds', 'amount_available', 'currency_id', '10', 10)
        self.database_architect.data_base_to_csv()
        self.database_architect.commit_and_close_db()

    # column name is incorrect
    def test_update_table_data_invalid(self):
        self.database_architect.connect_to_database('test_db.db')
        self.database_architect.update_table_data('machine_funds', 'amount_', 'currency_id', '10', 10)
        self.database_architect.data_base_to_csv()
        self.database_architect.commit_and_close_db()

    def test_get_data_base_data_valid(self):
        self.database_architect.connect_to_database('test_db.db')
        result = self.database_architect.get_data_base_data()
        self.assertNotEqual({}, result)

    # data base has no tables
    # delete database before test
    def test_get_data_base_data_invalid(self):
        self.database_architect.data_base_file_path = "D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db"
        self.database_architect.create_db_connection()
        result = self.database_architect.get_data_base_data()
        self.assertNotEqual({}, result)

    def test_reset_data_base(self):
        self.database_architect.connect_to_database('vendor_data_base.db')
        self.database_architect.reset_data_base()
        self.assertNotEqual(0, len(self.database_architect.csv_files))
        self.assertNotEqual(0, len(self.database_architect.db_tables))


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
