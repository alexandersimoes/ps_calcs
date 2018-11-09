# -*- coding: utf-8 -*-

''' Import statements '''
import sys
import numpy as np
import pandas as pd

def rca(tbl, populations=None):
  
  # fill missing values with zeros
  tbl = tbl.fillna(0)

  # get sum over columns
  col_sums = tbl.sum(axis=1)

  # we now need to transpose or "reshape" this array so that
  # it is in the form of one long column
  col_sums = col_sums.values.reshape((len(col_sums), 1))

  # create the numerator matrix for the final RCA calculation by
  # dividing each value by its row's sum
  rca_numerator = np.divide(tbl, col_sums)

  # get the sum over all the rows
  row_sums = tbl.sum(axis=0)

  # if populations is set create the denominator based on that for POP RCA
  if populations.__class__ == pd.DataFrame or populations.__class__ == pd.Series:

    # create the denominator matrix for the final RCA calculation
    # by dividing the industry sums by a single value (the matrix total sum)
    rca_denominator = populations / float(populations.sum())
    
    # rca_denominator = rca_denominator.reshape((len(rca_denominator), 1))
    # print rca_numerator.shape
    
    # rca_denominator = pd.DataFrame(rca_denominator, columns=[rca_numerator.columns[0]])
    # rca_denominator = rca_denominator.reindex(index=rca_numerator.index)
    # rca_denominator = rca_denominator.reindex(columns=rca_numerator.columns, method="ffill")
    # print rca_decnominator.ix["ac"]

    # lastly we get the RCAs by dividing the numerator matrix by denominator
    rcas = rca_numerator.T / rca_denominator
    rcas = rcas.T
    

  else:
    # get total of all the values in the matrix
    total_sum = tbl.sum().sum()

    # create the denominator matrix for the final RCA calculation
    # by dividing the industry sums by a single value (the matrix total sum)
    rca_denominator = row_sums / total_sum

    # lastly we get the RCAs by dividing the numerator matrix by denominator
    rcas = rca_numerator / rca_denominator
    

  # rcas[rcas >= 1] = 1
  # rcas[rcas < 1] = 0
  
  return rcas
