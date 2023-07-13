#*******************************************************************************

import os, sys

import numpy               as np

sys.path.insert(0, os.path.join('..','refdat_namesets'))
from  aux_namematch  import  reprule, tlc_dict

#*******************************************************************************


# Set three letter country code
COUNTRY = ''


# Parse CSVs
wpp_file1    = r'WPP2022_FERT_F02_FERTILITY_RATES_BY_AGE_ESTIMATES.csv'
with open(wpp_file1, errors='ignore') as fid01:
  flines_rev = [val.strip().split(',') for val in fid01.readlines()]

wpp_file2    = r'WPP2022_FERT_F02_FERTILITY_RATES_BY_AGE_MEDIUM_VARIANT.csv'
with open(wpp_file2, errors='ignore') as fid01:
  flines_fwd = [val.strip().split(',') for val in fid01.readlines()]


# Construct output data structure
pop_dat = np.zeros((0,21), dtype=float)


# Add values from retrospective estimates
for row_val in flines_rev:
  if(reprule(row_val[2]) == tlc_dict[COUNTRY]):
    year_val = int(row_val[10])
    if(year_val%5):
      continue
    bin_pops       = [float(row_val[idx].replace(' ','')) for idx in range(11,20)]
    fert_row       = np.zeros(20, dtype=float)
    fert_row[2:11] = bin_pops
    pop_dat  = np.vstack((pop_dat,np.array([year_val]+fert_row.tolist())))

# Add values from forward projections
for row_val in flines_fwd:
  if(reprule(row_val[2]) == tlc_dict[COUNTRY]):
    year_val = int(row_val[10])
    if(year_val%5):
      continue
    if(year_val == pop_dat[-1,0]):
      continue
    bin_pops = [float(row_val[idx].replace(' ','')) for idx in range(11,20)]
    fert_row       = np.zeros(20, dtype=float)
    fert_row[2:11] = bin_pops
    pop_dat  = np.vstack((pop_dat,np.array([year_val]+fert_row.tolist())))


# Write data files
np.savetxt('fert_dat_{:s}.csv'.format(COUNTRY), pop_dat.T, fmt='%.1f', delimiter=',')

#*******************************************************************************