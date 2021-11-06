#********************************************************************************
#
# Builds a config file for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

from emod_api.config import default_from_schema_no_validation as dfs

#********************************************************************************

def update_config_obj(config):

  # ***** Get variables for this simulation *****
  RUN_NUM        = gdata.var_params['run_number']
  TIME_DELTA     = gdata.var_params['num_tsteps']
  BI_STD         = gdata.var_params['base_inf_stddev_mult']


  # ***** Random number seed ****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     =    0.0
  config.parameters.Simulation_Duration                            = TIME_DELTA

  config.parameters.Enable_Termination_On_Zero_Total_Infectivity   =    1
  config.parameters.Minimum_End_Time                               =   50.0


  # ***** Intrahost *****
  if(BI_STD > 0.01):
    config.parameters.Base_Infectivity_Distribution                = 'GAMMA_DISTRIBUTION'
    config.parameters.Base_Infectivity_Scale                       =    0.5*BI_STD*BI_STD
    config.parameters.Base_Infectivity_Shape                       =    1.0/BI_STD/BI_STD
  else:
    config.parameters.Base_Infectivity_Distribution                = 'CONSTANT_DISTRIBUTION'
    config.parameters.Base_Infectivity_Constant                    =    0.5

  config.parameters.Incubation_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean                =    3.0
  config.parameters.Incubation_Period_Gaussian_Std_Dev             =    1.0

  config.parameters.Infectious_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Infectious_Period_Gaussian_Mean                =    3.0
  config.parameters.Infectious_Period_Gaussian_Std_Dev             =    1.0

  config.parameters.Enable_Disease_Mortality                       =    0


  # ***** Strain Tracking *****
  config.parameters.Enable_Strain_Tracking                         =    1
  config.parameters.Enable_Label_By_Infector                       =    1

  # ***** Interventions *****
  config.parameters.Enable_Network_Infectivity                     =    1

  config.parameters.Network_Infectivity_Coefficient                =   [1.0]
  config.parameters.Network_Infectivity_Exponent                   =   [0.0]


  # ***** Immunity *****
  config.parameters.Enable_Immunity                                =    1
  config.parameters.Enable_Immune_Decay                            =    0

  config.parameters.Post_Infection_Acquisition_Multiplier          =    0.0
  config.parameters.Post_Infection_Transmission_Multiplier         =    0.0
  config.parameters.Post_Infection_Mortality_Multiplier            =    0.0


  # ***** Interventions *****
  config.parameters.Enable_Interventions                           =    1
  config.parameters.Campaign_Filename                              = gdata.camp_file


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                       = 'TRACK_ALL'


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin                    =    1

  config.parameters.Default_Geography_Initial_Node_Population      =  312
  config.parameters.Default_Geography_Torus_Size                   =    4

  config.parameters.Enable_Vital_Dynamics                          =    0


  # ***** Reporting *****
  config.parameters.Enable_Default_Reporting                       =    1
  config.parameters.Enable_Event_DB                                =    1
  config.parameters.SQL_Events                                     = ["NewInfection"]

  config.parameters.Custom_Reports_Filename                        = gdata.reports_file


  return config

#********************************************************************************

def configBuilder():

  FILE_CONFIG  =  'config_useful.json'
  SCHEMA_PATH  =  gdata.schema_path

  default_conf = dfs.get_default_config_from_schema(SCHEMA_PATH,as_rod=True)

  # Probably ought to be an emod-api call
  config_obj = update_config_obj(default_conf);
  config_obj.parameters.finalize()
  with open(FILE_CONFIG, 'w') as fid01:
    json.dump(config_obj, fid01, sort_keys=True, indent=4)


  return FILE_CONFIG

#********************************************************************************