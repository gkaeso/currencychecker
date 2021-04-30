#!/usr/bin/env python

import argparse
import re


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
        metavar='S',
        type=_validate_currency,
        help='The currency to convert'
    )

    parser.add_argument(
        '-t', '--target',
        required=False,
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

def parse_cmd(parser: argparse.ArgumentParser) -> None:
    """
    This function parses the command.

    :return: None
    """
    parsed_cmd = parser.parse_args()

    print(f'source={parsed_cmd.source}, target={parsed_cmd.target}, amount={parsed_cmd.amount}')

    return


if __name__ == '__main__':

    parser = get_parser()
    parse_cmd(parser)
