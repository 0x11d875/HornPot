import datetime
import sqlite3
import time


def get_timestamp():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S'))

def log(msg, module=None):

    if module is None:
        full_message = f'[{get_timestamp()}]: {msg}\n'
    else:
        full_message = f'[{get_timestamp()}][{module}]: {msg}\n'

    print(full_message, end='')

    with open("log.txt", 'a') as f:
        f.write(full_message)






class Database:

    def __init__(self):
        self.con = sqlite3.connect('connections.db')
        self.cur = self.con.cursor()

        self.create_tables()

    def __del__(self):
        self.con.close()

    def create_tables(self):
        connections_table = """CREATE TABLE IF NOT EXISTS "sessions" (
                            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "timestamp"	TEXT,
                            "source_ip"	TEXT,
                            "source_port"	TEXT,
                            "conservation"	TEXT,
                            "downloads"	TEXT
                            );"""

        self.cur.execute(connections_table)


    def add_session(self, timestamp: str, source_ip: str, source_port: str, conservation: str, downloads=""):
        insert_query = """
        INSERT INTO sessions (timestamp, source_ip, source_port, conservation, downloads) 
        VALUES (?, ?, ?, ?, ?)
        """
        self.cur.execute(insert_query, (str(timestamp), str(source_ip), str(source_port), str(conservation), str(downloads)))
        self.con.commit()
