import unittest
from capital_gains.solution import _to_dicts
from capital_gains.operation import Gain
from decimal import Decimal
import io

class TestSolution(unittest.TestCase):
    
    def test_decimal_to_float(self) -> None:

        g = [Gain(tax = Decimal('23.99'))]
        self.assertEqual(_to_dicts(g), [{'tax': 23.99}])