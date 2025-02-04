import unittest
import io
from decimal import Decimal
from capital_gains.operation import weighted_average_cost, _round_money, calc_gains, Operation, Kind, Gain

class TestMathFormulas(unittest.TestCase):
    
    def test_initial_average_cost(self) -> None:

        current_average_cost = Decimal(0)
        current_units = 0
        unit_cost = Decimal(20)
        added_units = 10

        new_average_cost = weighted_average_cost(
            current_average_cost,
            current_units,
            unit_cost,
            added_units,
        )

        self.assertEqual(new_average_cost, Decimal('20.00'))

    def test_weighted_average_cost(self) -> None:

        current_average_cost = Decimal(20)
        current_units = 5
        unit_cost = Decimal(10)
        added_units = 5

        new_average_cost = weighted_average_cost(
            current_average_cost,
            current_units,
            unit_cost,
            added_units,
        )

        self.assertEqual(new_average_cost, Decimal('15.00'))

    def test_weighted_average_cost_rounding(self) -> None:
        """Teste de cálculo preço médio arredondado, retirado da descrição do problema:
        Se houver a compra de 10 ações por R$ 20,00 e 5 ações por R$ 10,00,
        o preço médio ponderado é (10 x20,00 + 5 x 10,00) / 15 = 16.67."""

        new_average_cost = weighted_average_cost(
            current_average_cost=Decimal(0),
            current_units=0,
            added_units=10,
            unit_cost=Decimal(20),
        )

        new_average_cost = weighted_average_cost(
            current_average_cost=new_average_cost,
            current_units=10,
            added_units=5,
            unit_cost=Decimal(10),
        )

        self.assertEqual(new_average_cost, Decimal('16.67'))

    def test_weighted_average_cost_rounding_small_value(self) -> None:

        new_average_cost = weighted_average_cost(
            current_average_cost=Decimal('0.01'),
            current_units=1_000_000,
            unit_cost=Decimal('0.06'),
            added_units=100_000,
        )

        self.assertEqual(new_average_cost, Decimal('0.01'))

    def test_weighted_average_cost_rounding_small_value2(self) -> None:

        new_average_cost = weighted_average_cost(
            current_average_cost=Decimal('0.01'),
            current_units=1_000_000,
            unit_cost=Decimal('0.07'),
            added_units=100_000,
        )

        self.assertEqual(new_average_cost, Decimal('0.02'))


    def test_round_money(self) -> None:

        self.assertEqual(_round_money(Decimal('5.666666')), Decimal('5.67'))
        self.assertEqual(_round_money(Decimal('10000.00000001')), Decimal('10000.00'))
        self.assertEqual(_round_money(Decimal('0.015')), Decimal('0.02'))
        self.assertEqual(_round_money(Decimal('0.055')), Decimal('0.06'))
        self.assertEqual(_round_money(Decimal('0.0554')), Decimal('0.06'))
        self.assertEqual(_round_money(Decimal('0.054')), Decimal('0.05'))


class TestDocumentedCases(unittest.TestCase):
    "A descrição desses testes está na própria descrição do problema"

    def test_case_1(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=100),
            Operation(kind=Kind.SELL, unit_cost=Decimal('15.00'), quantity=50),
            Operation(kind=Kind.SELL, unit_cost=Decimal('15.00'), quantity=50),
        ])

        expected = [Gain.no_tax(), Gain.no_tax(), Gain.no_tax()]

        self.assertListEqual(gains, expected)

    def test_case_2(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('20.00'), quantity=5000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('5.00'), quantity=5000),
        ])

        expected = [Gain.no_tax(), Gain(tax=Decimal('10000.00')), Gain.no_tax()]

        self.assertListEqual(gains, expected)

    def test_case_3(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('5.00'), quantity=5000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('20.00'), quantity=3000),
        ])

        expected = [Gain.no_tax(), Gain.no_tax(), Gain(tax=Decimal('1000.00'))]

        self.assertListEqual(gains, expected)
    
    def test_case_4(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.BUY, unit_cost=Decimal('25.00'), quantity=5000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('15.00'), quantity=10000),
        ])

        expected = [Gain.no_tax(), Gain.no_tax(), Gain.no_tax()]

        self.assertListEqual(gains, expected)

    def test_case_5(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.BUY, unit_cost=Decimal('25.00'), quantity=5000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('15.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('25.00'), quantity=5000),
        ])

        expected = [Gain.no_tax(), Gain.no_tax(), Gain.no_tax(), Gain(tax=Decimal('10000.00'))]

        self.assertListEqual(gains, expected)

    def test_case_6(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('2.00'), quantity=5000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('20.00'), quantity=2000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('20.00'), quantity=2000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('25.00'), quantity=1000),
        ])

        expected = [
            Gain.no_tax(),
            Gain.no_tax(),
            Gain.no_tax(),
            Gain.no_tax(),
            Gain(tax=Decimal('3000.00')),
        ]

        self.assertListEqual(gains, expected)

    def test_case_7(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('2.00'), quantity=5000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('20.00'), quantity=2000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('20.00'), quantity=2000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('25.00'), quantity=1000),
            Operation(kind=Kind.BUY, unit_cost=Decimal('20.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('15.00'), quantity=5000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('30.00'), quantity=4350),
            Operation(kind=Kind.SELL, unit_cost=Decimal('30.00'), quantity=650),
        ])

        expected = [
            Gain.no_tax(),
            Gain.no_tax(),
            Gain.no_tax(),
            Gain.no_tax(),
            Gain(tax=Decimal('3000.00')),
            Gain.no_tax(),
            Gain.no_tax(),
            Gain(tax=Decimal('3700.00')),
            Gain.no_tax(),
        ]

        self.assertListEqual(gains, expected)

    def test_case_8(self) -> None:
        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('50.00'), quantity=10000),
            Operation(kind=Kind.BUY, unit_cost=Decimal('20.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('50.00'), quantity=10000),
        ])

        expected = [
            Gain.no_tax(),
            Gain(tax=Decimal('80000.00')),
            Gain.no_tax(),
            Gain(tax=Decimal('60000.00')),
        ]

        self.assertListEqual(gains, expected)

class TestExtraCases(unittest.TestCase):
    
    def test_all_stocks_sold(self) -> None:

        gains = calc_gains([
            Operation(kind=Kind.BUY, unit_cost=Decimal('20.00'), quantity=10099),
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('16.00'), quantity=20099),
            Operation(kind=Kind.BUY, unit_cost=Decimal('20.00'), quantity=10000),
            Operation(kind=Kind.BUY, unit_cost=Decimal('10.00'), quantity=10000),
            Operation(kind=Kind.SELL, unit_cost=Decimal('16.00'), quantity=20000),
        ])

        expected = [
            Gain.no_tax(),
            Gain.no_tax(),
            Gain(tax=Decimal('3939.4')),
            Gain.no_tax(),
            Gain.no_tax(),
            Gain(tax=Decimal(4000)),
        ]

        self.assertEqual(gains, expected, "Ao vender todas ações deve zerar o preço médio")