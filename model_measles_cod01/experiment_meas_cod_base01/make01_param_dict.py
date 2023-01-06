#********************************************************************************
#
#********************************************************************************

import json

import numpy as np

#*******************************************************************************

# This script makes a json dictionary that is used by the pre-processing script
# in EMOD. Variable names defined here will be available to use in creating
# the input files. Please don't change the variable name for 'EXP_NAME' or
# for 'NUM_SIMS' because those are also used in scripts outside of EMOD.

# The pre-process script will open the json dict created by this method. For
# everything in the 'EXP_VARIABLE' key, that script will assume a list and
# get a value from that list based on the sim index. For everything in the 
# 'EXP_CONSTANT' key, it will assume a single value and copy that value.



# ***** Setup *****
param_dict = dict()

param_dict['EXP_NAME']     = 'MEAS-COD-Base01'
param_dict['NUM_SIMS']     =    32
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']       =     list(range(NSIMS))



# ***** Constants for this experiment *****

# Number of days to run simulation (start Jan 1, 2006)
param_dict['EXP_CONSTANT']['num_tsteps']           =   10#365.0*(7.0) + 1

# R0 value
param_dict['EXP_CONSTANT']['R0']                   =    14.0

# R0 seasonality
param_dict['EXP_CONSTANT']['R0_peak_day']          =    65.0
param_dict['EXP_CONSTANT']['R0_peak_width']        =    45.0
param_dict['EXP_CONSTANT']['R0_peak_magnitude']    =     1.3

# Importation rate per-100k per-day
param_dict['EXP_CONSTANT']['log10_import_rate']    =   -0.50

# Parameters for gravity model for network connections
param_dict['EXP_CONSTANT']['net_inf_power']        =    2.0
param_dict['EXP_CONSTANT']['net_inf_ln_mult']      =   -2.0
param_dict['EXP_CONSTANT']['net_inf_maxfrac']      =     0.1

# Correlation between acqusition and transmission heterogeneity
param_dict['EXP_CONSTANT']['corr_acq_trans']       =     0.9

# Individual level risk variance (acquisition multiplier; mean = 1.0; log-normal distribution)
param_dict['EXP_CONSTANT']['ind_variance_risk']    =     0.6

# Base agent weight; less than 5 may have memory issues
param_dict['EXP_CONSTANT']['agent_rate']           =   12.0

# Node level overdispersion; 0.0 = Poisson
param_dict['EXP_CONSTANT']['proc_overdispersion']  =     0.0

# Subdivide LGAs into 100km^2 regions
param_dict['EXP_CONSTANT']['use_10k_res']          =   False



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
