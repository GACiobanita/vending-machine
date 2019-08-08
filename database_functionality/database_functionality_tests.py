from .database_architect import DatabaseArchitect
import unittest


class TestDatabaseFunctionality(unittest.TestCase):

    def setUp(self):
        self.database_architect = DatabaseArchitect(
            'D:\\Python\\vending-machine\\vending-machine\\database\\test_db.db')

    def test_create_table_valid(self):
        self.database_architect.create_table("test_table_name")
        self.database_architect.commit_and_close_db()
        self.assertNotEqual(None, self.database_architect.db_connection)

    def test_get_table_name_valid(self):
        self.database_architect.get_table_from_db()
        self.database_architect.close_db()
        self.assertNotEqual(None, self.database_architect.db_connection)

    def test_delete_table_valid(self):
        self.database_architect.drop_table("test_table_name")
        self.database_architect.commit_and_close_db()
        self.assertNotEqual(None, self.database_architect.db_connection)

    def test_create_table_column_with_basic_type(self):
        self.database_architect.add_table_column_with_basic_type("test_table_name", "Item_Price", "text")
        self.database_architect.commit_and_close_db()

    def test_get_table_columns(self):
        self.database_architect.get_table_columns("test_table_name")
        self.database_architect.close_db()

    def test_add_data_to_table(self):
        self.database_architect.add_data_to_table("test_table_name")
        self.database_architect.close_db()

    def test_csv_to_db(self):
        self.database_architect.csv_to_db('test_csv_to_db.db', "csv_table")
        self.database_architect.close_db()

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
