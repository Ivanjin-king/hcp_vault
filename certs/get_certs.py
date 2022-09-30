import socket
import ssl
import pprint
from datetime import datetime

# cert_file_pathname = 'test_cert'
# s = socket.socket()
def get_cert (host,port):
    context = ssl.create_default_context()
    context.check_hostname = False
    print(f'Connecting to {host} to get certificate...')
    conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=host)
    conn.settimeout(3.0)
    failure = False
    try:
        conn.connect((host, port))
        cert = conn.getpeercert()
        pprint.pprint(cert)
    except ssl.SSLError as e:
        # print (e)
        cert = e.verify_message
        failure = True
    return cert,failure

ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

hosts =[{'host':'x.x.x.x','port':3000},{'host': 'www.google.com', 'port': 443}]
for host in hosts:
    print("-" * 50)
    print(f'Starting to detect {host}')
    cert = get_cert (host['host'],host['port'])
    if cert[1] != True:
        cert_expiration = datetime.strptime(cert[0]['notAfter'], ssl_date_fmt)
        print('Certificate Expired: ', cert_expiration)
    else:
        print(cert)

# context = ssl.create_default_context()
# context.check_hostname = False
# print(f'Connecting to {host} to get certificate...')
# conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=host)
# conn.settimeout(3.0)
# try:
#     conn.connect((host, port))
#     cert = conn.getpeercert()
#     pprint.pprint(cert)
# except ssl.SSLError as e:
#     x = e
#     print (e)


