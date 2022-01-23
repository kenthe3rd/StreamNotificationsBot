import sqlite3
import os

class DatabaseManager:
    def addUser(self, twitchUser, author):
        if False == self.userInDB(twitchUser):
            query = "INSERT INTO streamers (user_login, online) VALUES (?,0);"
            params = [twitchUser]
            self.executeQuery(query, params)
        if False == self.serverInDB(author.guild):
            self.addServer(author.guild)
        self.associateUserAndServer(twitchUser, author.guild.id)    
        
    def addServer(self, server):
        query = "INSERT INTO servers (discord_id) VALUES (?);"
        params = [server.id]
        self.executeQuery(query, params)
        
    def executeQuery(self, query, params):
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        
    def getConnection(self):
        return sqlite3.connect(database=os.getenv('PATH_TO_SQLITE_DB'))
    
    def serverInDB(self, server):
        conn = self.getConnection()
        query = "SELECT id FROM servers WHERE discord_id = ?;"
        params = [server.id]
        cursor = conn.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row != None:
            return True
        else:
            return False
        
    def userInDB(self, twitchUser):
        conn = self.getConnection()
        query = "SELECT id FROM streamers WHERE user_login = ?;"
        params = [twitchUser]
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row != None:
            return True
        else:
            return False
    
    def associateUserAndServer(self, twitchUser, discordServerID):
        conn = self.getConnection()
        query = "SELECT id FROM streamers WHERE user_login = ?;"
        params = [twitchUser]
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        userID = row[0]
        query = "SELECT id FROM servers WHERE discord_id = ?"
        params = [discordServerID]
        cursor.execute(query, params)
        row = cursor.fetchone()
        serverID = row[0]
        query = "SELECT * FROM servers_streamers WHERE server = ? AND streamer = ?;"
        params = [userID, serverID]
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row == None:
            query = "INSERT INTO servers_streamers (streamer, server) VALUES (?,?);"
            cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        
    def setNotificationsChannel(self, channelName, author):
        if author.guild_permissions.administrator == False:
            return
        channels = author.guild.channels
        for channel in channels:
            if channel.name == channelName:
                query = "UPDATE servers SET notifications_channel = ? WHERE discord_id = ?;"
                params = [channel.id, author.guild.id]
                self.executeQuery(query, params)
                
    def getStreamerData(self):
        output = {}
        conn = self.getConnection()
        cursor = conn.cursor()
        query = "SELECT id, user_login, online FROM streamers;"
        params = []
        cursor.execute(query, params)
        while(True):
            row = cursor.fetchone()
            if row == None:
                break
            output[row[1]] = row
        cursor.close()        
        conn.close()
        return output
    
    def setStreamerOnline(self, user_login, online):
        query = "UPDATE streamers SET online = ? WHERE user_login = ?;"
        params =  [online, user_login]
        self.executeQuery(query, params)