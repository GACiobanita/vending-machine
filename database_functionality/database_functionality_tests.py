from .database_architect import DatabaseArchitect
import unittest


class TestDatabaseFunctionality(unittest.TestCase):

    def setUp(self):
        self.database_architect = DatabaseArchitect()

    def test_get_data_base_table_valid(self):
        self.database_architect.get_data_base_data()


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
