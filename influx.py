import ast
from datetime import datetime
import json
import re
import sqlite3
import sys
import time
import pytz
from requests import Session

from services.Session import SessionBase

TIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


def get_timestamp():
    berlin_tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.fromtimestamp(time.time(), berlin_tz)

    return current_time.strftime(TIMEFORMAT)

def log(msg, module=None):

    if module is None:
        full_message = f'[{get_timestamp()}]: {msg}\n'
    else:
        full_message = f'[{get_timestamp()}][{module}]: {msg}\n'

    print(full_message, end='')

    with open("log.txt", 'a') as f:
        f.write(full_message)

def print_progress(current: float, total: float = 0, msg: str = "") -> None:
    if total == 0:
        sys.stdout.write(f"\r{msg} {int(current)}")
        sys.stdout.flush()
    else:
        percent = (current / total) * 100
        sys.stdout.write(f"\r{msg} {current} / {total} = {percent:.4f}%")
        sys.stdout.flush()



class Influx:

    def __init__(self, config_module):
        self.client = None
        try:
            from influxdb import InfluxDBClient
            host = config_module.influx_hostname
            port = config_module.influx_port
            username = config_module.influx_username
            password = config_module.influx_password
            database = config_module.influx_database_name
            self.client = InfluxDBClient(host, port, username, password, database)
            print("client ok")
        except Exception as e:
            self.client = None
            print(e)

    def add_session(self, session: SessionBase):
        try:
            data = {
                "measurement": "connection",
                "tags": {"session_handler": str(session.__class__.__name__), "server_port": session.own_port6,
                           "client_port": session.remote_port6,
                           "client_ip": session.remote_ip6,
                           "connected": session.connected,
                           "disconnect_reason": str(session.termination_reason)},
                "time": session.session_start,
                "fields": {"server_port": session.own_port6,
                           "client_port": session.remote_port6,
                           "client_ip": session.remote_ip6,
                           "connected": session.connected,
                           "disconnect_reason": str(session.termination_reason)}
            }

            self.client.write_points([data])
            print(f"Data submitted: {data}")

        except Exception as e:
            print(f"Error submitting data: {e}")

