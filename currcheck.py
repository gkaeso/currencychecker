#!/usr/bin/env python

import argparse
import logging
import re
from dataclasses import dataclass

import bs4
import requests

from resources import set_logger, XE_URL, CONVERSION_VERBOSE, RATE_VERBOSE


set_logger()

@dataclass
class CurrencyChecker:

    amount: float
    source: str
    target: str

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

        #req = requests.get(XE_URL.format(amount=self.amount, source=self.source, target=self.target))
        #req.raise_for_status()

        logging.info('Parsing result')

        #html_result = bs4.BeautifulSoup(req.text, 'html.parser').find(class_='dEqdnx').find('p')

        return re.sub(r"[^0-9.]", "", '12.00')#html_result.text.split('=')[1])

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
        This function validates the input for currency conversion.

        This function is therefore called once for each of the positional parameters.
        Three parameters are given for currency conversion, in the following order:
        - the currency code of the currency to convert.
        - the currency code to convert to.

        :return: The validated argument.
        """
        logging.debug(f'Validating arg: {val}')

        if not re.match(r"^[a-zA-Z]{3}$", val):
            raise argparse.ArgumentError()
        cache.append(val)

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
        result = CurrencyChecker(*['10', *parsed_cmd.r]).exchange_rate()
        if parsed_cmd.v:
            logging.debug('Set verbose on')
            result = RATE_VERBOSE.format(
                source=parsed_cmd.r[0],
                target=parsed_cmd.r[1],
                result=result
            )
    else:
        parser.error('Missing valid argument')
        logging.error('Missing valid argument')

    logging.info(result)

    return result


if __name__ == '__main__':

    logging.info('START - CURRENCY CHECKER')

    print(parse_cmd(get_parser()))

    logging.info('STOP - CURRENCY CHECKER')
