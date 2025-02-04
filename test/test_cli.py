import unittest
from capital_gains.cli import run
import io

class TestCli(unittest.TestCase):
    
    def test_cli_output_format(self) -> None:
        "json compacto, sem espaço entre separadores, sem zeros extras nas casas decimais"

        with open('test/input.json', 'r') as input_file, \
            open('test/output.json', 'r') as expected_output:
        
            output = run(input_file)

            self.assertListEqual(output.readlines(), expected_output.readlines())