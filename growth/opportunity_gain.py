# -*- coding: utf-8 -*-

''' Import statements '''
import sys
import numpy as np
import pandas as pd
import density

def opportunity_gain(rcas, proximities, pci):
  
  # turn proximities in to ratios out of total
  prox_ratio = proximities / proximities.sum()
  
  # get the inverse of the RCAs matrix. Since they are in the form of 1's and
  # 0's this will flip all of them i.e. 1 = 0 and 0 = 1
  inverse_rcas = 1 - rcas
  
  # convert PCIs to a matrix of repeated values
  pci_matrix = pd.DataFrame(pci.reshape((1, len(pci))), columns=pci.index)
  pci_matrix = pci_matrix.reindex(index=rcas.index, method="ffill") # forward fill
  
  # here we now have the middle part of the equation
  middle = inverse_rcas * pci_matrix
  
  # get the density with the backwards bizzaro RCAs
  dcp = density.density(1-rcas, proximities)
  # now get the inverse
  dcp = 1-dcp
  # we now have the right-half of the equation
  right = dcp * pci_matrix
  
  # matrix multiplication with proximities ratio
  opp_gain = middle.dot(prox_ratio) - right
  
  return opp_gain