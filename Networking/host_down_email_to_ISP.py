"""
This script reads an excel file for host IP and performs ping operations on those ip. Then it prepares a list of host which are down, having high losses. This list is then emailed to ISP. 
"""

import subprocess
import time
omport os
import pandas as pd
import getpass
import collections
from exchangelib import Account, Configuration, Credentials, DELEGATE, Message, Mailbox
sec1=time.time()
def connect(server, email, username, password):
                creds = Credentials(username=username, password=password)
                config = Configuration(server=server, credentials=creds)
                return Account(primary_smtp_address=email, autodiscover=False, config = config, access_type=DELEGATE)

a1='mail.sanimabank.com'
a2=os.environ.get('python_user') # using env variables for username and password
a3=os.environ.get('python_user')
a4=os.environ.get('python_pass')
a=connect(a1,a2,a3,a4)
print(str(a))
signature='Regards,\nSanima Bank,\nNetwork Monitoring System,\nIT.Department.'



#*******************BEGINNING OF HOST SELECTION PART***************************

isp_list_file=pd.read_excel('branches_ip_list.xlsx',usecols=['Branches','Subisu'])
Subisu_host_down=set()
Subisu_host_up=set()
Subisu_host_latency=set()


def ping_funct(isp):
    for i in isp_list_file.index:
        if str(isp_list_file[isp][i]) != 'na':
            ping_reply = subprocess.run(["ping","-n","2", isp_list_file[isp][i]],stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            print(f'Collecting stats for host: {isp_list_file[isp][i]} , i.e. : {isp_list_file["Branches"][i]}')
            #print('returncode for ' , i, ' is :' , str(ping_reply.returncode ))
            if ping_reply.returncode==0:
                if ('unreachable' in str(ping_reply.stdout)):
                    if isp=='Subisu':
                        Subisu_host_down.add(isp_list_file['Branches'][i])
                    else:
                        pass

                        
                else:
                    print('stdout for ' , i, ' is :' , str(ping_reply.stdout))
                    
                    loss_percent=str(ping_reply.stdout).split('\\r\\n')[6].split(',')[2].split()[3].lstrip('(').rstrip('%')
                    avg_time=str(ping_reply.stdout).split('\\r\\n')[8].split(',')[2].split()[2].rstrip('ms')
                    print(f'loss percentage is {loss_percent} and avg_time is {avg_time}')


                    if isp=='Subisu':
                        Subisu_host_up.add(isp_list_file['Branches'][i])
                        print(f'the loss percent is {loss_percent} and avg_time is {avg_time}')
                        print('Type is: ' , type(avg_time))
                        if int(loss_percent) >= 50 or int(avg_time) >= 100:

                            Subisu_host_latency.add(isp_list_file['Branches'][i])
                        else:
                            pass


                    
            elif ping_reply.returncode==1:
                if isp=='Subisu':
                    Subisu_host_down.add(isp_list_file['Branches'][i])
                else:
                    pass

                
                
            
            #print('stdout for ' , i, ' is :' , str(ping_reply.stdout))
        else:
            print('NO IP TO SCAN....CONTINUING TO NEXT IP...')
        





#******************END OF HOST SELECTION PART***************************************
#*******FUNCTION TO SEND EMAIL************************************
def send_email(to_which_isp, arg1_for_down, arg2_for_latency):
    m = Message(
        account=a,
        subject='!!!SANIMA BANK LINK(S) ISSUE!!!',

        body='All bodies are beautiful',
        to_recipients=[
            Mailbox(email_address='abhishekpoudel1992@gmail.com'),
        
        ],
        # Simple strings work, too
        cc_recipients=['Core-IT@sanimabank.com'], 
         # Or a mix of both
    )



    if to_which_isp == 'Subisu':
        
        m.to_recipients[0].email_address='enterprise.support@subisu.net.np'
        if arg1_for_down is None and arg2_for_latency is None:
            pass
        elif arg1_for_down is not None and arg2_for_latency is None:
            m.subject='!!!SANIMA BANK-LINK(S) DOWN Subisu'
            m.body='Below branch(s) are down at the moment. Please look into the issue on urgent basis.\n\n' + str(Subisu_host_down).lstrip('{').rstrip('}').replace(',','\n') + '\n\n'+ signature
            m.send()
        elif arg1_for_down is None and arg2_for_latency is not None:
            m.subject='!!!SANIMA BANK HIGH LATENCY LINK(S) Subisu '
            m.body='Below branch(s) are facing high latency at the moment. Please look into the issue on urgent basis.\n\n' + str(Subisu_host_latency).lstrip('{').rstrip('}').replace(',','\n') + '\n\n'+ signature
            m.send()
        elif arg1_for_down is not None and arg2_for_latency is not None:
            m.subject='!!!SANIMA BANK LINK(S) DOWN and HIGH LATENCY Subisu'
            m.body='Below branch(s) are down at the moment. \n\n' + str(Subisu_host_down).lstrip('{').rstrip('}').replace(',','\n') + '\n\nBelow branch(s) are facing high latency at the moment.\n\n' +str(Subisu_host_latency).lstrip('{').rstrip('}').replace(',','\n') + '\n\nPlease look into the issue on urgent basis.\n' + '\n\n'+ signature
            m.send()

    

    



#**********CONDITIONS FOR SENDING EMAIL***************************
def condition_for_email(ISP):
    if 'Subisu' in ISP:
        down_list=Subisu_host_down
        latency_list=Subisu_host_latency
    
    
    

    if len(down_list) != 0 or len(latency_list) !=0:
        if len(down_list) != 0 and len(latency_list) !=0:
            #mail to Subisu with message body DOWN AND LATENCY hosts
            #send_email(Subisu, down, latency)
            if ISP=='Subisu':
                send_email('Subisu',down_list,latency_list)
            
            


        elif len(down_list) == 0:
            #mail to Subisu with message body LATENCY hosts
            #send_email(Subisu, null, latency)
            if ISP=='Subisu':
                send_email('Subisu',None,latency_list)
            
            
        elif len(latency_list) ==0:
            #mail to Subisu with message DOWN hosts
            #send_email(Subisu,down,null)
            if ISP=='Subisu':
                send_email('Subisu',down_list,None)
            
            
    elif len(down_list) == 0 and len(latency_list) ==0:
        #do nothing i.e no email
        pass



#PING and create a list



ping_funct('Subisu')

print('Subisu_host_down: ',Subisu_host_down)


#condition_for_email(ISP)




condition_for_email('Subisu')



sec2=time.time()

print('Execution time is : ', sec2-sec1)

