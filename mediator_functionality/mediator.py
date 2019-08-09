from database_functionality.database_architect import DatabaseArchitect


class Mediator(object):

    def __init__(self):
        self.data_base_architect = None
        self.entire_data_base = []
        self.item_data = {}
        self.fund_data = {}

    def get_data_base(self, data_base_architect):
        self.data_base_architect = data_base_architect

    def get_data_from_data_base(self):
        self.entire_data_base = self.data_base_architect.get_data_base_data()

    def create_item_and_cost_list(self):
        for row in self.entire_data_base['item_list'].iterrows():
            int_value = 0
            int_value = self.transform_currency_to_int(row[1]['item_cost'])
            if int_value != 0:
                self.item_data[row[1]['item_name']] = (row[1]['item_cost'], int_value)
            else:
                print("item_list table contains data that cannot be formatted to numbers in the item_cost column.")

    def create_funds_list(self):
        for row in self.entire_data_base['machine_funds'].iterrows():
            self.fund_data[row[1]['currency_name']] = (row[1]['amount_available'])

    @staticmethod
    # we convert Text data from the column, which is a string now, to a float followed by int
    # we also convert pounds to their amount in pence
    def transform_currency_to_int(string_cost):
        if '£' in string_cost:
            string_cost = string_cost.replace('£', '')
            try:
                float_conversion = float(string_cost)
                float_conversion *= 100
                int_conversion = int(float_conversion)
                return int_conversion
            except ValueError:
                pass

    def update_item_list_stock(self, item_name, stock_value):
        self.data_base_architect.update_table_data('item_list', 'item_amount', 'item_id',
                                                   str(self.get_data_id('item_list', 'item_name', item_name,
                                                                        'item_id')),
                                                   stock_value)

    def update_funds(self, dispensed_amount):
        print(self.fund_data)
        for key, value in dispensed_amount.items():
            self.data_base_architect.update_table_data('machine_funds', 'amount_available', 'currency_id',
                                                       str(self.get_data_id('machine_funds', 'currency_name', key,
                                                                            'currency_id')),
                                                       self.fund_data[key]-value)

    def get_data_id(self, table_name, column_name, item_name, required_id):
        data_frame = self.entire_data_base[table_name]
        result = data_frame[data_frame[column_name] == item_name][required_id]
        return result.item()
