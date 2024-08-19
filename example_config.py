import socket

from services import ServiceBase

ip = "0.0.0.0"
# TODO: also adda quota for number of overall connections and/or connections per time of one ip or ip range to avoid flooding
quota = {'idle': 60, 'active': 60, 'tx': 4*1024, 'rx': 4*1024}

config = {'quota': quota}


service_configs = []
service_configs.append({'name': 'telnet', 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': 2223, 'service': ServiceBase})
