import sqlite3

connector = sqlite3.connect('storage.db')

class Data:

    def __init__(self):
        self.connector = sqlite3.connect('storage.db')
        self.modEntry = self.modEntry(self)
        self.verificationEntry = self.verificationEntry(self)
        self.taggingEntry = self.taggingEntry(self)

        # Setup 'modLogs' Databases if isn't valid
        try:
            # modLogs table container 
            connector.execute('''CREATE TABLE modLogs (
                ACTION TEXT NOT NULL,
                DURATION INTEGER NULL,
                REASON TEXT NOT NULL,
                MODERATOR INTEGER NOT NULL,
                TARGET INTEGER NOT NULL,
                DATE TEXT NOT NULL
            );''')

        except Exception as error:
            pass # Database table is already created

        # Setup 'verification' Database if isn't valid
        try:
            # verification table container
            connector.execute('''CREATE TABLE verification (
                DISCORDID BIGINT NOT NULL,
                USERNAME TEXT NOT NULL,
                USERID INTEGER NOT NULL,
                DATE TEXT NOT NULL
            );''')

        except Exception as error:
            pass # Database table is already created

        # Setup 'tagging' Database if isn't valid
        try:
            # Tagging table container
            connector.execute('''CREATE TABLE tagging (
                CHANNELID BIGINT NOT NULL,
                NAME TEXT NOT NULL,
                CONTENT TEXT NOT NULL,
                DATE TEXT NOT NULL
            );''')

        except Exception as error:
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
        
        def update(self, id, **kwargs):
            duration = kwargs.get("duration", None)
            reason = kwargs.get("reason", None)

            try:
                if duration:
                    self.cursor.execute('''UPDATE modLogs SET DURATION = (?) WHERE rowid = (?);''', (duration, id))
                elif reason:
                    self.cursor.execute('''UPDATE modLogs SET REASON = (?) WHERE rowid = (?);''', (reason, id))
            except sqlite3.Error as error:
                print(f'{error}')
                return False
            return True

    
    class verificationEntry:

        def __init__(self, Data):
            self.Data = Data
            self.connector = Data.connector
            self.cursor = self.connector.cursor()
        
        def insert(self, discordid, username, userid, date):
            try:
                self.cursor.execute('''INSERT INTO verification (DISCORDID, USERNAME, USERID, DATE) VALUES (?, ?, ?, ?);''', (discordid, username, userid, date))
                self.connector.commit()
            except sqlite3.Error as error:
                print(f'{error}')
        
        def fetch(self, id):
            index = 0
            try:
                self.cursor.execute('''SELECT * FROM verification''')
            except sqlite3.Error as error:
                print(f'{error}')
            
            for discordid, username, userid, date in self.cursor.fetchall():
                index += 1
                if int(discordid) == id:
                    return {
                        "index": index,
                        "discordid": discordid,
                        "username": username,
                        "userid": userid,
                        "date": date
                    }
        
        def check_discordid(self, value):
            try:
                self.cursor.execute('''SELECT * FROM verification''')
                for discordid, username, userid, date in self.cursor.fetchall():
                    if discordid == value:
                        return True
                return False
            except sqlite3.Error as error:
                print(f'{error}')
                return False
    

    class taggingEntry:

        def __init__(self, Data):
            self.Data = Data
            self.connector = Data.connector
            self.cursor = self.connector.cursor()
        
        def insert(self, channelid, name, content, date):
            try:
                self.cursor.execute('''INSERT INTO tagging (CHANNELID, NAME, CONTENT, DATE) VALUES (?, ?, ?, ?);''', (channelid, name, content, date))
                self.connector.commit()
            except sqlite3.Error as error:
                print(f'{error}')
        
        def fetch(self, indentifier, channelIdentifier):
            index = 0
            try:
                self.cursor.execute('''SELECT * FROM tagging''')
            except sqlite3.Error as error:
                print(f'{error}')
            
            for channelid, name, content, date in self.cursor.fetchall():
                index += 1
                if name == indentifier and channelid == channelIdentifier:
                    return {
                        "index": index,
                        "channelid": channelid,
                        "content": content,
                        "date": date
                    }
            return None
        
        def fetchAll(self, channelIdentifier):
            index = 0
            result = []
            try:
                self.cursor.execute('''SELECT * FROM tagging''')
            except sqlite3.Error as error:
                print(f'{error}')
            
            for channelid, name, content, date in self.cursor.fetchall():
                index += 1
                if channelid == channelIdentifier:
                    result.append({
                        "index": index,
                        "channelid": channelid,
                        "name": name,
                        "content": content,
                        "date": date
                    })
            return result
        
        def update(self, id, **kwargs):
            content = kwargs.get("content", None)
            date = kwargs.get("date", None)
            try:
                if content and date:
                    self.cursor.execute('''UPDATE tagging SET CONTENT = (?) WHERE rowid = (?);''', (content, id))
                    self.cursor.execute('''UPDATE tagging SET DATE = (?) WHERE rowid = (?);''', (date, id))
            except sqlite3.Error as error:
                print(f'{error}')
                return False
            return True
        
        def check_indentifier(self, indentifier):
            try:
                self.cursor.execute('''SELECT * FROM tagging''')
                for channelid, name, content, date in self.cursor.fetchall():
                    if name == indentifier:
                        return True
                return False
            except sqlite3.Error as error:
                print(f'{error}')
                return False