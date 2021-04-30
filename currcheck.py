#!/usr/bin/env python

import argparse
import re
from dataclasses import dataclass

import bs4
import requests


XE_URL = 'https://www.xe.com/currencyconverter/convert?Amount={amount}&From={source}&To={target}'

@dataclass
class CurrencyConverter:
    amount: float
    source: str
    target: str

    def convert(self) -> str:
        return self._fetch_conversion() if self.source != self.target else str(self.amount)

    def _fetch_conversion(self) -> str:
        """
        This method processes the command and returns the converted amount.

        It calls online and parses the conversion result.

        :return: The converted amount.
        """
        req = requests.get(XE_URL.format(amount=self.amount,source=self.source, target=self.target))
        req.raise_for_status()

        html_result = bs4.BeautifulSoup(req.text, 'html.parser').find(class_='iGrAod')
        html_result.find(class_='faded-digits').decompose()

        return re.sub("[^0-9.]", "", html_result.text)

    @staticmethod
    def validate(val: str, cache=[]) -> str:
        """
        This function validates the input for currency conversion.

        This function is therefore called once for each of the positional parameters.
        Three parameters are given for currency conversion, in the following order:
        - the amount of money to convert.
        - the currency code of the currency to convert.
        - the currency code to convert to.

        :return: The validated argument.
        """
        if len(cache) == 0:
            if not re.match(r"^([0-9]*[.])?[0-9]+$", val):
                raise argparse.ArgumentError()
        else:
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
        prog='currconv',
        description='Currency Checker'
    )

    parser.add_argument(
        '-x',
        required=False,
        metavar=('A', 'S', 'T'),
        type=CurrencyConverter.validate,
        nargs=3,
        help='Converts the amount A from source currency S to target currency T'
    )

    return parser

def parse_cmd(parser: argparse.ArgumentParser) -> str:
    """
    This function parses the command.

    It calls the appropriate logic to successfully process and parse the input command.

    :return: The command result.
    """
    result: str

    parsed_cmd = parser.parse_args()
    if parsed_cmd.x:
        return CurrencyConverter(*parsed_cmd.x).convert()


if __name__ == '__main__':
    print(parse_cmd(get_parser()))
