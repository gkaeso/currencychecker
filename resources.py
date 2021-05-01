import os.path
import logging

from pathlib import Path


LOG_DIR = Path(os.path.join(Path(__file__).parent, 'log'))
LOG_NAME = 'currcheck.log'

def set_logger() -> None:
    """
    This function defines a basic logger.

    Calls to 'logging' module suffice to call the logger once it has been defined.

    :return: None.
    """
    if not LOG_DIR.exists(): LOG_DIR.mkdir()

    logging.basicConfig(
        filename=LOG_DIR / LOG_NAME,
        level=logging.DEBUG,
        format='%(asctime)s - [%(levelname)s] : %(message)s',
        encoding='utf-8'
    )

    return

XE_URL = 'https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={source}&To={target}'

CONVERSION_VERBOSE = '''
----------------
Currency Checker
----------------
Conversion
--
Amount: {amount}
From:   {source}
To:     {target}
--
Result: {result} {target}
----------------
'''

RATE_VERBOSE = '''
----------------
Currency Checker
----------------
Exchange Rate
--
From:   {source}
To:     {target}
--
Result: 1 {source} = {result} {target}
----------------
'''

ISO_URL = 'https://www.currency-iso.org/dam/downloads/lists/list_one.xml'

ISO_VERBOSE = '''
----------------
Currency Checker
----------------
ISO 4217
--
ISO: {source}
--
Result: CODE={code}, NUM={num} ; 
----------------
'''