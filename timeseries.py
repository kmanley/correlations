import os, sys
import pandas
from dateutil.parser import parse as parse_date
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def load(symbol, start_date=None, end_date=None, path="data"):
    log.info("loading %s" % symbol)
    filename = os.path.join(path, "%s.csv" % symbol)
    data = pandas.read_csv(filename, parse_dates=True, index_col=0)
    data = data.drop(["Open", "High", "Low", "Close", "Volume"], axis=1)
    data = data.rename(columns={"Adj Close" : symbol})
    data = data.sort()
    data = data.truncate(before=start_date, after=end_date)
    return data
            
            
    
