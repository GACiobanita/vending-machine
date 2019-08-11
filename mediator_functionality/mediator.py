from database_functionality.database_architect import DatabaseArchitect


class Mediator(object):

    def __init__(self):
        self.data_base_architect = DatabaseArchitect()
        self.data_base_architect.connect_to_database("vendor_data_base.db")
        self.entire_data_base = self.get_data_from_data_base()
        self.item_data = self.create_item_and_cost_data()
        self.fund_data = self.create_funds_data()

    def get_data_from_data_base(self):
        return self.data_base_architect.get_data_base_data()

    def create_item_and_cost_data(self):
        item_data = {}
        # iterate through the 'item_list' table of the database
        for row in self.entire_data_base['item_list'].iterrows():
            int_value = self.transform_currency_to_int(row[1]['item_cost'])
            if int_value != 0:
                item_data[row[1]['item_name']] = (row[1]['item_cost'], int_value, row[1]['item_amount'])
            else:
                print("item_list table contains data that cannot be formatted to numbers in the item_cost column.")
        return item_data

    def get_item_data(self):
        return self.item_data

    def create_funds_data(self):
        fund_data = {}
        # iterate through the 'machine_funds' table of the database
        for row in self.entire_data_base['machine_funds'].iterrows():
            int_value = self.transform_currency_to_int(row[1]['currency_name'])
            fund_data[row[1]['currency_name']] = (int(row[1]['amount_available']), int_value)
        return fund_data

    def get_fund_data(self):
        return self.fund_data

    @staticmethod
    # we convert Text data from the column, which is a string now, to a float followed by int
    # we also convert pounds to their amount in pence
    def transform_currency_to_int(string_money):
        if '£' in string_money:
            string_money = string_money[1:]
            try:
                float_conversion = float(string_money)
                float_conversion *= 100
                int_conversion = int(float_conversion)
                return int_conversion
            except ValueError:
                pass
        elif 'p' in string_money:
            try:
                string_money = string_money[:-1]
                int_conversion = int(string_money)
                return int_conversion
            except ValueError:
                pass

    # once a purchase is confirmed update the amount of currency available as change and the item quantity left in the
    # vending machine
    def update_data_base(self, item_name, stock_value, currency_available):
        item_id = str(self.get_data_id('item_list', 'item_name', item_name, 'item_id'))
        self.update_item_list_stock(stock_value, item_id)
        for key, value in currency_available.items():
            currency_id = str(self.get_data_id('machine_funds', 'currency_name', key, 'currency_id'))
            self.update_funds(currency_id, value)
        self.data_base_architect.data_base_to_csv()

    # specify the table(item list) in which to update the column(item amount), by what to find
    # the current item (item_id) , then the data itself, item_id and stock_value
    def update_item_list_stock(self, stock_value, item_id):
        self.data_base_architect.update_table_data('item_list', 'item_amount', 'item_id',
                                                   item_id, stock_value)

    # same as above
    def update_funds(self, currency_id, new_amount):
        self.data_base_architect.update_table_data('machine_funds', 'amount_available', 'currency_id',
                                                   currency_id, new_amount)

    # get id from table where column_name is equal to item name
    def get_data_id(self, table_name, column_name, item_name, required_id):
        data_frame = self.entire_data_base[table_name]
        result = data_frame[data_frame[column_name] == item_name][required_id]
        return result.item()

    def close_data_base(self):
        self.data_base_architect.close_db()

    def commit_changes_to_data_base(self):
        self.data_base_architect.commit_changes_to_database()

    def commit_changes_and_close_data_base(self):
        self.data_base_architect.commit_and_close_db()

    def request_data_base_reset(self):
        self.data_base_architect.reset_data_base()
        # mediator also needs to be reset to the new data
        self.item_data = {}
        self.fund_data = {}
        self.entire_data_base = None
        # then get the new database data on reset
        self.entire_data_base = self.get_data_from_data_base()
        self.item_data = self.create_item_and_cost_data()
        self.fund_data = self.create_funds_data()
