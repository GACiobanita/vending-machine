from mediator_functionality.mediator import Mediator
import re

REGEX = re.compile('[a-zA-Z@_!#$%^&*()<>?/\\\\|}{~:]')
EXAMPLE_STRING = '[£2 £1 50p 20p 10p 5p 2p 1p]'

# a container for the database data taken from the mediator
class VendorItem(object):
    def __init__(self, item_name, item_display_price, item_int_price, items_available):
        self.item_name = str(item_name)
        self.items_available = int(items_available)
        self.item_display_price = str(item_display_price)
        self.item_int_price = int(item_int_price)

    def __str__(self):
        return str(self.item_name) + " available for: " + str(self.item_display_price) + ".\n"


# each CurrencyCount item is equal to a single coin value
class CurrencyCount(object):
    def __init__(self, currency_name, currency_int_value, currency_available):
        self.currency_name = str(currency_name)
        self.currency_available = int(currency_available)
        self.currency_int_value = int(currency_int_value)

    def __str__(self):
        return str(self.currency_available) + ' coins of ' + self.currency_name + ' value available.\n'

    def get_sum_of_coins(self):
        return self.currency_available * self.currency_int_value


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
        # un pack the values given by the mediator then create {option : vendor item} pairs
        # option will be used to select items
        for item_name, (display_price, int_price, availability) in self.items_information.items():
            if availability > 0:
                items_list[option_count] = VendorItem(item_name, display_price, int_price, availability)
                option_count += 1
        return items_list

    def create_change_list(self):
        available_change = {}
        change_to_give = {}
        change_inserted = {}
        # un pack the values given by the mediator then create all the change holding structures of the project
        for currency_name, (amount_available, int_value) in sorted(list(self.funds_information.items()),
                                                                   key=lambda x: x[1][1],
                                                                   reverse=True):
            available_change[currency_name] = CurrencyCount(currency_name, int_value, amount_available)
            change_to_give[currency_name] = CurrencyCount(currency_name, int_value, 0)
            change_inserted[currency_name] = CurrencyCount(currency_name, int_value, 0)
        return available_change, change_to_give, change_inserted

    # reset the inserted change is a way of showing that a refund was given
    def reset_inserted_change(self):
        for currency_name, (amount_available, int_value) in sorted(list(self.funds_information.items()),
                                                                   key=lambda x: x[1][1],
                                                                   reverse=True):
            self.change_inserted[currency_name] = CurrencyCount(currency_name, int_value, 0)

    # displaying items preceded by their option value
    def display_available_items(self):
        for select_option, item in self.items_list.items():
            print('[' + str(select_option) + '] ' + str(item))

    def item_purchase_process(self):
        # display purchase options
        self.display_available_items()
        # handle purchase input
        selected_option, selected_item = self.input_number_for_item_selection()
        # handle what quantity will be bought, also verifies if enough items are available
        item_quantity = self.input_item_quantity(selected_item.items_available)
        item_cost = self.calculate_item_cost(selected_item.item_int_price, item_quantity)
        confirmed_payment = False
        print('Your total amounts to: ' + '£' + str(item_cost / 100))
        while confirmed_payment is False:
            # handle change being inserted
            inserted_change = self.insert_change()
            self.create_change_inserted_dict(inserted_change)
            # calculate the sum that was inserted
            inserted_sum = self.calculate_currency_sum(self.change_inserted)
            # verify if enough change was inserted else the process starts again
            confirmed_payment = self.verify_inserted_change(item_cost, inserted_sum)
        # if there are enough funds in the machine to give change back, the purchase is confirmed and data is update
        # in the data base
        purchase_confirmation = self.calculate_change_amount(inserted_sum - item_cost)
        if purchase_confirmation is True:
            self.confirm_purchase_in_data_base(int(selected_option), selected_item, item_quantity)

    def close_vending_machine(self):
        print('Shutting down.')
        self.mediator.close_data_base()

    def input_number_for_item_selection(self):
        selected_item = None
        print('Input the number shown before the item, without [] to select an item.\n')
        while selected_item is None:
            try:
                selection = input('Which item would you like to purchase?\n ')
                selected_item = self.items_list[int(selection)]
            except KeyError:
                print('There is no such option available, try using a valid option.')
                pass
        return selection, selected_item

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
    def calculate_item_cost(selected_item_value, quantity):
        return selected_item_value * quantity

    def calculate_change_amount(self, payment_difference):
        for currency_name, currency_item in self.change_to_give_back.items():
            # verify if there are any coins of this type to give as change
            available_coin_amount = self.available_change[currency_name].currency_available
            if available_coin_amount > 0:
                # calculate the amount of coins of this type needed to reach the payment_amount number
                number_of_coins = payment_difference // currency_item.currency_int_value
                # if the available amount of coins is not 0 but is still not enough to reach the sum
                if number_of_coins > available_coin_amount:
                    self.change_to_give_back[currency_name].currency_available = available_coin_amount
                else:
                    # there are enough coins to reach the sum
                    self.change_to_give_back[currency_name].currency_available = number_of_coins
                # reduce payment amount to calculate for the next type of coin
                payment_difference -= currency_item.currency_int_value * self.change_to_give_back[
                    currency_name].currency_available
        if payment_difference > 0:
            # if we reach this point then this means we don't have enough coins to give change back
            print('Vending machine does not have enough change, money refunded.')
            # remove the inserted coins that were used as available change
            self.remove_inserted_currency_from_available_currency()
            return False
        else:
            # we successfully created a list of coins to give back as change
            for currency_name, currency_item in self.available_change.items():
                self.available_change[currency_name].currency_available -= self.change_to_give_back[
                    currency_name].currency_available
            self.give_change_to_customer()
            return True

    # pass data to mediator for updates
    def confirm_purchase_in_data_base(self, selected_option, purchased_item, item_quantity):
        currency_data = {}
        remaining_stock = purchased_item.items_available - item_quantity
        for currency_name, currency_item in self.available_change.items():
            currency_data[currency_name] = currency_item.currency_available
        self.mediator.update_data_base(purchased_item.item_name, remaining_stock, currency_data)
        if remaining_stock == 0:
            del self.items_list[selected_option]
        else:
            self.items_list[selected_option].items_available = remaining_stock

    def insert_change(self):
        change_string = None
        print('You can insert the following coins in the machine.\n')
        print(EXAMPLE_STRING + '\n')
        print('Insert coins in the following way:[1 1 0 0 1 1 0 0].\n')
        print('Each number represents the amount of coins of that type to be inserted.\n')
        print('The above example would be equal to £3.15.')
        print(EXAMPLE_STRING + '\n')
        input_string = input('Now please input the amount you would like to insert\n')
        change_list = self.input_string_verification(input_string)
        return change_list

    def verify_inserted_change(self, item_cost, inserted_change):
        if inserted_change < item_cost:
            self.reset_inserted_change()
            print('Insufficient funds inserted.')
            return False
        return True

    def create_change_inserted_dict(self, change_list):
        count = 0
        for currency_name, currency_item in self.change_inserted.items():
            self.change_inserted[currency_name].currency_available = int(change_list[count])
            count += 1

    # so we can use inserted coins to give change back
    def add_inserted_currency_to_available_currency(self):
        for currency_name, currency_item in self.available_change.items():
            self.available_change[currency_name].currency_available += self.change_inserted[
                currency_name].currency_available

    # in case of a refund we remove the change inserted, which we we're using as currency for giving back change
    # this is specific for cases where the user give too much change and we have to give it back
    # despite change missing from the database
    def remove_inserted_currency_from_available_currency(self):
        for currency_name, currency_item in self.available_change.items():
            self.available_change[currency_name].currency_available -= self.change_inserted[
                currency_name].currency_available

    def give_change_to_customer(self):
        output_string = 'Your change is: '
        for currency_name, currency_item in self.change_to_give_back.items():
            if self.change_to_give_back[currency_name].currency_available is not 0:
                output_string += str(currency_item.currency_available) + ' ' + str(currency_name) + ', '
        output_string = output_string[:-2]
        print(output_string)

    @staticmethod
    def calculate_currency_sum(change_inserted):
        currency_sum = 0
        for currency_name, currency_data in change_inserted.items():
            currency_sum += currency_data.currency_available * currency_data.currency_int_value
        return currency_sum

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
        string_list = [int(string_element) for string_element in string_list]
        return string_list

    def request_mediator_to_reset_data_base(self):
        self.mediator.request_data_base_reset()
        # vending machine data also needs to be reset with new data from the mediator
        self.funds_information = {}
        self.items_information = {}
        self.items_list = {}
        self.available_change = None
        self.change_to_give_back = None
        self.change_inserted = None
        # get new data
        self.funds_information = self.mediator.get_fund_data()
        self.items_information = self.mediator.get_item_data()
        self.items_list = self.create_items_list()
        self.available_change, self.change_to_give_back, self.change_inserted = self.create_change_list()
