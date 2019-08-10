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
        available_change, change_to_give = self.vending_machine.create_change_list()
        self.assertNotEqual(0, len(available_change))
        self.assertNotEqual(0, len(change_to_give))

    # incorrect data
    def test_create_change_list_invalid(self):
        self.vending_machine.funds_information = {10: 10}
        available_change, change_to_give = self.vending_machine.create_change_list()
        self.assertNotEqual(0, len(available_change))
        self.assertNotEqual(0, len(change_to_give))

    def test_calculate_change_amount_valid_change_given(self):
        self.vending_machine.calculate_change_amount(159) # or 1.59 GBP

    def test_calculate_change_amount_valid_not_enough_change(self):
        self.vending_machine.calculate_change_amount(10000)  # or 100 GBP

    def test_input_string_verification_valid(self):
        self.vending_machine.input_string_verification("this is a string")

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
