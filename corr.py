import os, sys
import argparse
import datetime
import logging
import utils
import fetch
import pandas
from pandas.core import datetools
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# give argparse the ability to parse dates
def string_to_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d')

def load_time_series(symbol, start_date=None, end_date=None, downsample_days=1):
    log.info("loading %s for %s to %s" % (symbol, start_date, end_date))
    filename = "%s.csv" % symbol
    if not os.path.exists(filename):
        fetch.fetch_data(symbol)
    data = pandas.read_csv(filename, parse_dates=True, index_col=0)
    data = data.drop(["Open", "High", "Low", "Close", "Volume"], axis=1)
    data = data.rename(columns={"Adj Close" : symbol})
    data = data.sort()
    if data.index[0] > start_date:
        log.warning("no data for %s before %s" % (symbol, data.index[0]))
        return None
        
    data = data.truncate(before=start_date, after=end_date)
    log.info("%d rows after truncating" % len(data))

    # downsample if necessary
    if downsample_days > 1:
        drange = pandas.DateRange(start_date, end_date, offset = downsample_days * datetools.day)
        grouped = data.groupby(drange.asof)
        means = grouped.mean()
        log.info("%d rows after downsampling" % len(means))
        return means
    else:
        return data

def convert_to_excel(csv_filename):
    base_name = os.path.splitext(csv_filename)[0]
    xls_filename = base_name + ".xlsx" 
    try:
        import win32com.client 
        excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
        #excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False
        wb = excel.Workbooks.Open(os.path.abspath(csv_filename)) 
        ws = wb.Worksheets(base_name)
        ws.Range("B2").Select()
        ws.Range(excel.Selection, excel.Selection.End(win32com.client.constants.xlDown)).Select()
        ws.Range(excel.Selection, excel.Selection.End(win32com.client.constants.xlToRight)).Select() 
        CORR_MIN_THRESH = -0.25
        CORR_MAX_THRESH = 0.25
        excel.Selection.FormatConditions.Add(win32com.client.constants.xlCellValue, win32com.client.constants.xlBetween, str(CORR_MIN_THRESH), str(CORR_MAX_THRESH))
        excel.Selection.FormatConditions(1).Interior.ColorIndex = 4
        wb.SaveAs(os.path.abspath(xls_filename), FileFormat=51)
        wb.Close(SaveChanges=0)
    except Exception:
        log.exception("failed to convert %s to %s" % (csv_filename, xls_filename))
    else:
        log.info("converted %s to %s" % (csv_filename, xls_filename))

def compute_correlations(start_date, end_date, downsample_days, name, symbol_file):
    log.info("computing %d-day correlations between %s and %s" % (downsample_days, start_date, end_date))
    ndays = (end_date - start_date).days
    ts0 = None
    for symbol in utils.itersymbols(symbol_file):
        ts = load_time_series(symbol, start_date, end_date, downsample_days=downsample_days)
        if ts is not None:
            if ts0 is None:
                ts0 = ts
            else:
                ts0 = ts0.join(ts)
        else:
            log.warning("skipping %s because data is not available for %s" % (symbol, start_date))
            
        #print "*" * 40
        #print ts
        #print ts0
        #print "*" * 40 

    if ts0:
        corr = ts0.corr()
        filename = "corr_%s_%s_%s-day_%s.csv" % (str(start_date.date()), str(end_date.date()), downsample_days, name)
        corr.to_csv(filename)
        log.info("wrote %s" % filename)
        #convert_to_excel(filename)
    else:
        log.warning("no csv file written")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Correlation runner')
    parser.add_argument('ndays', type=int, help='n-day correlation')
    parser.add_argument('--symbol-file', type=str, default="symbols.txt", help='symbol file name')
    parser.add_argument('--regime-file', type=str, default="regimes.txt", help='regimes file name')
    args = parser.parse_args()
    error = False
    for filename in (args.regime_file, args.symbol_file):
        if not os.path.exists(filename):
            log.error("can't open %s" % filename)
            error = True
    if error:
        sys.exit(1)
        
    for start_date, end_date, name in utils.iterregimes(args.regime_file):
        compute_correlations(start_date, end_date, args.ndays, name, args.symbol_file)
            