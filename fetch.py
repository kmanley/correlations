import os
import sys
import argparse
#from http import HTTPClient
import requests
import utils
import datetime
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def fetch_data(symbol):
    url = "http://ichart.yahoo.com/table.csv?s=%s&a=00&b=1&c=1980&g=d&ignore=.csv" % symbol
    log.info("downloading data for %s" % symbol)
    data = requests.get(url).text
    filename = "%s.csv" % symbol
    with open(filename, "w") as fp:
        fp.write(data)
    log.info("Wrote file '%s'" % filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Yahoo! price fetcher')
    parser.add_argument('--symbol-file', type=str, default="symbols.txt", help='symbol file name')
    args = parser.parse_args()
    if os.path.exists(args.symbol_file):
        for symbol in utils.itersymbols(args.symbol_file):
            fetch_data(symbol)
    else:
        log.error("can't open %s" % args.symbol_file)
        
