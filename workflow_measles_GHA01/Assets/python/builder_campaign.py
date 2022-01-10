#********************************************************************************
#
# Builds a campaign file for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

from refdat_sias          import data_dict   as dict_sia
from refdat_ri            import data_dict   as dict_ri


import numpy as np

import emod_api.campaign     as     camp_module

from emod_api                 import schema_to_class as s2c
from emod_api.interventions   import utils

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****
  TIME_START   = gdata.var_params['start_time']
  PEAK_SIZE    = gdata.var_params['R0_peak_magnitude']
  PEAK_TIME    = gdata.var_params['R0_peak_day']

  # ***** Events *****

  node_dict = gdata.demog_node
  node_opts = list(node_dict.keys())

  # Add MCV RI
  for ri_name in dict_ri:
    ri_obj    = dict_ri[ri_name]
    coverage   = ri_obj['cover']
    node_list  = list()
    for targ_val in ri_obj['nodes']:
      for node_name in node_opts:
        if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
          node_list.append(node_dict[node_name])

    pdict     = {'startday':       TIME_START ,
                 'nodes':          node_list ,
                 'coverage':       coverage  }

    camp_module.add(IV_MCV1(pdict))


  # Add MCV SIAs
  for sia_name in dict_sia:
    sia_obj    = dict_sia[sia_name]
    SIA_COVER  = gdata.var_params['SIA_cover_{:s}'.format(sia_name)]
    start_val  = sia_obj['date']
    age_min    = sia_obj['age_min']
    age_max    = sia_obj['age_max']
    node_list  = list()
    for targ_val in sia_obj['nodes']:
      for node_name in node_opts:
        if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
          node_list.append(node_dict[node_name])

    pdict     = {'startday':       start_val ,
                 'nodes':          node_list ,
                 'agemin':         age_min ,
                 'agemax':         age_max ,
                 'coverage':       SIA_COVER }

    camp_module.add(IV_SIA(pdict))

  # Add infectivity seasonality
  all_nodes  = [node_dict[val] for val in node_opts]
  pdict      = {'startday':       TIME_START ,
                'nodes':          all_nodes ,
                'peak_size':      PEAK_SIZE ,
                'peak_wide':      45.0 ,
                'peak_time':      PEAK_TIME }

  camp_module.add(IV_BumpR0(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************

# Routine immunization for MCV1
def IV_MCV1(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',               SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',    SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('NodeLevelHealthTriggeredIV',  SCHEMA_PATH)
  camp_iv02  = s2c.get_class_with_defaults('DelayedIntervention',         SCHEMA_PATH)
  camp_iv03  = s2c.get_class_with_defaults('Vaccine',                     SCHEMA_PATH)
  camp_wane  = s2c.get_class_with_defaults('WaningEffectConstant',        SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config                 = camp_coord
  camp_event.Start_Day                                = params['startday']
  camp_event.Nodeset_Config                           = node_set

  camp_coord.Intervention_Config                      = camp_iv01

  camp_iv01.Actual_IndividualIntervention_Config      = camp_iv02
  camp_iv01.Demographic_Coverage                      = params['coverage']
  camp_iv01.Trigger_Condition_List                    = ['Births']

  camp_iv02.Actual_IndividualIntervention_Configs     = [camp_iv03]
  camp_iv02.Delay_Period_Distribution                 = "GAUSSIAN_DISTRIBUTION"
  camp_iv02.Delay_Period_Gaussian_Mean                =  300.0
  camp_iv02.Delay_Period_Gaussian_Std_Dev             =   90.0

  camp_iv03.Acquire_Config                            = camp_wane

  camp_wane.Initial_Effect                            =    1.0

  return camp_event

#********************************************************************************

# SIAs for MCV
def IV_SIA(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('Vaccine',                   SCHEMA_PATH)
  camp_wane  = s2c.get_class_with_defaults('WaningEffectConstant',      SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv01
  camp_coord.Target_Demographic             = 'ExplicitAgeRanges'
  camp_coord.Demographic_Coverage           = params['coverage']
  camp_coord.Target_Age_Min                 = params['agemin']/365.0
  camp_coord.Target_Age_Max                 = params['agemax']/365.0

  camp_iv01.Acquire_Config                  = camp_wane

  camp_wane.Initial_Effect                  = 1.0

  return camp_event

#********************************************************************************

# Seasonal infectivity forcing; snaggletooth
def IV_BumpR0(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('NodeInfectivityMult',       SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv01
  camp_coord.Number_Repetitions             =  -1       # Repeat forever
  camp_coord.Timesteps_Between_Repetitions  = 365.0

  init_off =  params['startday']           %365.0
  peak_wid =  params['peak_wide']
  x_peak   = (params['peak_time']-init_off)%365.0
  y_peak   =  params['peak_size']
  x_init   = (x_peak             -peak_wid)%365.0
  x_ends   = (x_peak             +peak_wid)%365.0

  if(peak_wid > x_peak):
    dx_val = x_peak
  elif(peak_wid > 365.0-x_peak):
    dx_val = 365.0-x_peak
  else:
    dx_val = peak_wid

  y_bound  = y_peak - (y_peak-1)/peak_wid * dx_val
  xyvals   = set([(   0.0, y_bound),
                  (x_init,     1.0),
                  (x_peak,  y_peak),
                  (x_ends,     1.0),
                  ( 365.0, y_bound)])
  xyvals   = sorted(list(xyvals), key=lambda val: val[0])

  camp_iv01.Multiplier_By_Duration.Times      = [val[0] for val in xyvals]
  camp_iv01.Multiplier_By_Duration.Values     = [val[1] for val in xyvals]

  return camp_event

#********************************************************************************