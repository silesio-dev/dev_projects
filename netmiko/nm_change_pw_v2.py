# 20211209 
# this script changes the password for admin username for Cisco devices
import time
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from tabulate import tabulate


def change_password(username):

    config = ['username ' + username + ' secret cisco2021']
    command = login.send_config_set(config)

    return print('Password changed on', ip)


hosts = open("hosts.txt")
table = []

for ip in hosts:
    
    device = {
        'ip': ip,
        'username': 'silesio',
        'password': 'password',
        'device_type': 'cisco_ios'
    }

    report = ''
    table_row = ip, report

    try:
        login = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip)
        report = 'Timeout to device'
        table_row = ip, report
        table.append(table_row)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip)
        report = 'End of file while attempting device'
        table_row = ip, report
        table.append(table_row)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip)
        report = 'SSH Issue. Are you sure SSH is enabled?'
        table_row = ip, report
        table.append(table_row)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        report = 'SSH Issue. Are you sure SSH is enabled?'
        table_row = ip, report
        table.append(table_row)
        continue    
    
    print('\nConnecting to IP:', ip)
    get_username = login.send_command('show run | in admin')
    # this condition is used to validate whether user admin was found
    if get_username == '':
        print('Username admin not found!')
        report = 'Username admin not found!'
    elif get_username != '':
        get_admin = get_username.split()
        username = get_admin[1]
        if username == 'admin':
            change_password(username)
            report = 'Password changed.'
    else:
        print('An error must have ocurred')
        report = 'An error must have ocurred!'

    table_row = ip, report
    table.append(table_row)


table_header = ['Device', 'Report']

time.sleep(1)
print('\nYour report is being processed...')
print(tabulate(table, table_header, tablefmt='fancy_grid'))
