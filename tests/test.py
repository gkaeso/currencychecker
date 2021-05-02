import argparse
import unittest

from currcheck import CurrencyChecker, _CurrencyCheckerValidator


class TestCurrencyCheckerValidator(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.valid_amount = '1.00'
        cls.valid_code = 'ABC'
        cls.valid_num = '123'

        cls.invalid_amount_two_decimal_dots = '1.0.0'
        cls.invalid_amount_letters = 'ABC'

        cls.invalid_code_and_num = 'ABCD'
        cls.invalid_code_digits = '100'

        cls.invalid_letters_and_digits = 'A2B'

    def test_convert_invalid_regex_1_param_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_amount_letters, [])

    def test_convert_invalid_regex_2_param_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_amount_two_decimal_dots, [])

    def test_convert_invalid_regex_3_param_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_letters_and_digits, [])

    def test_convert_valid_param1(self):
        self.assertEquals(_CurrencyCheckerValidator.validate_convert(self.valid_amount, []), self.valid_amount)

    def test_convert_invalid_regex_1_param_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_code_and_num, ['amount'])

    def test_convert_invalid_regex_2_param_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_code_digits, ['amount'])

    def test_convert_invalid_regex_3_param_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_letters_and_digits, ['amount'])

    def test_convert_valid_param2(self):
        self.assertEquals(_CurrencyCheckerValidator.validate_convert(self.valid_code, ['amount']), self.valid_code)

    def test_convert_invalid_regex_1_param_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_code_and_num, ['amount', 'source'])

    def test_convert_invalid_regex_2_param_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_code_digits, ['amount', 'source'])

    def test_convert_invalid_regex_3_param_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_convert(self.invalid_letters_and_digits, ['amount', 'source'])

    def test_convert_valid_param3(self):
        self.assertEquals(_CurrencyCheckerValidator.validate_convert(self.valid_code, ['amount', 'source']),  self.valid_code)

    def test_rate_invalid_regex_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_exchange_rate(self.invalid_code_and_num)

    def test_rate_invalid_regex_2(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_exchange_rate(self.invalid_code_digits)

    def test_rate_invalid_regex_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_exchange_rate(self.invalid_letters_and_digits)

    def test_rate_valid(self):
        self.assertEquals(_CurrencyCheckerValidator.validate_exchange_rate(self.valid_code), self.valid_code)

    def test_iso_invalid_regex_1(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_iso(self.invalid_code_and_num)

    def test_iso_invalid_regex_3(self):
        with self.assertRaises(argparse.ArgumentError):
            _CurrencyCheckerValidator.validate_iso(self.invalid_letters_and_digits)

    def test_iso_valid_code(self):
        self.assertEquals(_CurrencyCheckerValidator.validate_iso(self.valid_code), self.valid_code)

    def test_iso_valid_num(self):
        self.assertEquals(_CurrencyCheckerValidator.validate_iso(self.valid_num), self.valid_num)