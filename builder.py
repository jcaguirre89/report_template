# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 09:37:20 2018

@author: crist
"""

import pandas as pd
import numpy as np
import os
import datetime

from jinja2 import Environment, FileSystemLoader

#directories
fileDir = os.path.dirname(os.path.realpath(__file__))
fileName_html = 'report.html'
fileName_pdf = 'report.pdf'


#table 1: holdings summary
holdings_headers = ['Investment', 
                  'Series',
                  'Party Holding Security',
                  'Number',
                  'Yield',
                  'Currency',
                  'Book Cost',
                  'Market Value']
    
#make up data (would come from an SQL query, probably into a dataframe)

holdings1 = ['Deetken Impact Investment Corp.',
            'Series A',
            'Western Pacific Trust Company',
            10,
            8,
            'CAD',
            1000,
            1200]

holdings2 = ['Deetken Impact Investment Corp.',
            'Series B',
            'Western Pacific Trust Company',
            20,
            8,
            'CAD',
            2000,
            3200]

#this will be replaced by a sql query
holdings_df = pd.DataFrame([holdings1, holdings2], columns=holdings_headers)

#calculate total bv and mv
total_bv = holdings_df['Book Cost'].sum()
total_mv = holdings_df['Market Value'].sum()

#each row as list of tuples
holdings_table = list(holdings_df.itertuples(index=False, name=None))

inception_date = datetime.date(2017,1,1)

#table 2: Account Summary
account_headers = ['Investment Period',
                   'Starting Balance',
                   'Deposits',
                   'Withdrawals',
                   'Value Added',
                   'Market Value']

account_index = ['Stated Period',
                 'Last 12 Months',
                 'Since Invested (initial investment on {})'.format(inception_date.strftime('%Y/%m/%d'))]

#account summary table to come straight from a dataframe

account_table = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]


    
#instanciate Jinja templates
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template2.html')


context = {'name': 'Cristobal Aguirre',
           'address': '110 jervis',
           'holdings_headers': holdings_headers,
           'holdings_table': holdings_table,
           'total_bv': total_bv,
           'total_mv': total_mv,
           'account_headers': account_headers,
           'account_index': account_index,
           'account_table': account_table}


#populate template and create html file
html_out = template.render(context)
html_file = open(os.path.join(fileDir, fileName_html),"w")
html_file.write(html_out)
html_file.close()

#create PDF

#HTML TO PDF BOILERPLATE
from xhtml2pdf import pisa             # import python module
# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err


#convertHtmlToPdf(html_out, os.path.join(fileDir, fileName_pdf))

#WEASYPRINT VERSION
#from weasyprint import HTML
#HTML(string=html_out).write_pdf("report.pdf")

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convertHtmlToPdf(html_out, os.path.join(fileDir, fileName_pdf))
