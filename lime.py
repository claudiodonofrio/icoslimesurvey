# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 09:59:32 2019

@author: Claudio
"""

import icoslimer
import base64
import pandas as pd
import io
import os
import matplotlib.pyplot as plt
import report
import shutil



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
    #print(s['sid'])
    

# ------------------------------------------------------------------    
# get the statistics for all surveys
# ------------------------------------------------------------------

# define the output format from limesurvey
# you may choose between html, xls, pdf. Default is set to html
# set "lang" to choose a specific language, leaf blank for survey 
# default language
# set graph to "1" if you like to have bar charts included. Is only
# valid for output format pdf
    
output_format = 'html'
lang = ''
graph = '0'

# empty container to hold all the statistics
stats_list = []

for s in surveys['result']:

    stats = lime.get_statistics(s['sid'], output_format)

    # check if it is a json object and decode base64
    try:        
        stats = base64.b64decode(stats['result'])          
        stats_list.append([s['sid'], stats])
    except:
        print(stats['error'])
        
    
# you can get a timline for each survery. When was each survey 
# submitted? start/endate in form: yyyymmdd

startdate = '20190101'
enddate = '20251231'


timeline_list = []  
for s in stats_list:
    t = lime.get_timeline(s[0], 'day', startdate, enddate)
    timeline_list.append([s[0], t['result']])
    
    
# ------------------------------------------------------------------
# now release the session key
# afterwards you CAN NOT CALL new functions from the survey 
# ------------------------------------------------------------------
lime.release_session_key()


# ------------------------------------------------------------------
# do some fancy stuff with the statistics
# ------------------------------------------------------------------


# denpending on output format for statistics
# you have either pdf's, xls or html files.
# let's safe all the stats to a file. Format depending on output_format

# make sure the output directory exists
if not os.path.isdir('out'):
    os.mkdir('out')

for index, stats in stats_list:
    if not os.path.isdir('./out/'+index):
        os.mkdir('./out/'+index)
    with open('./out/' + index + '/' + index + '.' + output_format, 'wb') as f:
        f.write(stats)

    
    
# if you got the "xls" format you can read the data into a python pandas
# data frame to calculate your own statistics

if output_format == 'xls':
    for id, s in stats_list:
        dataframe = pd.read_excel(io.BytesIO(s))
        # print to console
        print(dataframe)
        
        
# we have extracted the timelines for each survey
# create a pandas data frame with column names
# print to console

    
# print each survey with a "dict" for the time entries
col = ['survey id', 'count per day']
df = pd.DataFrame(timeline_list, columns=col)
print(df)


# or as continous array
val=[]
for t in timeline_list:    
    sid = t[0]
    data = t[1]
    for k,v in data.items():
        val.append([sid,k,v])
    
df = pd.DataFrame(val, columns=['sid', 'time', 'count'])
print(df)
        

# now we create timeline figures and save them
for t in timeline_list:
    fig, ax = plt.subplots()
    ax.grid()
    ax.set(xlabel='date (day)', ylabel='n (count) ',
    title='Timeline for survey submissions')

    ts=[]
    count=[]
    sid = t[0]
    data = t[1]
    for k,v in data.items():        
        ts.append(v)
        count.append(k)
    ax.plot(count, ts, '*')
    ax.plot(count, ts, label=sid)
    ax.legend()
    ax.set_ylim(bottom=0)
    plt.savefig('./out/' + sid + '/' + sid + '_timeline.png', dpi=300, format='png')



# and finally we create a custom report
# but this is only possible, if output_format is HTML

if output_format == 'html':
        
        
    templatename = 'envriplus.html'
    
    for detail in surveys['result']:
        
        sid = detail['sid']    
        report_name = sid + '_report.html'
        
        statistic = None
        timeline = None
        detail = None
    
        # get statistis.
        for s in stats_list:
            if s[0] == sid:
                statistic = s[1]
                
                # prettyfy
                statistic = statistic.decode()            
        
        # find the corresponding timeline 
        for t in timeline_list:
            if t[0] == sid:
                # we assume, the timeline image is already saved.
                timeline = sid + '_timeline.png'
    
        for d in surveys['result']:
            if d['sid'] == sid:
                detail = d            
                
        # if stats or timeline is missing, skip
        if statistic is None or timeline is None or detail is None:
            pass
        else:        
            # create the report and safe to file
            r = report.report(templatename,detail, statistic, timeline)
            folder = './out/' + sid +'/'            
            with open(folder + report_name, 'w') as f:
                f.write(r)
                
            # now we copy the logo and css file into the same directory
            # such that the report is self contained
            shutil.copyfile('./template/envriplus_logo.png', folder + 'envriplus_logo.png')
            shutil.copyfile('./template/envriplus.css', folder + 'envriplus.css')
                
        
        
    
    
    
    
