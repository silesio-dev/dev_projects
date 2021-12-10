# 20211210
# this script will show the number of prefixes per vrf

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from tabulate import tabulate


hosts = open("hosts.txt")

for ip in hosts:
    
    device = {
        'ip': ip,
        'username': 'silesio',
        'password': 'password',
        'device_type': 'cisco_ios'
    }

    try:
        login = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip)
        report = 'End of file while attempting device'
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip)
        report = 'SSH Issue. Are you sure SSH is enabled?'
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        report = 'SSH Issue. Are you sure SSH is enabled?'
        continue    

    table_header = ['Client', 'Total Prefixes in BGP table']
    table = list()

    print('\nConnecting to IP:', ip)
    
    get_vrf_name = login.send_command('show vrf brief | in ipv4')
    vrf_name = get_vrf_name.split()
    
    for name in vrf_name[::4]:
        get_prefixes_entries = login.send_command(f"show ip bgp vpnv4 vrf {name} sum | in network entries")
        
        table_row = name, get_prefixes_entries
        table.append(table_row)


print(tabulate(table, table_header, tablefmt='fancy_grid'))
