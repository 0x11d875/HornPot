import ast
import datetime
import json
import re
import sqlite3
import sys
import time
import pytz


TIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


def get_timestamp():
    # Get current time with Berlin timezone
    berlin_tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.fromtimestamp(time.time(), berlin_tz)

    # Return the timestamp in ISO format with timezone info
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

    def add_session(self, session):
        try:
            data = {
                "measurement": "connection",
                "tags": {"session_handler": str(session.__class__.__name__)},
                "time": session.session_start,
                "fields": {"server_port": session.own_port6,
                           "client_port": session.remote_port6,
                           "client_ip": session.remote_ip6,
                           "disconnect_reason": str(session.termination_reason)}
            }

            self.client.write_points([data])
            print(f"Data submitted: {data}")

        except Exception as e:
            print(f"Error submitting data: {e}")



class Database:
    # VERISON NOTES:
    # 0.0.1 -> 0.0.2: Added messages table

    def __init__(self, config_module):
        self.config_module = config_module
        self.con = sqlite3.connect('connections.db')
        self.cur = self.con.cursor()

        self.VERSION = "0.0.2"
        self.current_version = "0.0.0"
        self.message_cache = {}



        self.init()
        self.upgrade()

    def __del__(self):
        self.con.commit()
        self.con.close()

    def __update_version(self, old, new):
        insert_query = """INSERT INTO "database_version" 
                          ("timestamp", "old_version", "current_version")
                          VALUES (?, ?, ?)"""
        self.cur.execute(insert_query, (get_timestamp(), old, new))
        self.con.commit()

    def upgrade(self):

        last_version = None

        while last_version != self.VERSION:
            self.cur.execute('SELECT "current_version" FROM "database_version" ORDER BY "id" DESC LIMIT 1')
            last_version = self.cur.fetchone()[0]
            if last_version == self.VERSION:
                break

            if last_version is None:
                print(f"DB update {last_version} -> 0.0.1")
                self.__update_version("0.0.0", "0.0.1")
                self.con.commit()

            elif last_version == "0.0.1":
                print(f"DB update {last_version} -> 0.0.2")
                self.cur.execute("SELECT id, conversation FROM sessions")
                sessions = self.cur.fetchall()
                # batch size for committing
                batch_size = 100000
                batch_count = 0

                pattern = r"(\[[rt]\])(\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\]): (b'.*')"

                for session_id, conversation in sessions:
                    if conversation == '[]':
                        continue
                    conversation_lst = ast.literal_eval(conversation)
                    new_conversation = []
                    for message in conversation_lst:
                        match = re.match(pattern, message)
                        if match:
                            # Extract the groups
                            direction = match.group(1).replace("[", "").replace("]", "")
                            timestamp = match.group(2).replace("[", "").replace("]", "")
                            message_content = match.group(3)

                            message_id = self.get_or_insert_message(message_content)

                            new_conversation.append((direction, timestamp, message_id))

                    conversation_json = json.dumps(new_conversation)
                    print_progress(session_id, len(sessions), f"Updating conversations...")
                    self.cur.execute("UPDATE sessions SET conversation = ? WHERE id = ?", (conversation_json, session_id))

                    batch_count += 1
                    if batch_count % batch_size == 0:
                        self.con.commit()

                self.con.commit()
                self.cur.execute("VACUUM;")

                self.__update_version(last_version, "0.0.2")
                self.con.commit()

    def init(self):
        connections_table = """CREATE TABLE IF NOT EXISTS "sessions" (
                            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "start_time"	TEXT,
                            "end_time" TEXT,
                            "client_ip"	TEXT,
                            "client_port"	TEXT,
                            "server_port"	TEXT,
                            "session_hand ler"	TEXT,
                            "conversation"	TEXT,
                            "disconnected_reason" TEXT,
                            "downloads"	TEXT
                            );"""

        self.cur.execute(connections_table)


        message_table = """CREATE TABLE IF NOT EXISTS "messages" (
                            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "message" BLOB
                            );"""

        self.cur.execute(message_table)


        version_Table = """CREATE TABLE IF NOT EXISTS "database_version" (
                            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "timestamp"	TEXT,
                            "old_version"	TEXT,
                            "current_version"	TEXT
                            );"""

        self.cur.execute(version_Table)

        # Check if versions are empty
        self.cur.execute('SELECT COUNT(*) FROM "database_version"')
        count = self.cur.fetchone()[0]

        if count == 0:
            insert_query = """INSERT INTO "database_version" 
                              ("timestamp", "old_version", "current_version")
                              VALUES (?, ?, ?)"""
            self.cur.execute(insert_query, (get_timestamp(), "0.0.0", self.VERSION))
            self.con.commit()


    def get_or_insert_message(self, message):
        if message in self.message_cache:
            return self.message_cache[message]

        self.cur.execute("SELECT id FROM messages WHERE message = ?", (message,))
        result = self.cur.fetchone()

        if result:
            message_id = result[0]
        else:
            self.cur.execute("INSERT INTO messages (message) VALUES (?)", (message,))
            message_id = self.cur.lastrowid

        self.message_cache[message] = message_id
        return message_id


    def add_session(self, session):

        conversation_prepared = []
        pattern = r"(\[[rt]\])(\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\]): (b'.*')"
        for message in session.conversation:
            match = re.match(pattern, message)
            if match:
                # Extract the groups
                direction = match.group(1).replace("[", "").replace("]", "")
                timestamp = match.group(2).replace("[", "").replace("]", "")
                message_content = match.group(3)

                message_id = self.get_or_insert_message(message_content)

                conversation_prepared.append((direction, timestamp, message_id))

        insert_query = """
        INSERT INTO sessions (start_time, client_ip, client_port, server_port, session_handler, conversation, end_time, disconnected_reason, downloads) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cur.execute(insert_query, (str(session.session_start,),
                                        str( session.remote_ip6),
                                        str(session.remote_port6),
                                        str(session.own_port6),
                                        str(str(session.__class__.__name__)),
                                        str(json.dumps(conversation_prepared)),
                                        str(get_timestamp()),
                                        str(session.termination_reason),
                                        str(session.downloads)))
        self.con.commit()

        if self.config_module.influx_enabled:
            influx_client = Influx(self.config_module)
            influx_client.add_session(session)
