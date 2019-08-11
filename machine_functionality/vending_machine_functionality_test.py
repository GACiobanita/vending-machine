from .vending_machine import VendingMachine
import unittest


class VendingMachineTest(unittest.TestCase):

    def setUp(self):
        self.vending_machine = VendingMachine()

    def test_display_available_items_valid(self):
        self.vending_machine.display_available_items()

    def test_input_number_for_item_selection_valid(self):
        self.vending_machine.input_number_for_item_selection()

    # input letter or number outside of the values displayed
    def test_input_number_for_item_selection_invalid(self):
        self.vending_machine.input_number_for_item_selection()

    def test_input_item_quantity_valid(self):
        self.vending_machine.input_item_quantity(10)

    def test_create_change_list_valid(self):
        available_change, change_to_give, change_inserted = self.vending_machine.create_change_list()
        self.assertNotEqual(0, len(available_change))
        self.assertNotEqual(0, len(change_to_give))
        self.assertNotEqual(0, len(change_inserted))

    # incorrect data
    def test_create_change_list_invalid(self):
        self.vending_machine.funds_information = {10: 10}
        available_change, change_to_give, change_inserted = self.vending_machine.create_change_list()
        self.assertNotEqual(0, len(available_change))
        self.assertNotEqual(0, len(change_to_give))

    def test_calculate_change_amount_valid_change_given(self):
        self.vending_machine.calculate_change_amount(159)  # or 1.59 GBP

    def test_calculate_change_amount_valid_not_enough_change(self):
        self.vending_machine.calculate_change_amount(10000)  # or 100 GBP

    def test_input_string_verification_valid_value(self):
        self.vending_machine.input_string_verification("2 0 1 2 0 0 0 0")

    def test_input_string_verification_invalid_value(self):
        self.vending_machine.input_string_verification("this is an invalid value")

    def test_insert_change_valid(self):
        result = self.vending_machine.insert_change()
        self.assertNotEqual(None, result)

    # invalid characters
    def test_insert_change_invalid(self):
        print('Input any letter that is not part of the English language into the change string.')
        result = self.vending_machine.insert_change()
        self.assertNotEqual(None, result)

    def test_calculate_currency_sum_valid(self):
        result = self.vending_machine.calculate_currency_sum(self.vending_machine.available_change)
        self.assertNotEqual(0, result)

    # invalid data passed
    def test_calculate_currency_sum_invalid(self):
        result = self.vending_machine.calculate_currency_sum(self.vending_machine)
        self.assertNotEqual(0, result)

    def test_verify_inserted_change_valid_true_result(self):
        result = self.vending_machine.verify_inserted_change(200, (1, 1, 1, 1, 0, 0, 0, 0))
        self.assertNotEqual(False, result)

    def test_verify_inserted_change_valid_false_result(self):
        result = self.vending_machine.verify_inserted_change(200, (0, 0, 1, 1, 0, 0, 0, 0))
        self.assertNotEqual(False, result)

    def test_add_inserted_currency_to_available_currency_valid(self):
        self.vending_machine.verify_inserted_change(200, (1, 1, 1, 1, 0, 0, 0, 0))
        self.vending_machine.available_change['£2'].currency_available = 10
        self.vending_machine.add_inserted_currency_to_available_currency()
        changed_currency = self.vending_machine.available_change['£2']
        self.assertEqual(11, self.vending_machine.available_change['£2'].currency_available)

    def test_add_inserted_currency_to_available_currency_invalid_not_enough_currency(self):
        self.vending_machine.verify_inserted_change(500, (1, 1, 1, 1, 0, 0, 0, 0))
        self.vending_machine.available_change['£2'].currency_available = 10
        self.vending_machine.add_inserted_currency_to_available_currency()
        changed_currency = self.vending_machine.available_change['£2']
        self.assertNotEqual(10, changed_currency.currency_available)

    def test_inserted_currency_from_available_currency_valid(self):
        self.vending_machine.verify_inserted_change(200, (1, 1, 1, 1, 0, 0, 0, 0))
        self.vending_machine.available_change['£2'].currency_available = 10
        self.vending_machine.remove_inserted_currency_from_available_currency()
        changed_currency = self.vending_machine.available_change['£2']
        self.assertEqual(9, changed_currency.currency_available)

    def test_inserted_currency_from_available_currency_invalid_not_enough_currency(self):
        self.vending_machine.verify_inserted_change(500, (1, 1, 1, 1, 0, 0, 0, 0))
        self.vending_machine.available_change['£2'].currency_available = 10
        self.vending_machine.remove_inserted_currency_from_available_currency()
        changed_currency = self.vending_machine.available_change['£2']
        self.assertEqual(9, changed_currency.currency_available)

    def test_close_db(self):
        self.vending_machine.close_vending_machine()

    def test_item_purchase_process(self):
        self.vending_machine.item_purchase_process()

    def test_request_mediator_to_reset_data_base(self):
        self.vending_machine.request_mediator_to_reset_data_base()
        self.assertNotEqual(0, len(self.vending_machine.funds_information))
        self.assertNotEqual(0, len(self.vending_machine.items_information))
        self.assertNotEqual(0, len(self.vending_machine.items_list))
        self.assertNotEqual(0, len(self.vending_machine.available_change))
        self.assertNotEqual(0, len(self.vending_machine.change_inserted))
        self.assertNotEqual(0, len(self.vending_machine.change_to_give_back))


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
