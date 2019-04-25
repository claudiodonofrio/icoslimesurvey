# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:26:57 2019

@author: Claudio
"""

# now create a custom report with all the information
# the template engine jinja2 is used
import jinja2
import datetime

# -------------------------------------------------------------------------
def report(templatename, details, stats, timeline):
    gen_date = datetime.datetime.utcnow().isoformat()
    
    templateLoader = jinja2.FileSystemLoader(searchpath = './template/')
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(templatename)
    
    
    report = template.render(gen_date=gen_date,
                             details=details,
                             stats = stats,
                             timeline=timeline)
    
    return report

# -------------------------------------------------------------------------
