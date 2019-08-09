from database_functionality.database_architect import DatabaseArchitect


class Mediator(object):

    def __init__(self):
        self.data_base_architect = None

    def get_data_base(self, data_base_architect):
        self.data_base_architect = data_base_architect

    def get_data_from_data_base(self):
        entire_data_base = self.data_base_architect.get_data_base_data()
        for table in entire_data_base:
            print(table[0])
            print(table[1])
            print('\n')


