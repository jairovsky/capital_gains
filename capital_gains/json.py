import json
import decimal
import typing

def parse(string: str) -> typing.Any:
    return json.loads(string, parse_float=decimal.Decimal)

def serialize(obj: typing.Any) -> str:
    return json.dumps(obj, separators=(',', ':'))