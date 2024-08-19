import socket

from services.Session import SessionBase
from services.Session_HTTP import SessionHTTP

ip4 = "0.0.0.0"
ip6 = "::"
ip = "::"

user = "user"

# TODO: also adda quota for number of overall connections and/or connections per time of one ip or ip range to avoid flooding
quota = {'idle': 60, 'active': 60, 'tx': 10*1024, 'rx': 10*1024}

config = {'quota': quota}


service_configs = []
service_configs.append({'name': 'telnet', 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': 2223, 'session': SessionBase})
service_configs.append({'name': 'telnet', 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': 8080, 'session': SessionHTTP})
