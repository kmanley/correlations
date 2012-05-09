import datetime

def string_to_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d')

def itersymbols(symbol_file):
    with open(symbol_file) as fp:
        for line in fp:
            # allow '#' comments in symbol file
            symbol = line.strip().upper().split("#")[0]
            if symbol:
                yield symbol
                
def iterregimes(regime_file):
    with open(regime_file) as fp:
        for line in fp:
            # allow '#' comments in symbol file
            regime = line.strip().split("#")[0]
            if regime:
                sdates, name = regime.split(":")
                sdate1, sdate2 = sdates.split(" to ")
                yield string_to_date(sdate1.strip()), string_to_date(sdate2.strip()), name.strip()
                    
if __name__ == "__main__":
    for item in itersymbols("symbols.txt"):
        print item
        
    for item in iterregimes("regimes.txt"):
        print item

