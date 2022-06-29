"""
This script reads query from an excel file and run the query on an sql database and stores the result of query into an excel file. 
"""

import pyodbc
import pandas as pd
import os

server = '192.168.1.6' 
database = 'ETL' 
username = os.environ.get('python_user') 
password = os.environ.get('python_pass') 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor2 = cnxn.cursor()
query_excel_file=pd.read_excel('D:/AVI/PYTHON/test.xlsx')
script=''

for i in range(len(query_excel_file['ID'])):
    #print(query_excel_file['sql'][i])
    script=query_excel_file['sql'][i]
    df = pd.read_sql_query(script, cnxn)
    print(df)
    df.to_excel(r"C:\Users\abhishek.poudel\Downloads\bulk_sms.xlsx")
    
