import argparse
import importlib.util
import pwd
import socket
import sys

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


def load_config(config_path):
    spec = importlib.util.spec_from_file_location("config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config_module
    spec.loader.exec_module(config_module)
    return config_module


parser = argparse.ArgumentParser(description='Start the application with a given config file.')
parser.add_argument('config_path', type=str, help='The path to the config.py file')
args = parser.parse_args()

config_module = load_config(args.config_path)


db = Database()
services = []
for service_config in config_module.service_configs:
    service_class = service_config['service']
    service_class = ServiceBase
    service_instance = service_class(
        service_config['name'],
        service_config['ip'],
        service_config['port'],
        db,
        config_module.config,
        SessionBase
    )
    services.append(service_instance)

drop_privileges('hornpot')
hornpot = HornPot(services)