import sqlite3

connector = sqlite3.connect('storage.db')

class Data:

    def __init__(self):
        self.connector = sqlite3.connect('storage.db')
        self.modEntry = self.modEntry(self)

        # Setup Database if isn't valid
        try: 
            connector.execute('''CREATE TABLE modLogs (
                ACTION TEXT NOT NULL,
                DURATION INTEGER NULL,
                REASON TEXT NOT NULL,
                MODERATOR INTEGER NOT NULL,
                TARGET INTEGER NOT NULL,
                DATE TEXT NOT NULL
            );''')
        except Exception as error:
            print(f'db init Exception: {error}')
            pass # Database table is already created
    
    class modEntry:

        def __init__(self, Data):
            self.Data = Data
            self.connector = Data.connector
            self.cursor = self.connector.cursor()
        
        def insert(self, action, duration, reason, moderator, target, date):
            try:
                self.cursor.execute('''INSERT INTO modLogs (ACTION, DURATION, REASON, MODERATOR, TARGET, DATE) VALUES (?, ?, ?, ?, ?, ?);''', (action, duration, reason, moderator, target, date))
                self.connector.commit()
                self.cursor.close()
            except sqlite3.Error as error:
                print(f'{error}')
        
        def fetch(self, id):
            result = []
            index = 0
            try:
                self.cursor.execute('''SELECT * FROM modLogs''')
            except sqlite3.Error as error:
                print(f'{error}')
            
            for action, duration, reason, moderator, target, date in self.cursor.fetchall():
                index += 1
                print(index, action, duration, reason, moderator, target, date)
                if int(target) == id:
                    result.append({
                        "index": index,
                        "action": action,
                        "duration": duration,
                        "reason": reason,
                        "moderator": moderator,
                        "target": target,
                        "date": date
                    })
            return result