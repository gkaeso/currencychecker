#!/usr/bin/env python

import argparse
import re

import bs4
import requests


def _validate_currency(curr: str) -> str:
    format_regex = re.compile(r"^[a-zA-Z]{3}$")

    if not format_regex.match(curr):
        raise argparse.ArgumentError()

    return curr

def get_parser() -> argparse.ArgumentParser:
    """
    This function defines the parser arguments.

    :return: The parser.
    """
    parser = argparse.ArgumentParser(
        prog='currconv',
        description='Currency Converter'
    )

    parser.add_argument(
        '-s', '--source',
        required=False,
        default='USD',
        metavar='S',
        type=_validate_currency,
        help='The currency to convert'
    )

    parser.add_argument(
        '-t', '--target',
        required=False,
        default='USD',
        metavar='T',
        type=_validate_currency,
        help='The currency needed'
    )

    parser.add_argument(
        'amount',
        metavar='A',
        type=int,
        help='The amount to convert'
    )

    return parser

def _fetch_conversion(amount: float, source: str, target: str) -> float:
    """
    This function processes the command and returns the converted amount.

    It calls online and parses the conversion result.

    :return: The converted amount.
    """
    req = requests.get(f'https://www.xe.com/currencyconverter/convert?Amount={amount}&From={source}&To={target}')
    req.raise_for_status()

    html_result = bs4.BeautifulSoup(req.text, 'html.parser').find(class_='iGrAod')
    html_result.find(class_='faded-digits').decompose()

    return float(re.sub("[^0-9.]", "", html_result.text))

def parse_cmd(parser: argparse.ArgumentParser) -> float:
    """
    This function parses the command.

    :return: The converted amount.
    """
    amount: float

    parsed_cmd = parser.parse_args()

    if parsed_cmd.source != parsed_cmd.target:
        amount = _fetch_conversion(parsed_cmd.amount, parsed_cmd.source, parsed_cmd.target)
    else:
        amount = float(parsed_cmd.amount)

    return amount


if __name__ == '__main__':

    parser = get_parser()
    print(parse_cmd(parser))

