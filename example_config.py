import socket

from services.Session import SessionBase
from services.Session_HTTP import SessionHTTP
from services.Session_ssh import SessionSSH
from services.Session_telnet import SessionTelnet
from services.Session_SMB import SessionSMB
ip4 = "0.0.0.0"
ip6 = "::"
ip = "::"

user = "user"

# TODO: also adda quota for number of overall connections and/or connections per time of one ip or ip range to avoid flooding
quota = {'idle': 10, 'active': 10, 'tx': 10*1024, 'rx': 10*1024}

config = {'quota': quota}


service_configs = []
service_configs.append({'name': 'telnet', 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': 23, 'session': SessionTelnet})
service_configs.append({'name': 'webserver', 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': 80, 'session': SessionHTTP})
service_configs.append({'name': 'telnet', 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': 445, 'session': SessionSMB})


# add ports to disable it. e.g. for using ssh
skip = set([])

for service in service_configs:
    skip.add(service['port'])



for port in range(1, pow(2,16)-1):
    continue
    if port in skip:
        continue
    service_configs.append({'name': str(port), 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': port, 'session': SessionBase})


# push stats to an influx db
influx_enabled = False
influx_hostname = ''
influx_port = 0
influx_username = ''
influx_password = ''
influx_database_name = ''
