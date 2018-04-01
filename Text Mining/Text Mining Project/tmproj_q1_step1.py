#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 08:07:27 2017

@author: shutao
"""
import re
import pandas as pd

from utility import hist_list_categories

category_mapping = {
        'Fall from/with ladder':'Falls',
        'Fall from/with platform catwalk (attached to struc':'Falls',
        'Fall from vehicle (vehicle/construction equipment)':'Falls',
        'Fall from/with structure (other than roof)':'Falls',
        'Fall from/with scaffold':'Falls',
        'Fall  other':'Falls',
        'Fall from roof':'Falls',
        'Fall from/with bucket (aerial lift/basket)':'Falls',
        'Collapse of structure':'Collapse of object',
        'Trench collapse':'Collapse of object',
        'Caught in stationary equipment':'Caught in/between Objects',
        'Fire/explosion':'Fires and Explosion',
        'Crushed/run-over of non-operator by operating cons':'Struck By Moving Objects',
        'Struck by falling object/projectile':'Struck By Moving Objects',
        'Crushed/run-over by highway vehicle':'Struck By Moving Objects',
        'Crushed/run-over by construction equipment during':'Struck By Moving Objects',
        'Electrocution by equipment contacting wire':'Electrocution',
        'Crushed/run-over/trapped of operator by operating':'Struck By Moving Objects',
        'Asphyxiation/inhalation of toxic vapor':'Suffocation',
        'Electrocution by touching exposed wire/source':'Electrocution',
        'Drown  non-lethal fall':'Drowning',
        'Fall through opening (other than roof)':'Falls',
        'Unloading-loading equipment/material (except by cr':'Struck By Moving Objects',
        'Electric shock  other and unknown cause':'Electrocution', 
        'Heat/hypothermia':'Exposure to extreme temperatures',
        'Elevator (struck by elevator or counter-weights)':'Struck By Moving Objects',
        'Electrocution from equipment installation/tool use':'Electrocution',
        'Wall (earthen) collapse':'Collapse of object'
    }

# load data
osha_data = pd.read_csv("osha_edit.csv")

# regular expression
regular_expression = r'FatCause:(.*)'

pre_analysis = osha_data['Pre Analysis']
osha_data['category_pred_step1'] = "" # new column
result_col = osha_data['category_pred_step1']

categories = []
for index in range(0,len(pre_analysis)):
    text = pre_analysis[index]
    if text:
        match = re.search(regular_expression, text)
        if match:
            result = match.group(1).strip()
            categories.append(result)
            if result in category_mapping.keys():
                result_col[index] = category_mapping[result]
            
hist_list_categories(categories, 'result/graph_q1_step1.png')

osha_data.to_csv('result/osha_q1_step1.csv')
print("Result save to file 'osha_pred_with.csv'")
