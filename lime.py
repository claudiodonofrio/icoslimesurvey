# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 09:59:32 2019

@author: Claudio
"""

import icoslimer
import base64
import pandas as pd
import io

# ------------------------------------------------------------------
# set server and authentication
# ------------------------------------------------------------------

url = 'http://localhost/limesurvey/index.php/admin/remotecontrol'
usr = 'limey'
pwd = 'EnvriPlus'


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

for s in surveys['result']:
    print(s)
    print(s['sid'])
    

# ------------------------------------------------------------------    
# get the statistics for all surveys
# ------------------------------------------------------------------

stats_list = []
set_output = 'xls'
for s in surveys['result']:
    
    # define the output format from limesurvey
    # you may choose between html, xls, pdf. Default is set to html
    
    stats = lime.get_statistics(s['sid'], set_output)

    # check if it is a json object, otherwise not statistics found
    try:
        statistics = stats.json()
        statistics = base64.b64decode(statistics['result'])          
        stats_list.append([s['sid'], statistics])
    except:
        print(statistics['error'])
        
    
# ------------------------------------------------------------------
# now release the session key
# ------------------------------------------------------------------
lime.release_session_key()


# ------------------------------------------------------------------
# do some fancy stuff with the statistics
# ------------------------------------------------------------------


# denpending on output format for statistics
# you have either pdf's, xls or html files.
# let's safe all the stats for html or pdf to a file

for id, s in stats_list:
    with open('./out/' + id + '.' + set_output, 'wb') as f:
        f.write(s)

    
    
# if you got the "xls" format you can read the data into a python pandas
# data frome to calculate your own statistics
#stats_list.append([s['sid'], pd.read_excel(io.BytesIO(statistics))])
        
for id, s in stats_list:
    dataframe = pd.read_excel(io.BytesIO(s))
    print(dataframe)


















































