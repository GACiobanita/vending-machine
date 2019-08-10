from database_functionality.database_architect import DatabaseArchitect


class Mediator(object):

    def __init__(self):
        self.data_base_architect = DatabaseArchitect()
        self.data_base_architect.connect_to_database("vendor_database.db")
        self.entire_data_base = self.get_data_from_data_base()
        self.item_data = self.create_item_and_cost_data()
        self.fund_data = self.create_funds_data()

    def get_data_from_data_base(self):
        return self.data_base_architect.get_data_base_data()

    def create_item_and_cost_data(self):
        item_data = {}
        for row in self.entire_data_base['item_list'].iterrows():
            int_value = 0
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
        for row in self.entire_data_base['machine_funds'].iterrows():
            int_value = self.transform_currency_to_int(row[1]['currency_name'])
            fund_data[row[1]['currency_name']] = (row[1]['amount_available'], int_value)
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

    def update_data_base(self, item_name, stock_value, dispensed_amount):
        item_id = str(self.get_data_id('item_list', 'item_name', item_name, 'item_id'))
        self.update_item_list_stock(stock_value, item_id)
        for key, value in dispensed_amount.items():
            currency_id = str(self.get_data_id('machine_funds', 'currency_name', key, 'currency_id'))
            self.update_funds(currency_id, value)

    def update_item_list_stock(self, stock_value, item_id):
        self.data_base_architect.update_table_data('item_list', 'item_amount', 'item_id',
                                                   item_id, stock_value)

    def update_funds(self, currency_id, new_amount):
        self.data_base_architect.update_table_data('machine_funds', 'amount_available', 'currency_id',
                                                   currency_id, new_amount)

    # def update_purchase_history(self, item_id, item_name, item_amount, pay_amount, currency_before_purchase,
    #                            currency_after_purchase):

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
