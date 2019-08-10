from mediator_functionality.mediator import Mediator
import re

REGEX = re.compile('[a-zA-Z@_!#$%^&*()<>?/\\\\|}{~:]')

class VendorItem(object):
    def __init__(self, item_name, item_display_price, item_int_price, items_available):
        self.item_name = item_name
        self.items_available = items_available
        self.item_display_price = item_display_price
        self.item_int_price = item_int_price

    def __str__(self):
        return str(self.item_name) + " available for: " + str(self.item_display_price) + ".\n"


class CurrencyCount(object):
    def __init__(self, currency_name, currency_int_value, currency_available):
        self.currency_name = currency_name
        self.currency_available = currency_available
        self.currency_int_value = currency_int_value

    def __str__(self):
        return str(self.currency_available) + ' coins of ' + str(self.currency_name) + ' value available.\n'


class VendingMachine(object):
    def __init__(self):
        self.mediator = Mediator()
        self.funds_information = self.mediator.get_fund_data()
        self.items_information = self.mediator.get_item_data()
        self.items_list = self.create_items_list()
        self.available_change, self.change_to_give_back, self.change_inserted = self.create_change_list()

    def create_items_list(self):
        items_list = {}
        option_count = 1
        for item_name, (display_price, int_price, availability) in self.items_information.items():
            items_list[option_count] = VendorItem(item_name, display_price, int_price, availability)
            option_count += 1
        return items_list

    def create_change_list(self):
        available_change = {}
        change_to_give = {}
        change_inserted = {}
        for currency_name, (amount_available, int_value) in self.funds_information.items():
            available_change[currency_name] = CurrencyCount(currency_name, int_value, amount_available)
            change_to_give[currency_name] = CurrencyCount(currency_name, int_value, 0)
            change_inserted[currency_name] = CurrencyCount(currency_name, int_value, 0)
        return available_change, change_to_give, change_inserted

    def display_available_items(self):
        for select_option, item in self.items_list.items():
            print('[' + str(select_option) + '] ' + str(item))

    def input_number_for_item_selection(self):
        selected_item = None
        print('Input the number shown before the item, without [] to select an item.\n')
        while selected_item is None:
            try:
                selection = input('Which item would you like to purchase?\n ')
                selected_item = self.items_list[selection]
            except KeyError:
                print('There is no such option available, try using a valid option.')
                pass
        return selected_item

    @staticmethod
    def input_item_quantity(available_quantity):
        print('Only ' + str(available_quantity) + ' of the selected item in stock.')
        quantity = None
        while quantity is None:
            try:
                selection = input("Input item quantity you would like to purchase: \n ")
                quantity = int(selection)
                if quantity > available_quantity:
                    print(
                        "Quantity unavailable, try less, only " + str(available_quantity) + ' available for purchase.')
                    quantity = None
            except ValueError:
                print('That is not valid item quantity, try a valid number.')
                pass
        return quantity

    @staticmethod
    def calculate_payment_amount(selected_item_value, quantity):
        return selected_item_value * quantity

    def calculate_change_amount(self, payment_amount):
        # go from the largest amount of currency to the smallest amount of currency 2 GBP to 1 pence
        for currency_name, currency_item in sorted(list(self.change_to_give_back.items()),
                                                   key=lambda x: x[1].currency_int_value,
                                                   reverse=True):
            # verify if there are any coins of this type to give as change
            available_coin_amount = self.available_change[currency_name].currency_available
            if available_coin_amount > 0:
                # calculate the amount of coins of this type needed to reach the payment_amount number
                number_of_coins = payment_amount // currency_item.currency_int_value
                # if the available amount of coins is not 0 but is still not enough to reach the sum
                if number_of_coins > available_coin_amount:
                    self.change_to_give_back[currency_name].currency_available = available_coin_amount
                else:
                    # there are enough coins to reach the sum
                    self.change_to_give_back[currency_name].currency_available = number_of_coins
                payment_amount -= currency_item.currency_int_value * self.change_to_give_back[
                    currency_name].currency_available
            # reduce payment amount to calculate for the next type of coin
        # if we reach this point then this means we don't have enough coins to give change back
        if payment_amount > 0:
            print(' There is not enough change, money refunded.')
        else:
            for currency_name, currency_item in self.available_change.items():
                self.available_change[currency_name].currency_available -= self.change_to_give_back[
                    currency_name].currency_available
                print(self.change_to_give_back[currency_name])

    def insert_change(self, payment_amount):
        example_string = '[£2 £1 50p 20p 10p 5p 2p 1p]'
        print('You can insert the following coins in the machine.\n')
        print(example_string + '\n')
        print(
            'Insert coins in the following way:[1 1 0 0 1 1 0 0], where each number represents the amount of coins of that type to be inserted.\n')
        print('The above would be equal to £3.15.')
        print(example_string + '\n')
        input_string = input('Now please input the amount you would like to insert\n')
        string_list = self.input_string_verification(input_string)
        count = 0
        for currency_name, currency_item in self.change_inserted.items():
            self.change_inserted[currency_name].currency_available = string_list[count]

    # so we can use inserted coins to give change back
    def add_inserted_currency_to_available_currency(self):
        for currency_name, currency_item in self.available_change.items():
            self.available_change[currency_name].currency_available += self.change_inserted[
                currency_name].currency_available

    # in case of a refund
    def remove_inserted_currency_from_available_currency(self):
        for currency_name, currency_item in self.available_change.items():
            self.available_change[currency_name].currency_available -= self.change_inserted[
                currency_name].currency_available

    @staticmethod
    # verify if the string contains any letters of symbols
    # string also needs to follow the example, meaning it needs to have a length of 15 but also split into a
    # list of length 8
    def input_string_verification(input_string):
        string_list = input_string.split(' ')
        while len(input_string) is not 15 or REGEX.search(input_string) is not None or len(
                string_list) is not 8:
            print('Input string was not correct, try again.\n')
            print('[£2 £1 50p 20p 10p 5p 2p 1p]\n')
            input_string = input('Now please input the amount you would like to insert.\n')
            string_list = input_string.split(' ')

            print(len(input_string))
            print(REGEX.search(input_string))
            print(len(string_list))
        return string_list
