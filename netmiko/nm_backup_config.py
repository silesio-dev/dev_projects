# performs backup of ios devices with timestamp

from os import write
from netmiko import ConnectHandler
import time
import datetime

# get the date and the time. Change date format to be accepted on windows
time_now = datetime.datetime.now().replace(microsecond=0).strftime('%Y_%m_%d_%H_%M_%S')

# file with IP of host devices
hosts = open('\\hosts.txt')

# folder path where the file will be saved
file_path = '\\Netmiko\\'

for ip in hosts:
    device = {
        'ip': ip,
        'username': 'silesio',
        'password': 'password',
        'device_type': 'cisco_ios'
    }


    login = ConnectHandler(**device)

    # this line removes \n from the ip. Now the ip is inside a list
    ipaddress = ip.split()
    cmd1 = login.send_command('show run')
    
    file = open(file_path + ipaddress[0] +'_'+ str(time_now), 'w')
    file.write(cmd1)
    file.close()

    print(f"Performing backup of {ip}")
    time.sleep(1)
    print(cmd1)
