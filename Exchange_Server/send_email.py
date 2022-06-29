"""
This python script creates a new folder in a location and sends the complete path of the folder via email using an exchange server. The name of the created folder is the date itself. This script is used by me on a daily schedule to send the location of the folder that contains various reports for the Finance department. The reports are loaded into this folder every day via a different cron job.
"""



import os
from datetime import date
###
import subprocess
import time
import pandas as pd
import getpass
import collections
from exchangelib import Account, Configuration, Credentials, DELEGATE, Message, Mailbox
###

###
def connect(server, email, username, password):
                creds = Credentials(username=username, password=password)
                config = Configuration(server=server, credentials=creds)
                return Account(primary_smtp_address=email, autodiscover=False, config = config, access_type=DELEGATE)

a1='mail.sanimabank.com'
a2=os.environ.get('python_user')
a3=os.environ.get('python_user') #using env variables to retreive username and passwords
a4=os.environ.get('python_pass')
a=connect(a1,a2,a3,a4)
print(str(a))
signature='Regards,\nSanima Bank,\nRobotic Process Automation,\nIT Department.'
###

###
def send_email(state):
    m = Message(
        account=a,
        subject='!!!SANIMA BANK LINK(S) ISSUE!!!',

        body='All bodies are beautiful',
        to_recipients=[
            Mailbox(email_address='abhishek.poudel@sanimabank.com'),
        ],
        # Simple strings work, too
        cc_recipients=['abhishek.poudel@sanimabank.com'], 
         # Or a mix of both
    )

    if state=='Success':
    	m.subject='RPA LOAN SMS SENT SUCCESSFULLY'
    	m.body="The SMS for notifying loan interest change to the customer's via RPA bot is sent successfully for today."+'\n\n'+ signature
    	m.send()

    elif state=='Failure':
    	m.subject='RPA LOAN SMS FAILURE'
    	m.body="The SMS for notifying loan interest change to the customer's via RPA bot entered a failed state."+'\n\n'+ signature
    	m.send()

###
today = date.today()
print(f'todays date is : {today}')
d2 = today.strftime("%d%m%Y")
#print(datetime.datetime.today().strftime('%m%d%Y'))
print(d2)
os.chdir(r"C:\Reports")
print(os.getcwd())
list_of_files=os.listdir()
print(a)
k=1


for i in list_of_files:
	if d2 in i:
		k=2
		print('file found')
		break
	else:
		#send_email()

		print('file not found')

if k==2:
	print('SEND SUCCESS EMAIL')
	send_email('Success')
else:
	print('SEND FAILURE EMAIL')
	send_email('Failure')

