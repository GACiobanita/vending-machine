from .database_architect import DatabaseArchitect
import unittest


class TestDatabaseFunctionality(unittest.TestCase):

    def setUp(self):
        self.database_architect = DatabaseArchitect()

    def test_get_data_base_table_valid(self):
        result = self.database_architect.get_data_base_data()
        print(result)

    def test_update_table_data_valid(self):
        self.database_architect.update_table_data('item_list', 'item_amount', 'item_id', '2', 9)
        self.database_architect.data_base_to_csv()
        self.database_architect.close_db()


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
