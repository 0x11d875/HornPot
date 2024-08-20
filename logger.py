import datetime
import sqlite3
import time

TIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%f'

def get_timestamp():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime(TIMEFORMAT))

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

        self.VERSION = "0.0.1"
        self.current_version = "0.0.0"

        self.init()
        self.upgrade()

    def __del__(self):
        self.con.close()


    def upgrade(self):
        # TODO
        return

        last_version = self.current_version

        while last_version != self.VERSION:
            self.cur.execute('SELECT "current_version" FROM "database_version" ORDER BY "id" DESC LIMIT 1')
            last_version = self.cur.fetchone()
            if last_version is None or last_version == self.VERSION:
                break

            if last_version == "0.0.0":
                insert_query = """INSERT INTO "database_version" 
                                  ("timestamp", "old_version", "current_version")
                                  VALUES (?, ?, ?)"""
                self.cur.execute(insert_query, (get_timestamp(), "0.0.0", "0.0.1"))
                self.con.commit()



    def init(self):
        connections_table = """CREATE TABLE IF NOT EXISTS "sessions" (
                            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "start_time"	TEXT,
                            "end_time" TEXT,
                            "client_ip"	TEXT,
                            "client_port"	TEXT,
                            "server_port"	TEXT,
                            "session_handler"	TEXT,
                            "conversation"	TEXT,
                            "disconnected_reason" TEXT,
                            "downloads"	TEXT
                            );"""

        self.cur.execute(connections_table)



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


    def add_session(self, session):
        insert_query = """
        INSERT INTO sessions (start_time, client_ip, client_port, server_port, session_handler, conversation, end_time, disconnected_reason, downloads) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cur.execute(insert_query, (str(session.session_start,),
                                        str( session.remote_ip6),
                                        str(session.remote_port6),
                                        str(session.own_port6),
                                        str(str(session.__class__.__name__)),
                                        str(session.conversation),
                                        str(session.session_end),
                                        str(session.termination_reason),
                                        str(session.downloads)))
        self.con.commit()
