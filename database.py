import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('anpr_records.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plates
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             plate_number TEXT,
             timestamp TEXT)
        ''')
        self.conn.commit()

    def insert_record(self, plate_number, timestamp):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO plates (plate_number, timestamp) VALUES (?, ?)', (plate_number, timestamp))
        self.conn.commit()

    def __del__(self):
        self.conn.close()