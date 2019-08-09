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

