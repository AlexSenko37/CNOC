#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:57:59 2020

Try chosen search terms for dicom metadata previously extracted into .csv file
containing scan series names. Generate a .csv file containing patients, and how
many of each type of scan was matched

@author: alex
"""

#import numpy as np
import pandas as pd

#rule1 =  “C-” OR “Cervical” OR “Cspine” OR “C.” OR “C SPINE” AND/OR “T2" AND “AX” or “Axial”

# read table of metadata from .csv files
metadata = pd.read_csv('dicom_metadata.csv')
metadata = metadata.fillna('none')
metadata['series name'].str.lower()

# change indexing to by hierarchical (hostpial --> patient --> scan #, series desc)
# actually questionable whether this is helpful at this stage, maybe omit

# apply rules to generate rule-specific dataframes
df_cervical = metadata[metadata['series name'].str.contains('c-' or 'cervical' or 'cspine' or 'c.' or 'c spine')]
df_cervical_t1 = df_cervical[df_cervical['series name'].str.contains('t1')]
df_cervical_t2 = df_cervical[df_cervical['series name'].str.contains('t2')]
df_cervical_t1_ax = df_cervical_t1[df_cervical_t1['series name'].str.contains('ax')]
df_cervical_t1_sag = df_cervical_t1[df_cervical_t1['series name'].str.contains('sag')]
df_cervical_t2_ax = df_cervical_t2[df_cervical_t2['series name'].str.contains('ax')]
df_cervical_t2_sag = df_cervical_t2[df_cervical_t2['series name'].str.contains('sag')]

# add a new column (eg, rule1true) of 1s to each rule-specific dataframe
df_cervical_t1_ax['t1 ax'] = 1
df_cervical_t1_sag['t1 sag'] = 1
df_cervical_t2_ax['t2 ax'] = 1
df_cervical_t2_sag['t2 sag'] = 1

# merge dataframes
df_merged = pd.concat([df_cervical_t1_ax, df_cervical_t1_sag, df_cervical_t2_ax, df_cervical_t2_sag], ignore_index = True)
df_merged = df_merged.fillna(0)
df_merged = df_merged.sort_values('patient')
df_merged = df_merged[['hospital','patient','scan','file','series name','t1 ax','t2 ax','t1 sag','t2 sag']]

# add back patients that have zero matches
df_all_patients = df_merged.merge(metadata,on=['hospital','patient','scan','file','series name'],how='right')
df_all_patients = df_all_patients.fillna(0)

# initialize an empty dataframe with the desired final format
df_oppl = pd.DataFrame({'hospital': [],'patient': [],'t1 ax': [],'t1 sag': [],'t2 ax': [],'t2 sag': [],'series names': []})

# get set of patients ids
names = df_all_patients.patient.unique()

# for each patient id
for name in names:
    # get patient's slice of dataframe
    df_patient = df_all_patients[df_all_patients['patient'] == name]
    # build a new dataframe row with the whole patient's summary in one line
    df_patient_ol = pd.DataFrame({'hospital': [df_patient['hospital'].iloc[0]],
                                  'patient': [df_patient['patient'].iloc[0]],
                                  't1 ax': [df_patient['t1 ax'].sum()],
                                  't1 sag': [df_patient['t1 sag'].sum()],
                                  't2 ax': [df_patient['t2 ax'].sum()],
                                  't2 sag': [df_patient['t2 sag'].sum()],
                                  'series names': [df_patient['series name'].tolist()]})
    
    # add row to dataframe
    df_oppl = pd.concat([df_oppl, df_patient_ol], ignore_index = True)
