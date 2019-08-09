from .mediator import Mediator
from database_functionality.database_architect import DatabaseArchitect
import unittest


class MediatorTest(unittest.TestCase):

    def setUp(self):
        self.data_base_architect = DatabaseArchitect()
        self.mediator = Mediator()
        self.mediator.get_data_base(self.data_base_architect)

    def test_get_data_from_data_base_valid(self):
        self.mediator.get_data_from_data_base()

    def test_create_item_and_cost_list_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.create_item_and_cost_list()
        print(self.mediator.item_data)

    def test_get_item_valid(self):
        self.mediator.get_data_from_data_base()
        result = self.mediator.get_data_id('Peach Tea')
        self.data_base_architect.close_db()
        print(result)

    def test_update_item_list_stock_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.update_item_list_stock('Peach Tea', '6')
        self.data_base_architect.data_base_to_csv()
        self.data_base_architect.close_db()

    def test_create_funds_list_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.create_funds_list()
        print(self.mediator.fund_data)
        self.data_base_architect.close_db()

    def test_update_funds_valid(self):
        dispensed_amount = {'10p': 1, '20p': 0}
        self.mediator.get_data_from_data_base()
        self.mediator.create_funds_list()
        self.mediator.update_funds(dispensed_amount)
        self.data_base_architect.data_base_to_csv()
        self.data_base_architect.close_db()

    def test_get_data_id_valid(self):
        self.mediator.get_data_from_data_base()
        result = self.mediator.get_data_id('machine_funds', 'currency_name', '10p', 'currency_id')
        print(result)
