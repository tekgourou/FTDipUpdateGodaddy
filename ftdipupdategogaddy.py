import paramiko
import time
import re
from godaddypy import Client, Account

FTDip = 'your CiscoFTD IP'
port = 22
username = 'FTD admin user'
password = 'FTD password'
domain = 'domain - ex : tekgourou.com'
a_record = 'hostname without the domain'
interface = 'FTD interface name'
godaddy_api_key = 'Godaddy API key'
godaddy_api_secret = 'Godaddy API secret'

def godaddyupdate(domain, a_record, IP):
    userAccount = Account(api_key=godaddy_api_key, api_secret=godaddy_api_secret)
    userClient = Client(userAccount)
    try:
        records = userClient.get_records(domain, name=a_record, record_type='A')
        for record in records:
            if IP != record["data"]:
                updateResult = userClient.update_record_ip(IP, domain, name=a_record, record_type='A')
                if updateResult is True:
                    msg = 'Update ended with no Exception.'
            else:
                msg = 'No DNS update needed.'
    except:
        msg = "Update ERROR for {}.{} A record".format(a_record, domain)

    return msg

def get_ip_from_FTD(interface):
    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(FTDip, port=port, username=username, password=password)
    remote_conn = remote_conn_pre.invoke_shell()
    time.sleep(3)
    remote_conn.send("show interface {}\n".format(interface))
    time.sleep(3)
    output2 = remote_conn.recv(700).decode('utf-8')
    print()
    ip_address = r'(?:IP address [\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})'
    foundip2 = re.findall( ip_address, output2 )[0]
    ip_address = r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})'
    IP = re.findall( ip_address, foundip2 )[0]
    print ('{} IP = {}'.format(interface, IP))
    return IP

msg = godaddyupdate(domain, a_record, get_ip_from_FTD(interface))

print (msg)