# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:44:08 2019

@author: Claudio
"""

# export the survyey

import icoslimer
import base64
import pandas as pd
import codecs
import io
import auth as a

# ------------------------------------------------------------------
# set server and authentication
# ------------------------------------------------------------------
# redentials are stored  in a file
# called authy.pass, which is not provided on github.
# you need somehow to provide url, usr, pwd 

url = 'http://path/to/the/limesurvey/remote/control'
usr = 'username'
pwd = 'password'

url = a.local()[0]
usr = a.local()[1]
pwd = a.local()[2]

# ------------------------------------------------------------------
# create a new instance, 
# ------------------------------------------------------------------
lime = icoslimer.IcosLimer()
lime.set_url(url)
lime.set_auth(usr, pwd)
lime.set_session_key()


# ------------------------------------------------------------------
# get a list of all the survyes
# ------------------------------------------------------------------
surveys = lime.list_surveys()

# @param string $sDocumentType any format available by plugins
# examples: pdf, csv, xls, json
        
# we use csv to convert the result to a pandas dataframe
# we create a list of data frames in df_list

output_format = 'csv'
df_list = []
for s in surveys['result']:

    survey = lime.export_responses(s['sid'], output_format)

    # check if result is the expected base64 decode
    try:        
        survey = base64.b64decode(survey['result'])                    
    except:
        print('expected json object, but: ' + str(survey))
        continue

    if output_format == 'csv':
            
        try:
            # convert bytes to string -sig means getting rid of BOM
            survey = codecs.decode(survey, 'utf-8-sig')
            df = pd.read_csv(io.StringIO(survey), sep=';', quotechar='"')
            print(df.head())
            df_list.append(df)
        except:
            print('conversion to pandas dataframe failed')
    else:
        try:
            folder = './out/' + s['sid'] + '/'
            filename = s['sid'] + '_survey.' + output_format 
            with open(folder + filename, 'wb') as f:
                f.write(survey)            
        except:
            print('writing file failed')          
        
    
        




























