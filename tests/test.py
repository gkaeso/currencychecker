import argparse
import unittest

from currcheck import CurrencyChecker, _CurrencyCheckerValidator


class TestCurrencyCheckerValidator(unittest.TestCase):

    def test_convert_invalid_regex_1_param_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('ABC', [])

    def test_convert_invalid_regex_2_param_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('1.0.3', [])

    def test_convert_invalid_regex_3_param_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('10A', [])

    def test_convert_valid_param1(self):
        amount: str = '1.00'
        self.assertEquals(_CurrencyCheckerValidator.validate_convert(amount, []), amount)

    def test_convert_invalid_regex_1_param_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('ABCD', ['amount'])

    def test_convert_invalid_regex_2_param_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('100', ['amount'])

    def test_convert_invalid_regex_3_param_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('A2B', ['amount'])

    def test_convert_valid_param2(self):
        source: str = 'ABC'
        self.assertEquals(_CurrencyCheckerValidator.validate_convert(source, ['amount']), source)

    def test_convert_invalid_regex_1_param_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('ABCD', ['amount', 'source'])

    def test_convert_invalid_regex_2_param_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('100', ['amount', 'source'])

    def test_convert_invalid_regex_3_param_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert('A2B', ['amount', 'source'])

    def test_convert_valid_param3(self):
        target: str = 'ABC'
        self.assertEquals(_CurrencyCheckerValidator.validate_convert(target, ['amount', 'source']), target)

    def test_rate_invalid_regex_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_exchange_rate('ABCD')

    def test_rate_invalid_regex_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_exchange_rate('123')

    def test_rate_invalid_regex_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_exchange_rate('A2B')

    def test_rate_valid(self):
        source: str = 'ABC'
        self.assertEquals(_CurrencyCheckerValidator.validate_exchange_rate(source), source)

    def test_iso_invalid_regex_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_iso('ABCD')

    def test_iso_invalid_regex_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_iso('1234')

    def test_iso_invalid_regex_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_iso('A2B')

    def test_iso_valid(self):
        source: str = 'ABC'
        self.assertEquals(_CurrencyCheckerValidator.validate_iso(source), source)
