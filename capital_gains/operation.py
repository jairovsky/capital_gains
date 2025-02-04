import dataclasses
import decimal
from decimal import Decimal
from enum import Enum
from typing import List, Tuple

MIN_TAXABLE_OPERATION_COST = 20000
PROFIT_TAX_PERCENT = Decimal(.2)
ROUND_CENTS_FORMAT = Decimal('.01')

class Kind(Enum):
    BUY = "buy"
    SELL = "sell"

@dataclasses.dataclass
class Operation:
    kind: Kind
    unit_cost: Decimal
    quantity: int

@dataclasses.dataclass
class Gain:
    tax: Decimal

    @staticmethod
    def no_tax() -> 'Gain':
        return Gain(tax = Decimal(0))

def calc_gains(operations: List[Operation]) -> List[Gain]:
    current_loss = Decimal(0)
    current_units = 0
    current_average_cost = Decimal(0)
    gains = [] #type: List[Gain]

    for op in operations:
        if op.kind == Kind.BUY:
            
            current_average_cost = \
                weighted_average_cost(
                    current_average_cost,
                    current_units,
                    op.unit_cost,
                    op.quantity,
                )

            current_units += op.quantity

            gains.append(dataclasses.replace(Gain.no_tax()))

        elif op.kind == Kind.SELL:
            
            operation_cost = op.quantity * op.unit_cost
            tax = Decimal(0)
            
            if _is_profit(op.unit_cost, current_average_cost):
                profit = (op.unit_cost - current_average_cost) * op.quantity
                profit_accounting_for_loss, loss_after_new_profit = _deduct_loss(profit, current_loss)
                current_loss = loss_after_new_profit
                if _is_taxable(operation_cost):
                    tax = _calc_tax(profit_accounting_for_loss)
            else:
                current_loss += (current_average_cost - op.unit_cost) * op.quantity

            current_units -= op.quantity

            gains.append(Gain(tax=tax))

    return gains

def weighted_average_cost(
    current_average_cost: Decimal,
    current_units: int,
    unit_cost: Decimal,
    added_units: int,
) -> Decimal:

    cost = ((current_average_cost * current_units) \
            + (unit_cost * added_units)) \
            / (current_units + added_units)
    
    return _round_money(cost)

def _round_money(value: Decimal) -> Decimal:
    return value.quantize(ROUND_CENTS_FORMAT, rounding=decimal.ROUND_HALF_UP)

def _is_taxable(opcost: Decimal) -> bool:
    return opcost >= MIN_TAXABLE_OPERATION_COST

def _is_profit(unit_cost: Decimal, current_average_cost: Decimal) -> bool:
    """Compara preço de venda e preço médio para decidir se houve lucro.
    A fim de simplificar o código, essa função assume que uma diferença de zero
    (unit_cost == current_average_cost) também é lucro.
    """
    return unit_cost >= current_average_cost

def _deduct_loss(profit: Decimal, current_loss: Decimal) -> Tuple[Decimal, Decimal]:
    "retorna valores atualizados de lucro e prejuízo após subtrair o prejuízo do lucro"
    return max(Decimal(0), profit - current_loss), max(Decimal(0), current_loss - profit)

def _calc_tax(taxable_amount: Decimal) -> Decimal:
    return _round_money(taxable_amount * PROFIT_TAX_PERCENT)
