# -*- coding: utf-8 -*-

''' Import statements '''
import sys
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportion_confint
# documentation - http://statsmodels.sourceforge.net/devel/generated/statsmodels.stats.proportion.proportion_confint.html

'''Expects a pivoted DataFrame (tbl). Calculates min and max RCA w/ 95%
    confidence returned as 2 separate DataFrames. Uses Fiellers theorum for
    combining 2 confidence intervals - one for the numerator and another for
    the denominator https://en.wikipedia.org/wiki/Fieller's_theorem.'''
def rca_w_confidence(tbl):
    
    '''Wrapper around confidence interval function to be called on a
        pandas dataframe via .apply(), must return a single series.'''
    def conf_int(series, nobs=None, get_max=False):
        nobs = series.sum() or nobs
        get_max = 1 if get_max else 0
        return proportion_confint(series, nobs, method='wilson')[get_max]
    
    '''Get the min and max confidence interval for numerator'''
    p1hat_min = tbl.apply(conf_int, axis=1)
    p1hat_max = tbl.apply(conf_int, axis=1, args=(None, True))
    
    '''Total value in matrix'''
    grand_total = tbl.sum().sum()
    
    '''Get the min and max confidence interval for denominator'''
    (p2hat_min, p2hat_max) = proportion_confint(ybo_pivot.sum(), grand_total, method='wilson')
    
    '''Project denominator conf intervals to same dimensions as tbl'''
    p2hat_min = pd.DataFrame([p2hat_min]*len(tbl.index))
    p2hat_min.index = tbl.index
    p2hat_max = pd.DataFrame([p2hat_max]*len(tbl.index))
    p2hat_max.index = tbl.index
    
    '''Using Fieller's theorem to combine 2 conf intervals'''
    rsa_min_all_new = p1hat_min / p2hat_max
    rsa_max_all_new = p1hat_max / p2hat_min
    
    return rsa_min_all_new, rsa_max_all_new