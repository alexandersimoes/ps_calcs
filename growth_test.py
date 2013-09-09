# -*- coding: utf-8 -*-
"""
    Test file for growth library
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The script attempts to use each of the functions in the various files
    found in the growth folder.
    
    The user needs to specify the following variables:
    
    - Database connection *
    - Year (default: 2005)
    - Population cutoff (default: 1,200,000)
    - Total exports cutoff (default: 1,000,000,000)
    
    *required!
"""


import MySQLdb, sys, argparse
import pandas as pd, pandas.io.sql as sql
import numpy as np
# import growth package
import growth

def get_countries(**kwargs):

    cursor = kwargs["db"].cursor()

    '''population cutoff'''
    q = """
    SELECT 
        c.id, c.name 
    FROM 
        observatory_country AS c, observatory_wdi_cwy AS cwy 
    WHERE 
        cwy.wdi_id = 1151 AND cwy.value > {0} AND cwy.year = {1} AND
        cwy.country_id = c.id
    """.format(kwargs["pop_cut"], kwargs["year"])
    cursor.execute(q)

    '''put all the countries that match criteria into a list'''
    pop_cutoff_countries = [c[0] for c in cursor.fetchall()]

    q = """
    SELECT 
        c.id, c.name, sum(export_value) as export_value
    FROM 
        observatory_country AS c, observatory_hs4_cpy as cpy
    WHERE 
        cpy.year = {0} AND cpy.country_id = c.id
    GROUP BY
        cpy.year, cpy.country_id
    HAVING
        export_value > {1}
    """.format(kwargs["year"], kwargs["val_cut"])
    cursor.execute(q)

    '''put all the countries that match criteria into a list'''
    val_cutoff_countries = [c[0] for c in cursor.fetchall()]

    '''merge the two sets by their intersection'''
    usable_countries = set(pop_cutoff_countries).intersection(set(val_cutoff_countries))
  
    return usable_countries

def get_rca_matrix(usable_countries, **kwargs):
    q = """
      SELECT 
          country_id, product_id, export_value 
      FROM 
          observatory_hs4_cpy 
      WHERE 
          year = {0}
      """.format(kwargs["year"])
    mcp_table = sql.read_frame(q, kwargs["db"])

    '''
        transform flat list into multidimentional matrix
        rows     = countries
        columns  = products
    '''
    mcp = mcp_table.pivot(index="country_id", columns="product_id", values="export_value")

    '''
        Again, we need to get the intersection of what is in our list of countries
        (that match the atlas criteria) and the ones found in the data
    '''
    country_list = set(mcp.index).intersection(usable_countries)

    ''' 
        Now we can reindex the mcp matrix with the correct countries
        this funciton takes care of matching up the indexes that exist and
        discarding the ones that don't
    '''
    mcp = mcp.reindex(index=list(country_list), fill_value=0).fillna(0)

    '''using growth stats library to calculate RCAs'''
    mcp = growth.rca(mcp)

    '''convert rcas to 0s and 1s'''
    mcp[mcp >= 1] = 1
    mcp[mcp < 1] = 0

    return mcp

def main(**kwargs):
  
    '''get a list of usable countries by predetermined cutoffs'''
    usable_countries = get_countries(**kwargs)
    print len(usable_countries), "usable countries after cutoffs."

    '''calculate RCAs'''
    mcp = get_rca_matrix(usable_countries, **kwargs)
    print
    print "Matrix of RCAs:"
    print mcp.shape

    '''country complexity '''
    eci = growth.complexity(mcp)[0]
    '''product complexity'''
    pci = growth.complexity(mcp)[1]
    print
    print "PCI & ECI (complexity):"
    print pci.shape, eci.shape

    '''calculate proximities'''
    proximity = growth.proximity(mcp)
    print
    print "Product proximities:"
    print proximity.shape

    '''calculate distances'''
    distances = growth.distance(mcp, proximity)
    print
    print "Distance matrix:"
    print distances.shape

    '''calculate opportunity gain'''
    opp_gain = growth.opportunity_gain(mcp, proximity, pci)
    print
    print "Opportunity gain matrix:"
    print opp_gain.shape
  

if __name__ == "__main__":
    
    '''Get command line arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-db_user", "--db_user", help="DB user name", 
                            default="root")
    parser.add_argument("-db_pw", "--db_pw", help="DB password", default="")
    parser.add_argument("-db_name", "--db_name", help="DB name", 
                            default="atlas")
    parser.add_argument("-pop", "--pop", help="Population cutoff to use", 
                            type=int, default="1200000")
    parser.add_argument("-val", "--val", help="Export value cutoff to use", 
                            type=int, default="1000000000")
    args = parser.parse_args()
    
    '''Try to set up database connection'''
    try:
        db = MySQLdb.connect (host = "localhost",
                              user = args.db_user,
                              passwd = args.db_pw,
                              db = args.db_name)
        db.autocommit(1)
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    
    ''' Set the year of which data will be used '''
    year = 2005 # any random year
    print
    print "Year:", year
  
    '''
        The following are the cutoff imposed by the Atlas, population >1,200,000
        and total export about > $1 Billion (see page 57)
    '''
    population_cutoff = args.pop
    print "Population cutoff:", population_cutoff
    
    total_exports_cutoff = args.val
    print "Total exports value cutoff:", total_exports_cutoff
    print

    main(db=db, year=year, pop_cut=population_cutoff, \
            val_cut=total_exports_cutoff)