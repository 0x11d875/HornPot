import pwd
import socket

from HornPot import HornPot
from logger import Database
from services.ServiceBase import ServiceBase
from services.Session import SessionBase

def drop_privileges(username):
    try:
        user_info = pwd.getpwnam(username)
        uid = user_info.pw_uid
        gid = user_info.pw_gid

        # switch the group
        import os
        os.setgid(gid)
        os.setegid(gid)

        # switch the user
        os.setuid(uid)
        os.seteuid(uid)

        # Ensure that we dropped privileges successfully
        assert os.getuid() == uid and os.getgid() == gid
        print(f"Dropped privileges to user: {username} (UID: {uid}, GID: {gid})")

    except KeyError:
        raise ValueError(f"User {username} does not exist")
    except OSError as e:
        raise RuntimeError(f"Could not drop privileges: {e}")



ip = "0.0.0.0"
db = Database()


service_configs = []
service_configs.append({'name': 'telnet', 'protocol': socket.SOCK_STREAM, 'ip': ip, 'port': 2223, 'service': ServiceBase})


services = []
for service_config in service_configs:
    service_class = service_config['service']
    service_instance = service_class(service_config['name'], service_config['ip'], service_config['port'], db, SessionBase)
    services.append(service_instance)


drop_privileges('hornpot')
hornpot = HornPot(services)