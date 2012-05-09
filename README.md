#Correlations#

This is a handy tool for finding uncorrelated assets.

The tool allows you to specify a list of symbols and a list of market regimes. It then:

* Downloads historical prices for your symbols from Yahoo
* Computes price movement correlations between the assets
* Saves the correlation matrix for each regime as a CSV file (optionally an XLS)
 

##Usage##

First, create a new directory
   
    cd correlations
    mkdir example

Next, create a symbols.txt file with one symbol per line

    AAPL
    AMZN
    DELL

Next create a regimes.txt file. Here is the format:

    ########################################
    # Market Regimes
    # One per line. Format:
    # YYYY-MM-DD to YYYY-MM-DD : <name>
    ########################################
    2008-10-05 to 2009-03-06 : Bear
    2009-03-06 to 2012-03-27 : Bull

Next, run the app:

    cd example
    python ..\corr.py 10

The ndays argument tells the script how to aggregate prices when computing the correlations. 

You'll see some logging:

    INFO:root:computing 10-day correlations between 2008-10-05 00:00:00 and 2009-03-06 00:00:00
    INFO:root:loading AAPL for 2008-10-05 00:00:00 to 2009-03-06 00:00:00
    INFO:root:105 rows after truncating
    INFO:root:16 rows after downsampling
    INFO:root:loading AMZN for 2008-10-05 00:00:00 to 2009-03-06 00:00:00
    INFO:root:105 rows after truncating
    INFO:root:16 rows after downsampling
    INFO:root:loading DELL for 2008-10-05 00:00:00 to 2009-03-06 00:00:00
    INFO:root:105 rows after truncating
    INFO:root:16 rows after downsampling
    INFO:root:wrote corr_2008-10-05_2009-03-06_10-day_Bear.csv
    INFO:root:computing 10-day correlations between 2009-03-06 00:00:00 and 2012-03-27 00:00:00
    INFO:root:loading AAPL for 2009-03-06 00:00:00 to 2012-03-27 00:00:00
    INFO:root:772 rows after truncating
    INFO:root:112 rows after downsampling
    INFO:root:loading AMZN for 2009-03-06 00:00:00 to 2012-03-27 00:00:00
    INFO:root:772 rows after truncating
    INFO:root:112 rows after downsampling
    INFO:root:loading DELL for 2009-03-06 00:00:00 to 2012-03-27 00:00:00
    INFO:root:772 rows after truncating
    INFO:root:112 rows after downsampling
    INFO:root:wrote corr_2009-03-06_2012-03-27_10-day_Bull.csv
    
And one CSV file for each regime:

    corr_2008-10-05_2009-03-06_10-day_Bear.csv
    corr_2009-03-06_2012-03-27_10-day_Bull.csv

Open the CSV files to see the correlation matrix:

            AAPL	    AMZN	      DELL
    AAPL	1	        0.182414184	  0.533195992
    AMZN	0.182414184	1	          -0.325296934
    DELL	0.533195992	-0.325296934  1
          

#License#
Copyright (c) 2012 Kevin T. Manley

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
