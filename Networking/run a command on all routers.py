"""
Run a command on all the routers and write success or failure to a text file
"""


from netmiko import ConnectHandler
import os
x=list(range(79))
f= open("list_of_done_router.txt","a+")
g= open("list_of_NOTdone_router.txt","a+")
c=[]
for k in x:
    print(k)
    b='10.0.'+str(k)+'.1' 
    c.append(b);
for a in c:
    host1=a
    l=k
    cisco_881 = {
    'device_type': 'cisco_ios',
    'host':   host1,
    'username': os.environ.get('python_user'),
    'password': os.environ.get('python_pass'),
    'port' : 22,          # optional, defaults to 22
    'secret':os.environ.get('python_secret')  # optional, defaults to ''
    }
    net_connect = ConnectHandler(**cisco_881)
    try:
        net_connect.enable()
        
    except:
        g.write(host1)
    
    f.write(host1)
    config_commands = [ 'ip access-list extended IP-CAMERA',
                                                            'permit ip 10.0.'+str(k)+'.0 0.0.0.31 host 192.168.6.49',
                                                            'permit ip 10.0.'+str(k)+'.0 0.0.0.31 host 192.168.6.49' ]
output = net_connect.send_config_set(config_commands)
print(output)

output = net_connect.send_command('wr')
