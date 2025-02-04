from typing import List
from capital_gains.json import parse, serialize
from capital_gains.operation import Operation, Kind, Gain, calc_gains

def solve(probleminput: str) -> str:

    operations = _from_dicts(parse(probleminput))

    gains = calc_gains(operations)

    return serialize(_to_dicts(gains))

def _from_dicts(dicts: List[dict]) -> List[Operation]:

    operations = []
    for d in dicts:
        operations.append(
            Operation(
                kind      = Kind(d['operation']),
                unit_cost = d['unit-cost'],
                quantity  = d['quantity'],
            )
        )

    return operations

def _to_dicts(gains: List[Gain]) -> List[dict]:
    
    dicts = []
    for g in gains:
        dicts.append({'tax': float(g.tax)})

    return dicts