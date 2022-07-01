"""
This script runs a command to shut all the unused port on multiple routers. The routers are in range such as 10.0.10.254, 10.0.11.254, 10.0.12.254 and so on.
"""

from netmiko import ConnectHandler
import os
#from operator import itemgetter
from getpass import getpass
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException



####Connect to the switch 
for IP in range(10,60):

    cisco_881 = {
                'device_type':'cisco_ios',
                'host': '10.0.'+str(IP)+'.254',
                'username': os.environ.get('python_user'),
                'password': os.environ.get('python_pass'),
                'port' : 22, 
                'secret' : os.environ.get('python_secret')
    }

    print('Connecting to the Router' + cisco_881['host'])
    net_connect = ConnectHandler(**cisco_881)
    net_connect.enable()

    output = net_connect.send_command('show ip int brief',use_textfsm=True)
    l=len(output)
    print('Total interfaces in host ' + cisco_881['host']+' are : ' + str(l))
    print ('\nList of interfaces which are UP \n')
    up_interfaces = []
    down_interfaces=[]
    for i in range(0,l):
        if (output[i]['status'] == 'up') and (output[i]['intf'].find("Fast")!= -1) :
            print (output[i]['intf'] +' ' + output[i]['status'])
            up_interfaces.append(output[i]['intf'])

    print ('\nList of interfaces  in host ' + cisco_881['host']+' which are DOWN : \n')
    for i in range(0,l):
        if output[i]['status'] != 'up' and (output[i]['intf'].find("Fast")!= -1):
            print (output[i]['intf'] +' ' + output[i]['status'])
            down_interfaces.append(output[i]['intf'])
        
    print("THE UP INTERFACES in host " + cisco_881['host']+ " ARE: " + str(up_interfaces))
    print("THE DOWN INTERFACES in host " + cisco_881['host']+ " ARE: " + str(down_interfaces))
    ####going for each interface
    for k in down_interfaces:
    	config_commands=['config t',
    	'interface '+k,
    	'shutdown'
    	]
    	exec_output=net_connect.send_config_set(config_commands)
    	print(exec_output)


