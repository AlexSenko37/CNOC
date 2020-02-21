#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go through dicom files and generate .csv file with Series Description for each scan
@author: alex
"""

import pydicom, glob, csv

basepath = 'DIRECTORY'
seriesNames = []

with open('dicom_metadata.csv','w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['hospital','patient','scan','file','series_name'])

# for each hospital
hospitals = ['MGH MRI', 'BWH MRI']
for hospital in hospitals:
    path = basepath + '/' + hospital + '/'
    
    # for each patient
    for patient in glob.glob(path + '/*'):
        
        # for each scan
        for scan in glob.glob(patient + '/*'):
            if scan[-3:] != 'xml':
            
                # for each file
                file_list = glob.glob(scan + '/*')
                ds = pydicom.filereader.dcmread(file_list[0])
                sd = None
                try:
                    sd = ds.SeriesDescription.lower()
                except:
                    print('no series description')
                path_chunks = file_list[0].replace('\\','/')
                path_chunks = path_chunks.split('/')
                row = [path_chunks[-4], path_chunks[-3], path_chunks[-2], path_chunks[-1], sd]
                with open('dicom_metadata.csv','a') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row)
        
