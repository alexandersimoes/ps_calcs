# -*- coding: utf-8 -*-

''' Import statements '''
import sys
import numpy as np
try:
    import statsmodels.api as sm
except ImportError as err:
    print "Warning: failed to import statsmodels module. Unable to " \
                        "run MHAT calculations. ({})".format(err)
import pandas as pd

def mhat(mcp, right_side, regression_type):
    
    # prepare data by unravelling matricies to long lists
    mcp_list = mcp.values.ravel()

    # run regression
    if regression_type == "ols":
        model = sm.OLS(mcp_list, right_side)
        results = model.fit()
    else:
        # print mcp_list[:10]
        # sys.exit()
        
        model = sm.Logit(mcp_list, right_side)
        # model = sm.Logit([1, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 1])
        results = model.fit()
        sys.exit()
    
    # print logit_results.__doc__
    # print logit_results.params
    # print results.summary()

    prediction = results.predict(right_side)

    # repackage so it is same shape as mcp
    prediction = prediction.reshape((len(mcp.index), len(mcp.columns)))
    prediction = pd.DataFrame(prediction, index=mcp.index, columns=mcp.columns)

    return prediction
