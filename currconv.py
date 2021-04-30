#!/usr/bin/env python

import argparse


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
        type=str,
        help='The currency to convert'
    )

    parser.add_argument(
        '-t', '--target',
        required=False,
        metavar='T',
        type=str,
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
