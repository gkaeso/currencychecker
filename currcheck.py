#!/usr/bin/env python

import argparse
import logging
import re
from dataclasses import dataclass

import bs4
import requests

from resources import set_logger, XE_URL, CONVERSION_VERBOSE, RATE_VERBOSE, ISO_URL, ISO_VERBOSE


set_logger()

@dataclass
class CurrencyChecker:

    amount: float
    source: str
    target: str
    is_verbose: bool

    def __init__(self, source, is_verbose):
        self.amount = 0
        self.source = source
        self.target = ''
        self.is_verbose = is_verbose

    def convert(self) -> str:
        return self._convert() if self.source != self.target else str(self.amount)

    def _convert(self) -> str:
        """
        This method fetches the currency conversion online and parses the result.

        :return: The converted amount.
        """
        logging.info('Fetching conversion')

        req = requests.get(XE_URL.format(amount=self.amount, source=self.source, target=self.target))
        req.raise_for_status()

        logging.info('Parsing result')

        html_result = bs4.BeautifulSoup(req.text, 'html.parser').find(class_='iGrAod')
        html_result.find(class_='faded-digits').decompose()

        return re.sub(r"[^0-9.]", "", html_result.text)

    def exchange_rate(self) -> str:
        return self._exchange_rate() if self.source != self.target else str(1.00)

    def _exchange_rate(self) -> str:
        """
        This method fetches the currency exchange rate online and parses the result.

        :return: The exchange rate.
        """
        logging.info('Fetching exchange rate')

        req = requests.get(XE_URL.format(amount=self.amount, source=self.source, target=self.target))
        req.raise_for_status()

        logging.info('Parsing result')

        html_result = bs4.BeautifulSoup(req.text, 'html.parser').find(class_='dEqdnx').find('p')

        return re.sub(r"[^0-9.]", "", html_result.text.split('=')[1])

    def iso(self) -> str:
        return self._iso(self.source.isdigit())

    def _iso(self, is_digit: bool) -> str:
        """
        This method fetches the ISO 4217 details of a currency.

        The input command-line argument can be the ISO_NUM or the ISO_CODE.
        This method will fetch and return both.

        :return: (ISO_CODE,ISO_NUM). # see https://www.iso.org/iso-4217-currency-codes.html
        """
        result: str

        logging.info('Fetching the ISO details')

        req = requests.get(ISO_URL)
        req.raise_for_status()

        logging.info('Parsing result')

        root_xml = bs4.BeautifulSoup(req.text, 'xml')
        iso_xml: bs4.element.Tag
        try:
            if is_digit:
                iso_xml = root_xml.find('CcyNbr', text=self.source).parent
            else:
                iso_xml = root_xml.find('Ccy', text=self.source).parent
        except AttributeError as e:
            logging.error(f'Currency code {self.source} is invalid')
            raise ValueError(f'Currency code {self.source} is invalid')

        iso_code, iso_num = iso_xml.find('Ccy').text, iso_xml.find('CcyNbr').text
        if self.is_verbose:
            result = ISO_VERBOSE.format(source=self.source, code=iso_code, num=iso_num)
        else:
            result = '{},{}'.format(iso_code, iso_num)

        return result

class _CurrencyCheckerValidator:

    @staticmethod
    def validate_convert(val: str, cache: list = []) -> str:
        """
        This function validates the input for currency conversion.

        This function is therefore called once for each of the positional parameters.
        Three parameters are given for currency conversion, in the following order:
        - the amount of money to convert.
        - the currency code of the currency to convert.
        - the currency code to convert to.

        :return: The validated argument.
        """
        logging.debug(f'Validating arg: {val}')

        if len(cache) == 0:
            if not re.match(r"^([0-9]*[.])?[0-9]+$", val):
                raise argparse.ArgumentError()
        else:
            if not re.match(r"^[a-zA-Z]{3}$", val):
                raise argparse.ArgumentError()
        cache.append(val)

        return val

    @staticmethod
    def validate_exchange_rate(val: str, cache: list = []) -> str:
        """
        This function validates the input for currency exchange rate.

        This function is therefore called once for each of the positional parameters.
        Two parameters are given for currency exchange rate, in the following order:
        - the currency code of the currency to convert.
        - the currency code to convert to.

        :return: The validated argument.
        """
        logging.debug(f'Validating arg: {val}')

        if not re.match(r"^[a-zA-Z]{3}$", val):
            raise argparse.ArgumentError()
        cache.append(val)

        return val

    @staticmethod
    def validate_iso(val: str) -> str:
        """
        This function validates the input for currency ISO search.

        This function is therefore called once for each of the positional parameters.
        One parameter is given for currency ISO search, but may be of two different types:
        - three-digit sequence
        - three-letter sequence

        :return: The validated argument.
        """
        logging.debug(f'Validating arg: {val}')

        if not re.match(r"^[a-zA-Z]{3}$", val) and not re.match(r"^[0-9]{3}$", val):
            raise argparse.ArgumentError()

        return val

def get_parser() -> argparse.ArgumentParser:
    """
    This function defines the command parser.

    :return: The parser.
    """
    parser = argparse.ArgumentParser(
        prog='currencychecker',
        description='Currency Checker'
    )

    parser.add_argument(
        '-x',
        required=False,
        metavar=('A', 'S', 'T'),
        type=_CurrencyCheckerValidator.validate_convert,
        nargs=3,
        help='Converts the amount A from source currency S to target currency T'
    )

    parser.add_argument(
        '-r',
        required=False,
        metavar=('S', 'T'),
        type=_CurrencyCheckerValidator.validate_exchange_rate,
        nargs=2,
        help='Checks the exchange rate from source currency S to target currency T'
    )

    parser.add_argument(
        '-i',
        required=False,
        metavar='C',
        type=_CurrencyCheckerValidator.validate_iso,
        nargs=1,
        help='Gets the ISO 4217 details of a currency C'
    )

    parser.add_argument(
        '-v',
        required=False,
        help='Adds output verbosity',
        action='store_true'
    )

    return parser

def parse_cmd(parser: argparse.ArgumentParser) -> str:
    """
    This function parses the command.

    It calls the appropriate logic to successfully process and parse the input command.

    :return: The command result.
    """
    result: str = ''

    parsed_cmd = parser.parse_args()
    logging.debug('Parsed args')

    if parsed_cmd.x:
        logging.info('Currency Conversion')
        result = CurrencyChecker(*parsed_cmd.x).convert()
        if parsed_cmd.v:
            logging.debug('Set verbose on')
            result = CONVERSION_VERBOSE.format(
                amount=parsed_cmd.x[0],
                source=parsed_cmd.x[1],
                target=parsed_cmd.x[2],
                result=result
            )
    elif parsed_cmd.r:
        logging.info('Currency Exchange Rate')
        result = CurrencyChecker(*[10, *parsed_cmd.r]).exchange_rate()
        if parsed_cmd.v:
            logging.debug('Set verbose on')
            result = RATE_VERBOSE.format(
                source=parsed_cmd.r[0],
                target=parsed_cmd.r[1],
                result=result
            )
    elif parsed_cmd.i:
        logging.info('ISO Search')
        result = CurrencyChecker(*parsed_cmd.i, bool(parsed_cmd.v)).iso()
    else:
        parser.error('Missing valid argument')
        logging.error('Missing valid argument')

    logging.info(result)

    return result


if __name__ == '__main__':

    logging.info('START - CURRENCY CHECKER')

    print(parse_cmd(get_parser()))

    logging.info('STOP - CURRENCY CHECKER')
