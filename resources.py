
XE_URL = 'https://www.xe.com/currencyconverter/convert?Amount={amount}&From={source}&To={target}'

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