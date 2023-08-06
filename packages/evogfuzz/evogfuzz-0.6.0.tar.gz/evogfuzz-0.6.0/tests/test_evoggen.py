import unittest
import string
from itertools import product

from pprint import pprint
from typing import Dict
from fuzzingbook.Grammars import Grammar, is_valid_grammar
from fuzzingbook.Parser import EarleyParser, tree_to_string

from evogfuzz.evogfuzz_class import EvoGGen
from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult

def oracle(inp: Input | str):
    def program(inp_):
        if eval(str(inp_)) <= -8:
            return True
        else:
            return False

    try:
        return OracleResult.BUG if program(inp) else OracleResult.NO_BUG
    except SyntaxError:
        return OracleResult.UNDEF

grammar: Grammar = {
    "<start>": ["<number>"],
    "<number>": ["<maybe_minus><one_nine>"],
    "<maybe_minus>": ["-", ""],
    "<one_nine>": [str(i) for i in range(1, 10)],
}

initial_inputs = ["-8", "1"]

def oracle_2(inp: Input | str):
    def program(inp_: str):
        elements = inp_.split(';')
        assert not (-9 <= eval(str(elements[0])) <= -1 and elements[1] == 'fuzzer')

    try:
        program(str(inp))
        return OracleResult.NO_BUG
    except AssertionError:
        return OracleResult.BUG
    except SyntaxError:
        return OracleResult.UNDEF

grammar_2: Grammar = {
    "<start>": ["<number>;<string>"],
    "<number>": ["<maybe_minus><one_nine><digits>"],
    "<maybe_minus>": ["-", ""],
    "<one_nine>": [str(i) for i in range(1, 10)],
    "<digits>": ["<digit><digits>", ""],
    "<digit>": [str(i) for i in range(0,10)],
    "<string>": ['<letter><string>', '<letter>'],
    "<letter>": [char for char in string.ascii_letters]
}

initial_inputs_2 = ["-8;fuzzer", "6;se"]

class TestEvoGGen(unittest.TestCase):
    def setUp(self) -> None:
        # Case #2: oracle, grammar, and initial_inputs
        assert is_valid_grammar(grammar=grammar)

        parser = EarleyParser(grammar=grammar)
        for inp in initial_inputs:
            for tree in parser.parse(inp):
                assert inp == tree_to_string(tree=tree)

        assert oracle(initial_inputs[0]) == OracleResult.BUG
        assert oracle(initial_inputs[1]) == OracleResult.NO_BUG


        # Case #2: oracle_2, grammar_2, and initial_inputs_2
        assert is_valid_grammar(grammar=grammar_2)

        parser = EarleyParser(grammar=grammar_2)
        for inp in initial_inputs_2:
            for tree in parser.parse(inp):
                assert inp == tree_to_string(tree=tree)

        assert oracle_2(initial_inputs_2[0]) == OracleResult.BUG
        assert oracle_2(initial_inputs_2[1]) == OracleResult.NO_BUG

    def test_evoggen(self):
        expected_grammar: Grammar = {
            "<start>": [("<number>", {"prob": None})],
            "<number>": [("<maybe_minus><one_nine>", {"prob": None})],
            "<maybe_minus>": [("-", {"prob": 1}), ("", {"prob": 0})],
            "<one_nine>": [
                ("1", {"prob": 0.0}),
                ("2", {"prob": 0.0}),
                ("3", {"prob": 0.0}),
                ("4", {"prob": 0.0}),
                ("5", {"prob": 0.0}),
                ("6", {"prob": 0.0}),
                ("7", {"prob": 0.0}),
                ("8", {"prob": 0.5}),
                ("9", {"prob": 0.5}),
            ],
        }

        evo = EvoGGen(
            grammar=grammar, inputs=initial_inputs, oracle=oracle, iterations=10
        )

        generator_grammar, failing_inputs = evo.optimize()
        failing_inputs_clean = {str(inp) for inp in failing_inputs}
        self.assertEqual(generator_grammar, expected_grammar)
        self.assertEqual(failing_inputs_clean, {"-8", "-9"})

    def test_evoggen_complex(self):
        evo = EvoGGen(
            grammar=grammar_2, inputs=initial_inputs_2, oracle=oracle_2, iterations=10
        )

        generator_grammar, failing_inputs = evo.optimize()
        failing_inputs_clean = {str(inp) for inp in failing_inputs}
        for i in failing_inputs_clean:
            print(i)
        # self.assertEqual(generator_grammar, expected_grammar)
        #self.assertEqual(failing_inputs_clean, {"-8", "-9"})

    def test_evoggen_transform_grammar(self):
        evo = EvoGGen(
            grammar=grammar_2,
            inputs=initial_inputs_2,
            oracle=oracle_2,
            iterations=100,
            transform_grammar=True
        )

        generator_grammar, failing_inputs = evo.optimize()
        failing_inputs_clean = {str(inp) for inp in failing_inputs}

        expected_result = set()
        for res in product([str(i) for i in range(-9, 0)], ['fuzzer']):
            expected_result.add(f"{res[0]};{res[1]}")
        self.assertSetEqual(expected_result, failing_inputs_clean)

if __name__ == "__main__":
    unittest.main()
