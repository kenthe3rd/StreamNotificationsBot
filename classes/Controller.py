import classes.DatabaseManager as db
import time
import classes.TwitchHelper as th
import classes.DiscordHelper as dh

class Controller:
    async def run(self):
        database = db.DatabaseManager()
        twitch = th.TwitchHelper()
        discord = dh.DiscordHelper()
        conn = database.getConnection()
        cursor = conn.cursor()
        query = "SELECT user_login, online FROM streamers;"
        params = []
        cursor.execute(query, params)
        data = {}
        while(True):
            row = cursor.fetchone()
            if row == None:
                cursor.close()
                conn.close()
                break
            data[row[0]] = row[1]
        for user_login in data:
            streamData = twitch.getStream(user_login)
            onlineInDB = data[user_login]
            if streamData['data'] != [] and onlineInDB == False:
                #print(streamData['data'][0])
                await discord.broadcastStreamerWentOnline(user_login, streamData['data'][0])
                database.setStreamerOnline(user_login, 1)
            elif streamData['data'] == [] and onlineInDB == True:
                database.setStreamerOnline(user_login, 0)
