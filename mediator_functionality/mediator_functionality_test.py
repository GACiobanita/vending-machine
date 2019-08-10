from .mediator import Mediator
import unittest


class MediatorTest(unittest.TestCase):

    def setUp(self):
        self.mediator = Mediator()

    def test_get_data_from_data_base_valid(self):
        self.mediator.get_data_from_data_base()
        self.assertNotEqual({}, self.mediator.entire_data_base)
        self.mediator.close_data_base()

    # data base is not created
    def test_get_data_from_data_base_invalid(self):
        self.mediator.data_base_architect = None
        self.mediator.get_data_from_data_base()
        self.assertNotEqual({}, self.mediator.entire_data_base)
        self.mediator.close_data_base()

    def test_create_item_and_cost_data_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.create_item_and_cost_data()
        self.assertNotEqual(0, len(self.mediator.item_data))
        self.mediator.close_data_base()

    # there is no data base data
    def test_create_item_and_cost_data_invalid(self):
        self.mediator.entire_data_base = {}
        self.mediator.create_item_and_cost_data()
        self.assertNotEqual(0, len(self.mediator.item_data))
        self.mediator.close_data_base()

    def test_get_item_valid(self):
        self.mediator.get_data_from_data_base()
        result = self.mediator.get_data_id('item_list', 'item_name', 'Peach Tea', 'item_id')
        self.assertEqual(2, result)

    # item name is not found in the db table
    def test_get_item_valid(self):
        self.mediator.get_data_from_data_base()
        result = self.mediator.get_data_id('item_list', 'item_name', 'does not exist', 'item_id')
        self.assertEqual(2, result)

    def test_update_item_list_stock_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.update_item_list_stock('Peach Tea', '6')
        self.mediator.data_base_architect.data_base_to_csv()

    # no data name is not in db
    def test_update_item_list_stock_invalid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.update_item_list_stock('', '')
        self.mediator.data_base_architect.data_base_to_csv()

    def test_create_funds_data_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.create_funds_data()
        self.assertNotEqual(0, len(self.mediator.fund_data))

    # no data base data
    def test_create_funds_data_invalid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.entire_data_base = {}
        self.mediator.create_funds_data()
        self.assertNotEqual(0, len(self.mediator.fund_data))

    def test_update_funds_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.update_funds('10', '10')
        self.mediator.data_base_architect.data_base_to_csv()

    def test_update_funds_invalid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.update_funds('', '')
        self.mediator.data_base_architect.data_base_to_csv()

    def test_get_data_id_valid(self):
        self.mediator.get_data_from_data_base()
        result = self.mediator.get_data_id('machine_funds', 'currency_name', '10p', 'currency_id')
        self.assertNotEqual('10', result)

    # no database data
    def test_get_data_id_invalid(self):
        result = self.mediator.get_data_id('machine_funds', 'currency_name', '10p', 'currency_id')
        self.assertNotEqual('10', result)

    def test_update_data_base_valid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.update_data_base('Peach Tea', '10', {'10p': 10})
        self.mediator.data_base_architect.data_base_to_csv()

    # no data
    def test_update_data_base_invalid(self):
        self.mediator.get_data_from_data_base()
        self.mediator.update_data_base('', '', {'': None})
        self.mediator.data_base_architect.data_base_to_csv()
