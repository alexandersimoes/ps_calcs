# -*- coding: utf-8 -*-
"""
    Test file for converting OEC data dumps to MCP matrix
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    WARNING: This script looks for a file "data/year_origin_hs92_4.tsv" which is
             excluded from this git repo. Before running this script will need 
             to download this file here: http://atlas.media.mit.edu/static/db/raw/year_origin_hs92_4.tsv.bz2
              ~ or ~
             run the fetch_oec_data.sh script.

    1. Import data to pandas DataFrame
    2. Convert this file to Mcp
    3. Run RCA calculation
    4. Convert to binary (1s and 0s)
"""


import sys
import pandas as pd
# import product space calculations package
from ps_calcs import rca


def main():
    ''' 
        Step 1:
        Import the data file to a pandas DataFrame.
    '''
    try:
        oec_df = pd.read_csv("data/year_origin_hs92_4.tsv", \
                                sep="\t", \
                                converters={"hs92":str})
    except IOError:
        sys.exit("File doesn't exist, use fetch_oec_data.sh to download.")
    

    ''' 
        Step 2:
        Convert our vertically oriented data CPY (country-product-year) into
        the multidimensional Mcp matrix.
        rows     = countries
        columns  = products
    '''
    # Only use most recent year (could loop through each year too...)
    most_recent_year = sorted(oec_df.year.unique())[-1]
    oec_df = oec_df[oec_df.year == most_recent_year]
    
    # We only care about the country, product and export_val columns
    # so let's drop all the others
    oec_df = oec_df[["origin", "hs92", "export_val"]]
    
    # Drop all rows without export value
    oec_df = oec_df[~oec_df.export_val.isnull()]
    
    # Now we pivot our flat file to be countries X products
    mcp = oec_df.pivot(index="origin", columns="hs92", values="export_val")
    
    ''' 
        Step 3:
        Now this is the easiest part, we use the ps_calcs library to run the
        RCA calculation on the Mcp matrix.
    '''
    rcas = rca(mcp)
    
    # Here are some tests...
    # 1. Print the 10 products New Zealand (nzl) has the highest RCA in.
    # 0204 = Sheep and Goat Meat
    # print rcas.ix['nzl'].order(ascending=False).head(10)
    
    # Here are some tests...
    # 1. Print the 10 countries with the highest RCA in cars (8703).
    # SVK = Slovakia
    # print rcas['8703'].order(ascending=False).head(10)


    ''' 
        Step 4:
        Lastly, we can convert our nominal RCA values into binary 1s and 0s,
        1 and > meaning that countries exports their fair share of the product
        and 0 meaning they don't.
    '''
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0
    
    print "Calculation run successfully! Read the source code to see what's going on."
    

if __name__ == "__main__":
    main()