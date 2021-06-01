CURRENCY CHECKER
----------------

A python program checking various details on currencies worldwide.

_______________

## Objective

The idea behind this app was to:

- create a **command-line** program
- do **web-scraping**

_______________

## Installation

Requires Python 3.9.

Clone this Git repository, then move to the directory and run the following install:
  
    pip install -r requirements.txt

_______________

## Usage

This is a command-line program which scrapes currency-related
content online and display the output in the terminal.

##### Currency Converter

To convert A amount from a source currency C to target currency T, run:
  
    python currencychecker.py -x A C T [-v]

The amount must be a positive integer or decimal.

Currencies must be the standard three-letter code defined by [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217)

Optional -v argument increases the output verbosity.

_e.g._

    python currencychecker.py -x 150.10 USD EUR -v
    
_N.B._ This program uses [xe.com](https://www.xe.com/) to get cuurency conversions. 

##### Exchange Rate

To check the exchange rate from a source currency C to target currency T, run:
  
    python currencychecker.py -r C T [-v]

Currencies must be the standard three-letter code defined by [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217)

Optional -v argument increases the output verbosity.

_e.g._

    python currencychecker.py -r USD EUR -v
    
_N.B._ This program uses [xe.com](https://www.xe.com/) for exchange rates.
    
##### ISO 4217

To check the exchange rate from a source currency C to target currency T, run:
  
    python currencychecker.py -i C

Currency must be the standard three-letter code or three-digit number defined by [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217)

Optional -v argument increases the output verbosity.

_e.g._

    python currencychecker.py -i EUR -v
    python currencychecker.py -i 978 -v

_N.B._ This program uses [currency-iso.org](https://www.currency-iso.org/) for ISO details.

_______________

## Technical

Web-scraping implemented using libraries:
- **requests**, for HTTP requests
- **beautifulsoup4**, for HTML parsing
- **lxml**, (via beautifulsoup4) for XML parsing

_N.B._ Requests made by this program are mostly quick. 
However, the target websites called in the program sometimes slow HTTP 
requests down on purpose if too many are made. 
This program does not mimic any browser user agent.
    
